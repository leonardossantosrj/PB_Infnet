import pandas as pd
import streamlit as st

st.set_page_config(page_title="Painel Saneamento Brasil", layout="wide")

# Estado de sessão: criado aqui para valer em todas as páginas
if "dados_usuario" not in st.session_state:
    st.session_state["dados_usuario"] = pd.DataFrame()

# Menu de navegação: cada página é um arquivo da pasta paginas/
menu = st.navigation(
    [
        st.Page("paginas/sobre.py", title="Sobre o projeto", default=True),
        st.Page("paginas/indicadores.py", title="Indicadores"),
        st.Page("paginas/conteudo_web.py", title="Conteúdo da web"),
        st.Page("paginas/enviar_dados.py", title="Enviar dados"),
        st.Page("paginas/integracao_api.py", title="API"),
    ]
)
menu.run()
