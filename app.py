import re
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from wordcloud import WordCloud

st.set_page_config(page_title="Painel Saneamento Brasil", layout="wide")

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
}


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


# ---------- Estado de sessão: guarda os dados enviados pelo usuário ----------
if "dados_usuario" not in st.session_state:
    st.session_state["dados_usuario"] = pd.DataFrame()


def salvar_upload():
    # Roda assim que um arquivo é enviado, antes do resto da página ser recarregado
    if st.session_state["arquivo"] is not None:
        st.session_state["dados_usuario"] = pd.read_csv(st.session_state["arquivo"])


def limpar_upload():
    st.session_state["dados_usuario"] = pd.DataFrame()


indicadores = pd.concat([carregar_indicadores(), st.session_state["dados_usuario"]])

st.title("Painel Saneamento Brasil: ODS 6")

aba_sobre, aba_indicadores, aba_web, aba_upload = st.tabs(
    ["Sobre o projeto", "Indicadores", "Conteúdo da web", "Enviar dados"]
)

# ---------- Aba 1: sobre o projeto ----------
with aba_sobre:
    st.header("Problema de negócio")
    st.write(
        "Em 2020, apenas 48,7% da população brasileira tinha esgotamento sanitário gerenciado "
        "de forma segura, abaixo da média mundial de 54,0% (OMS/UNICEF). O Marco Legal do "
        "Saneamento (Lei 14.026/2020) definiu como meta, até 2033, levar água potável a 99% da "
        "população e coleta e tratamento de esgoto a 90%. Os dados para acompanhar esse avanço "
        "existem, mas estão espalhados em bases técnicas, muitas vezes em inglês, e são difíceis "
        "de interpretar. Isso dificulta que gestores públicos, ONGs e cidadãos acompanhem a "
        "evolução do saneamento e cobrem resultados."
    )

    st.header("Objetivos do projeto")
    st.markdown(
        """
- Reunir em um único painel os indicadores de acesso à água e ao esgoto do Brasil.
- Comparar o Brasil com outros países e com a média mundial.
- Exibir notícias e conteúdos da web sobre saneamento no Brasil.
- Usar IA generativa (LLM) para explicar os indicadores em linguagem simples.
"""
    )

    st.header("Links úteis")
    st.markdown(
        """
- [ONU: Objetivo 6, Água potável e saneamento](https://unric.org/pt/objetivo-6-agua-potavel-e-saneamento-2/)
- [Lei 14.026/2020: Marco Legal do Saneamento](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/lei/L14026.htm)
- [OMS/UNICEF JMP: dados de água e saneamento](https://washdata.org)
- [Our World in Data: Clean Water and Sanitation](https://ourworldindata.org/clean-water-sanitation)
- [Instituto Trata Brasil](https://tratabrasil.org.br)
- [Conecta Brasil](https://conectabrasil.org/home)
- [Observatório do Terceiro Setor: projetos sociais](https://observatorio3setor.org.br/carrossel/lista-conheca-projetos-sociais-de-15-causas-diferentes/)
"""
    )

    st.header("Amostra dos dados")
    st.dataframe(indicadores[indicadores["País"] == "Brazil"].tail(10), hide_index=True)

# ---------- Aba 2: indicadores com filtros ----------
with aba_indicadores:
    brasil_2020 = indicadores[(indicadores["País"] == "Brazil") & (indicadores["Ano"] == 2020)]
    col1, col2 = st.columns(2)
    col1.metric("Brasil 2020: água segura", f"{brasil_2020['Água segura (%)'].iloc[0]}%")
    col2.metric("Brasil 2020: esgoto seguro", f"{brasil_2020['Esgoto seguro (%)'].iloc[0]}%")

    paises = st.multiselect(
        "Países ou regiões",
        sorted(indicadores["País"].unique()),
        default=["Brazil", "World", "Latin America and the Caribbean"],
    )
    indicador = st.selectbox("Indicador", INDICADORES, index=3)
    anos = st.slider("Período", 2000, 2020, (2000, 2020))

    filtrado = indicadores[
        indicadores["País"].isin(paises)
        & (indicadores["Ano"] >= anos[0])
        & (indicadores["Ano"] <= anos[1])
    ]

    st.subheader(indicador)
    grafico = filtrado.pivot(index="Ano", columns="País", values=indicador)
    grafico.index = grafico.index.astype(str)  # evita o ano aparecer como "2,000" no eixo
    st.line_chart(grafico)

    st.dataframe(filtrado, hide_index=True)
    st.download_button(
        "Baixar dados filtrados (CSV)",
        filtrado.to_csv(index=False),
        file_name="indicadores_filtrados.csv",
        mime="text/csv",
    )

# ---------- Aba 3: conteúdo extraído da web ----------
with aba_web:
    st.header("Wikipedia: Saneamento básico")
    texto = carregar_texto()
    contagem = contar_palavras(texto)

    col1, col2, col3 = st.columns(3)
    col1.metric("Parágrafos", len(texto.split("\n")))
    col2.metric("Palavras", len(texto.split()))
    col3.metric("Palavras diferentes", len(contagem))

    nuvem = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(contagem)
    figura, eixo = plt.subplots()
    eixo.imshow(nuvem)
    eixo.axis("off")
    st.pyplot(figura)

    st.subheader("Palavras mais frequentes")
    top_palavras = pd.DataFrame(contagem.most_common(10), columns=["Palavra", "Frequência"])
    st.dataframe(top_palavras, hide_index=True)

    st.header("Notícias recentes sobre saneamento")
    noticias = carregar_noticias()
    st.write(f"{len(noticias)} notícias coletadas no Google Notícias.")
    st.dataframe(
        noticias,
        hide_index=True,
        column_config={"link": st.column_config.LinkColumn("Link")},
    )

    st.subheader("Notícias por veículo")
    st.bar_chart(noticias["veiculo"].value_counts().head(10))

# ---------- Aba 4: upload e download de arquivos ----------
with aba_upload:
    st.header("Enviar dados complementares")
    st.write(
        "Envie um CSV com as colunas: País, Ano, Água básica (%), Água segura (%), "
        "Esgoto básico (%) e Esgoto seguro (%). Os dados aparecem na aba Indicadores "
        "e ficam guardados enquanto a sessão estiver aberta."
    )

    with open("data/processed/exemplo_upload_brasil_urbano_rural.csv", encoding="utf-8") as arquivo:
        st.download_button(
            "Baixar arquivo de exemplo (Brasil urbano e rural)",
            arquivo.read(),
            file_name="exemplo_upload_brasil_urbano_rural.csv",
            mime="text/csv",
        )

    st.file_uploader("Escolha um arquivo CSV", type="csv", key="arquivo", on_change=salvar_upload)

    st.subheader("Dados enviados nesta sessão")
    st.dataframe(st.session_state["dados_usuario"], hide_index=True)
    st.button("Limpar dados enviados", on_click=limpar_upload)
