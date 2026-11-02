import pandas as pd
import requests
import streamlit as st

# Endereço da API FastAPI (rodar antes: uvicorn api:app --reload)
URL_API = "http://127.0.0.1:8000"

st.title("Integração com a API")
st.write(
    "Esta página consome a API FastAPI do projeto. A documentação completa das rotas "
    f"fica em {URL_API}/docs."
)

st.header("Consultar indicadores (GET /indicadores)")
pais = st.text_input("País ou região (nome em inglês, ex.: Brazil, World)", "Brazil")

resposta = requests.get(f"{URL_API}/indicadores", params={"pais": pais})
st.dataframe(pd.DataFrame(resposta.json()), hide_index=True)

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
    resposta = requests.post(f"{URL_API}/indicadores", json=novo_dado)
    st.write(resposta.json())
