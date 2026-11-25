import ollama
import pandas as pd
import streamlit as st

from assistente import MODELO_LLM, responder
from dados import carregar_sentimentos

SENTIMENTOS = ["negativo", "neutro", "positivo"]

st.title("Insights com IA")
st.write(
    "Esta página fecha o ciclo de ciência de dados do projeto: os dados coletados e preparados "
    "nas etapas anteriores passam por modelos de IA que rodam no próprio computador e viram "
    "gráficos e respostas em linguagem simples."
)

# ---------- O ciclo de ciência de dados do projeto ----------
etapa1, etapa2, etapa3, etapa4 = st.columns(4)
etapa1.markdown("**1. Coleta**  \nIndicadores da OMS/UNICEF, Google Notícias e Wikipedia (web scraping)")
etapa2.markdown("**2. Preparação**  \nColunas padronizadas, dados salvos em `data/` e servidos pela API FastAPI")
etapa3.markdown("**3. IA**  \nModelo de sentimento local (TP4) e LLM local com memória (TP5)")
etapa4.markdown("**4. Insights**  \nSentimento das notícias por tema e respostas sobre os indicadores")

# ---------- Resultado do modelo de sentimento ----------
st.header("Sentimento das notícias sobre saneamento")
try:
    noticias = carregar_sentimentos()
except FileNotFoundError:
    noticias = None
    st.info(
        "As notícias ainda não foram classificadas. Com a API ligada, rode no terminal: "
        "python 3_modeling/classificar_noticias.py"
    )

if noticias is not None:
    percentuais = noticias["sentimento"].value_counts(normalize=True).mul(100)
    col1, col2, col3 = st.columns(3)
    col1.metric("Notícias positivas", f"{percentuais.get('positivo', 0):.0f}%")
    col2.metric("Notícias neutras", f"{percentuais.get('neutro', 0):.0f}%")
    col3.metric("Notícias negativas", f"{percentuais.get('negativo', 0):.0f}%")

    # Quantidade de notícias por tema e sentimento (as três colunas sempre existem, mesmo com zero)
    por_tema = pd.crosstab(noticias["termo"], noticias["sentimento"]).reindex(columns=SENTIMENTOS, fill_value=0)
    st.subheader("Notícias por tema da busca")
    st.bar_chart(por_tema, color=["#d62728", "#9e9e9e", "#2ca02c"])

    # Insight automático: o tema com a maior proporção de notícias negativas
    negativas = por_tema["negativo"] / por_tema.sum(axis=1) * 100
    st.write(
        f"O tema com a maior proporção de notícias negativas é **{negativas.idxmax()}** "
        f"({negativas.max():.0f}% das notícias desse tema)."
    )

    filtro = st.selectbox("Ver notícias", ["todas"] + SENTIMENTOS)
    tabela = noticias if filtro == "todas" else noticias[noticias["sentimento"] == filtro]
    st.dataframe(
        tabela[["termo", "titulo", "veiculo", "data", "sentimento", "confianca", "link"]],
        hide_index=True,
        column_config={"link": st.column_config.LinkColumn("link", display_text="abrir")},
    )

# ---------- Assistente com memória conversacional ----------
st.header("Pergunte aos dados")
st.write(
    f"O assistente usa o modelo {MODELO_LLM}, que roda no computador pelo Ollama. Ele responde com base "
    "nos indicadores, nas notícias classificadas e no texto da Wikipedia, e lembra as últimas mensagens "
    'da conversa. Por isso você pode fazer perguntas de continuação, como "e no mundo?".'
)
st.caption(
    "Exemplos: Como está o esgoto no Brasil? · E comparado ao mundo? · "
    "O Brasil vai bater a meta de 2033? · O que as notícias dizem sobre o tema?"
)

if "historico_chat" not in st.session_state:
    st.session_state["historico_chat"] = []

if st.button("Limpar conversa"):
    st.session_state["historico_chat"] = []

for mensagem in st.session_state["historico_chat"]:
    with st.chat_message(mensagem["role"]):
        st.write(mensagem["content"])

pergunta = st.chat_input("Digite sua pergunta sobre água e saneamento")
if pergunta:
    st.session_state["historico_chat"].append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.write(pergunta)

    with st.chat_message("assistant"):
        try:
            with st.spinner("O modelo local está pensando..."):
                resposta = responder(st.session_state["historico_chat"])
        except ConnectionError:
            st.session_state["historico_chat"].pop()  # tira a pergunta sem resposta do histórico
            st.error("O Ollama não está rodando. Abra o aplicativo do Ollama e tente de novo.")
            st.stop()
        except ollama.ResponseError as erro:
            st.session_state["historico_chat"].pop()
            if erro.status_code == 404:
                st.error(f"O modelo {MODELO_LLM} não foi baixado. Rode no terminal: ollama pull {MODELO_LLM}")
            else:
                st.error(f"O Ollama respondeu com erro: {erro.error}")
            st.stop()
        st.write(resposta)

    st.session_state["historico_chat"].append({"role": "assistant", "content": resposta})
