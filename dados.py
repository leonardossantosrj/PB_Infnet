# Funções e constantes usadas por várias páginas do app (evita repetir código).

import re
from collections import Counter

import pandas as pd
import streamlit as st

COLUNAS = {
    "Entity": "País",
    "Year": "Ano",
    "wat_bas": "Água básica (%)",
    "wat_sm": "Água segura (%)",
    "san_bas": "Esgoto básico (%)",
    "san_sm": "Esgoto seguro (%)",
}
INDICADORES = ["Água básica (%)", "Água segura (%)", "Esgoto básico (%)", "Esgoto seguro (%)"]

# Palavras muito comuns que não ajudam na nuvem de palavras
STOPWORDS = {
    "para", "pela", "pelo", "pelas", "pelos", "como", "mais", "mas", "entre", "sobre",
    "também", "quando", "onde", "isso", "essa", "esse", "esta", "este", "seus", "suas",
    "sua", "seu", "dos", "das", "nos", "nas", "aos", "que", "com", "uma", "não", "são",
    "foi", "ser", "tem", "têm", "pode", "podem", "sendo", "está", "estão", "muito",
    "outros", "outras", "cada", "desde", "até", "após", "ainda", "apenas", "forma",
    "sem", "por", "the", "and",
} #talvez aqui pudesse usar a própria biblioteca do skt-learn, como fiz junto com a IA queria entender como era o stopwords de outra
#forma de implementação.


# ---------- Funções de carga com cache: os arquivos são lidos só uma vez ----------
@st.cache_data
def carregar_indicadores():
    dados = pd.read_csv("data/raw/oms_unicef_agua_saneamento.csv")
    return dados[list(COLUNAS)].rename(columns=COLUNAS)


@st.cache_data
def carregar_texto():
    with open("data/raw/wikipedia_saneamento.txt", encoding="utf-8") as arquivo:
        return arquivo.read()


@st.cache_data
def carregar_noticias():
    return pd.read_csv("data/raw/noticias_saneamento.csv")


@st.cache_data
def contar_palavras(texto):
    palavras = re.findall(r"[a-záéíóúâêôãõç]+", texto.lower())
    palavras = [p for p in palavras if len(p) > 3 and p not in STOPWORDS]
    return Counter(palavras)
