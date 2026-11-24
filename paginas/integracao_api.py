import pandas as pd
import requests
import streamlit as st

from dados import carregar_noticias

URL_API = "http://127.0.0.1:8000"

def chamar_api(metodo, rota, **kwargs):
    """Chama a API e mostra uma mensagem clara se ela estiver fora do ar ou responder com erro."""
    try:
        resposta = requests.request(metodo, f"{URL_API}{rota}", timeout=60, **kwargs)
    except requests.exceptions.ConnectionError:
        st.error("A API não está rodando. Abra outro terminal e rode: python -m uvicorn api:app --reload")
        return None
    except requests.exceptions.Timeout:
        st.error("A API demorou mais de 60 segundos para responder. Tente de novo com um texto menor.")
        return None

    if resposta.status_code != 200:
        st.error(f"Erro {resposta.status_code}: {resposta.json().get('detail')}")
        return None
    return resposta.json()


st.title("Integração com a API")
st.write(
    "Esta página consome a API FastAPI do projeto. A documentação completa das rotas "
    f"fica em {URL_API}/docs."
)

# ---------- modelo de linguagem local ----------
st.header("Análise de sentimento com modelo local (POST /processar_texto)")
st.write(
    "O texto é analisado pelo modelo cardiffnlp/twitter-xlm-roberta-base-sentiment, "
    "que roda no próprio computador, sem serviços na nuvem."
)

noticias = carregar_noticias()
titulo = st.selectbox("Escolha uma notícia coletada para preencher o texto", noticias["titulo"])
texto = st.text_area("Texto para analisar (pode editar)", titulo)

if st.button("Analisar sentimento"):
    with st.spinner("Processando no modelo local..."):
        analise = chamar_api("POST", "/processar_texto", json={"texto": texto})
    if analise:
        col1, col2 = st.columns(2)
        col1.metric("Sentimento", analise["resultado"]["sentimento"])
        col2.metric("Confiança", f"{analise['resultado']['confianca']:.0%}")
        st.caption(f"Tipo de análise: {analise['tipo_analise']} · Modelo: {analise['modelo']}")

# ---------- consulta e envio de indicadores ----------
st.header("Consultar indicadores (GET /indicadores)")
pais = st.text_input("País ou região (nome em inglês, ex.: Brazil, World)", "Brazil")

indicadores = chamar_api("GET", "/indicadores", params={"pais": pais})
if indicadores:
    st.dataframe(pd.DataFrame(indicadores), hide_index=True)

st.header("Enviar novo indicador (POST /indicadores)")
with st.form("novo_indicador"):
    novo_pais = st.text_input("País, região ou município")
    ano = st.number_input("Ano", min_value=2000, max_value=2033, value=2024)
    agua_basica = st.number_input("Água básica (%)", min_value=0.0, max_value=100.0)
    agua_segura = st.number_input("Água segura (%)", min_value=0.0, max_value=100.0)
    esgoto_basico = st.number_input("Esgoto básico (%)", min_value=0.0, max_value=100.0)
    esgoto_seguro = st.number_input("Esgoto seguro (%)", min_value=0.0, max_value=100.0)
    enviar = st.form_submit_button("Enviar")

if enviar:
    novo_dado = {
        "pais": novo_pais,
        "ano": ano,
        "agua_basica": agua_basica,
        "agua_segura": agua_segura,
        "esgoto_basico": esgoto_basico,
        "esgoto_seguro": esgoto_seguro,
    }
    salvo = chamar_api("POST", "/indicadores", json=novo_dado)
    if salvo:
        st.success(salvo["message"])
