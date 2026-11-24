import json

import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from transformers import pipeline

app = FastAPI(
    title="API Painel Saneamento Brasil",
    description="Consulta e envio de indicadores de acesso à água e ao esgoto (ODS 6) "
    "e análise de sentimento de textos com um modelo de linguagem rodando localmente.",
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

# ---------- Modelo de linguagem local (TP4) ----------
NOME_MODELO = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
ROTULOS = {"positive": "positivo", "neutral": "neutro", "negative": "negativo"}


# Se o carregamento falhar, a API sobe mesmo assim, e a rota /processar_texto responde 503.
try:
    classificador = pipeline("text-classification", model=NOME_MODELO, tokenizer=NOME_MODELO)
    erro_modelo = None
except Exception as erro:
    classificador = None
    erro_modelo = str(erro)


# ---------- Modelos de entrada e de resposta ----------
class Indicador(BaseModel):
    pais: str
    ano: int
    agua_basica: float = Field(ge=0, le=100)
    agua_segura: float = Field(ge=0, le=100)
    esgoto_basico: float = Field(ge=0, le=100)
    esgoto_seguro: float = Field(ge=0, le=100)


class IndicadorResposta(BaseModel):
    pais: str
    ano: int
    agua_basica: float | None 
    agua_segura: float | None
    esgoto_basico: float | None
    esgoto_seguro: float | None


class RespostaEnvio(BaseModel):
    message: str
    indicador: Indicador


class EntradaTexto(BaseModel):
    texto: str = Field(
        min_length=3,
        max_length=2000,
        examples=["Investimento em saneamento cresce 51% após Marco Legal"],
    )


class ResultadoSentimento(BaseModel):
    sentimento: str
    confianca: float = Field(ge=0, le=1)


class RespostaProcessamento(BaseModel):
    texto: str
    tipo_analise: str
    modelo: str
    resultado: ResultadoSentimento


# ---------- Erros de validação com mensagem clara ----------
@app.exception_handler(RequestValidationError)
async def erro_de_validacao(request: Request, exc: RequestValidationError):
    erros = []
    for e in exc.errors():
        campo = " > ".join(str(parte) for parte in e["loc"])
        erros.append(f"{campo}: {e['msg']}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Dados de entrada inválidos. Confira os campos abaixo.", "erros": erros},
    )


def carregar_dados():
    try:
        oficiais = pd.read_csv("data/raw/oms_unicef_agua_saneamento.csv")
        enviados = pd.read_csv(ARQUIVO_ENVIADOS)
    except FileNotFoundError as erro:
        raise HTTPException(status_code=503, detail=f"Base de dados indisponível: {erro.filename}")
    oficiais = oficiais[list(COLUNAS)].rename(columns=COLUNAS)
    return pd.concat([oficiais, enviados])


# ---------- Rotas ----------
@app.get("/indicadores", response_model=list[IndicadorResposta])
def consultar_indicadores(pais: str = "Brazil"):
    """
    Retorna os indicadores de água e esgoto de um país ou região, ano a ano.

    - **pais**: nome em inglês, como no arquivo da OMS/UNICEF (ex.: Brazil, World).
      Também encontra os registros enviados pela rota POST.
    - Responde **404** se não houver dados para o nome informado.
    """
    dados = carregar_dados()
    dados = dados[dados["pais"] == pais]
    if dados.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum dado encontrado para '{pais}'. Use o nome em inglês, como Brazil ou World.",
        )
    # to_json troca os valores vazios (NaN) por null, que o formato JSON aceita
    return json.loads(dados.to_json(orient="records"))


@app.post("/indicadores", response_model=RespostaEnvio)
def enviar_indicador(indicador: Indicador):
    """
    Adiciona um novo registro de indicadores, por exemplo de um estado ou município.

    O registro é salvo em data/processed/indicadores_api.csv e passa a aparecer
    na rota GET /indicadores. Os percentuais devem estar entre 0 e 100 (senão, 422).
    """
    novo = pd.DataFrame([indicador.model_dump()])
    novo.to_csv(ARQUIVO_ENVIADOS, mode="a", header=False, index=False)
    return {"message": "Indicador salvo com sucesso", "indicador": indicador}


@app.post("/processar_texto", response_model=RespostaProcessamento)
def processar_texto(entrada: EntradaTexto):
    """
    Classifica o sentimento de um texto (positivo, neutro ou negativo) com um modelo
    de linguagem que roda localmente, sem chamar serviços na nuvem.

    - **texto**: de 3 a 2.000 caracteres, por exemplo o título de uma notícia.
    - Responde **400** se o texto tiver só espaços, **422** se estiver fora do tamanho,
      **503** se o modelo não carregou e **500** se o modelo falhar ao processar.
    """
    if classificador is None:
        raise HTTPException(
            status_code=503,
            detail=f"O modelo de linguagem não está disponível. Motivo: {erro_modelo}",
        )

    if not entrada.texto.strip():
        raise HTTPException(status_code=400, detail="O texto não pode conter apenas espaços.")

    try:
        # truncation=True corta textos acima do limite do modelo, em vez de dar erro
        saida = classificador(entrada.texto, truncation=True)[0]
    except Exception as erro:
        raise HTTPException(status_code=500, detail=f"Erro ao processar o texto no modelo: {erro}")

    return {
        "texto": entrada.texto,
        "tipo_analise": "classificação de sentimento",
        "modelo": NOME_MODELO,
        "resultado": {
            "sentimento": ROTULOS.get(saida["label"].lower(), saida["label"]),
            "confianca": round(saida["score"], 4),
        },
    }
