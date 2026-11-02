import pandas as pd
import streamlit as st


def salvar_upload():
    # Roda assim que um arquivo é enviado, antes do resto da página ser recarregado
    if st.session_state["arquivo"] is not None:
        st.session_state["dados_usuario"] = pd.read_csv(st.session_state["arquivo"])


def limpar_upload():
    st.session_state["dados_usuario"] = pd.DataFrame()


st.title("Enviar dados complementares")
st.write(
    "Envie um CSV com as colunas: País, Ano, Água básica (%), Água segura (%), "
    "Esgoto básico (%) e Esgoto seguro (%). Os dados aparecem na página Indicadores "
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
