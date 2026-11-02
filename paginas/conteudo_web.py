import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from wordcloud import WordCloud

from dados import carregar_noticias, carregar_texto, contar_palavras

st.title("Conteúdo da web")

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

termo = st.selectbox("Tema da busca", ["Todos"] + sorted(noticias["termo"].unique()))
if termo != "Todos":
    noticias = noticias[noticias["termo"] == termo]

st.write(f"{len(noticias)} notícias coletadas no Google Notícias.")
st.dataframe(
    noticias,
    hide_index=True,
    column_config={"link": st.column_config.LinkColumn("Link")},
)

st.subheader("Notícias por veículo")
st.bar_chart(noticias["veiculo"].value_counts().head(10))
