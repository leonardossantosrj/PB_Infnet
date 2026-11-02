# Extrai notícias sobre saneamento do Google Notícias e salva em CSV.

import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://news.google.com/rss/search"

# Três buscas para cobrir os principais temas do ODS 6
termos = ["saneamento básico", "água potável", "tratamento de esgoto"]

noticias = []
for termo in termos:
    parametros = {"q": termo, "hl": "pt-BR", "gl": "BR", "ceid": "BR:pt-419"}
    resposta = requests.get(url, params=parametros)

    # O Google Notícias entrega as notícias em formato RSS (XML), por isso o parser "xml"
    soup = BeautifulSoup(resposta.content, "xml")

    for item in soup.find_all("item"):
        veiculo = item.source.text
        noticias.append(
            {
                "termo": termo,
                "titulo": item.title.text.replace(" - " + veiculo, ""),
                "veiculo": veiculo,
                "data": pd.to_datetime(item.pubDate.text).date(),
                "link": item.link.text,
            }
        )

# Uma mesma notícia pode aparecer em mais de uma busca: fica só a primeira
tabela = pd.DataFrame(noticias).drop_duplicates(subset="link")
tabela.to_csv("data/raw/noticias_saneamento.csv", index=False)

print(f"{len(tabela)} notícias salvas em data/raw/noticias_saneamento.csv")
