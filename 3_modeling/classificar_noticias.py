# Classifica o sentimento de todas as notícias coletadas, usando a rota /processar_texto da API (TP4).
# O resultado vira um dado processado, usado nos gráficos e no assistente da página "Insights com IA".
#
# Rodar a partir da pasta do projeto, com a API ligada em outro terminal:
#   python -m uvicorn api:app --reload
#   python 3_modeling/classificar_noticias.py

import pandas as pd
import requests

URL_API = "http://127.0.0.1:8000/processar_texto"
ARQUIVO_ENTRADA = "data/raw/noticias_saneamento.csv"
ARQUIVO_SAIDA = "data/processed/noticias_sentimento.csv"

noticias = pd.read_csv(ARQUIVO_ENTRADA)
sentimentos = []
confiancas = []

for numero, titulo in enumerate(noticias["titulo"], start=1):
    try:
        resposta = requests.post(URL_API, json={"texto": titulo}, timeout=60)
    except requests.exceptions.ConnectionError:
        raise SystemExit("A API não está rodando. Em outro terminal, rode: python -m uvicorn api:app --reload")

    if resposta.status_code != 200:
        raise SystemExit(f"A API respondeu com erro {resposta.status_code}: {resposta.json().get('detail')}")

    resultado = resposta.json()["resultado"]
    sentimentos.append(resultado["sentimento"])
    confiancas.append(resultado["confianca"])
    print(f"{numero}/{len(noticias)}: {resultado['sentimento']} | {titulo[:70]}")

noticias["sentimento"] = sentimentos
noticias["confianca"] = confiancas
noticias.to_csv(ARQUIVO_SAIDA, index=False)

print(f"\n{len(noticias)} notícias classificadas e salvas em {ARQUIVO_SAIDA}")
print(noticias["sentimento"].value_counts(normalize=True).mul(100).round(1).to_string())
