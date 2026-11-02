# API do Painel Saneamento Brasil.
# Documentação automática: http://127.0.0.1:8000/docs

import json

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="API Painel Saneamento Brasil",
    description="Consulta e envio de indicadores de acesso à água e ao esgoto (ODS 6).",
)

# Nomes das colunas na API: sem acentos e sem símbolos, mais fáceis de usar em JSON
COLUNAS = {
    "Entity": "pais",
    "Year": "ano",
    "wat_bas": "agua_basica",
    "wat_sm": "agua_segura",
    "san_bas": "esgoto_basico",
    "san_sm": "esgoto_seguro",
}
ARQUIVO_ENVIADOS = "data/processed/indicadores_api.csv"


class Indicador(BaseModel):
    pais: str
    ano: int
    agua_basica: float = Field(ge=0, le=100)
    agua_segura: float = Field(ge=0, le=100)
    esgoto_basico: float = Field(ge=0, le=100)
    esgoto_seguro: float = Field(ge=0, le=100)


def carregar_dados():
    oficiais = pd.read_csv("data/raw/oms_unicef_agua_saneamento.csv")
    oficiais = oficiais[list(COLUNAS)].rename(columns=COLUNAS)
    enviados = pd.read_csv(ARQUIVO_ENVIADOS)
    return pd.concat([oficiais, enviados])


@app.get("/indicadores")
def consultar_indicadores(pais: str = "Brazil"):
    """
    Retorna os indicadores de água e esgoto de um país ou região, ano a ano.

    - **pais**: nome em inglês, como no arquivo da OMS/UNICEF (ex.: Brazil, World).
      Também encontra os registros enviados pela rota POST.
    """
    dados = carregar_dados()
    dados = dados[dados["pais"] == pais]
    # to_json troca os valores vazios (NaN) por null, que o formato JSON aceita
    return json.loads(dados.to_json(orient="records"))


@app.post("/indicadores")
def enviar_indicador(indicador: Indicador):
    """
    Adiciona um novo registro de indicadores, por exemplo de um estado ou município.

    O registro é salvo em data/processed/indicadores_api.csv e passa a aparecer
    na rota GET /indicadores. Os percentuais devem estar entre 0 e 100.
    """
    novo = pd.DataFrame([indicador.model_dump()])
    novo.to_csv(ARQUIVO_ENVIADOS, mode="a", header=False, index=False)
    return {"message": "Indicador salvo com sucesso", "indicador": indicador}
