import pandas as pd
import streamlit as st

from dados import INDICADORES, carregar_indicadores

st.title("Indicadores de água e esgoto")

# Junta os dados oficiais com os dados enviados pelo usuário na página "Enviar dados"
indicadores = pd.concat([carregar_indicadores(), st.session_state["dados_usuario"]])

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
grafico.index = grafico.index.astype(str)
st.line_chart(grafico)

st.dataframe(filtrado, hide_index=True)
st.download_button(
    "Baixar dados filtrados (CSV)",
    filtrado.to_csv(index=False),
    file_name="indicadores_filtrados.csv",
    mime="text/csv",
)
