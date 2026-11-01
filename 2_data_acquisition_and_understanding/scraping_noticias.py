# Extrai notícias sobre saneamento básico do Google Notícias e salva em CSV.

import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://news.google.com/rss/search?q=saneamento+b%C3%A1sico&hl=pt-BR&gl=BR&ceid=BR:pt-419"

resposta = requests.get(url)

# O Google Notícias entrega as notícias em formato RSS (XML), por isso o parser "xml"
soup = BeautifulSoup(resposta.content, "xml")

noticias = []
for item in soup.find_all("item"):
    veiculo = item.source.text
    noticias.append(
        {
            "titulo": item.title.text.replace(" - " + veiculo, ""),
            "veiculo": veiculo,
            "data": pd.to_datetime(item.pubDate.text).date(),
            "link": item.link.text,
        }
    )

pd.DataFrame(noticias).to_csv("data/raw/noticias_saneamento.csv", index=False)

print(f"{len(noticias)} notícias salvas em data/raw/noticias_saneamento.csv")
