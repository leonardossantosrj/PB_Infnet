# Extrai o texto do artigo "Saneamento básico" da Wikipedia e salva em TXT.

import requests
from bs4 import BeautifulSoup

url = "https://pt.wikipedia.org/wiki/Saneamento_b%C3%A1sico"

# A Wikipedia pede que todo acesso automático se identifique
cabecalho = {"User-Agent": "painel-saneamento-ods6/1.0 (projeto academico)"}

resposta = requests.get(url, headers=cabecalho)
soup = BeautifulSoup(resposta.text, "html.parser")

# O texto do artigo fica dentro da div com id "mw-content-text"
conteudo = soup.find(id="mw-content-text")

paragrafos = []
for p in conteudo.find_all("p"):
    texto = p.get_text().strip()
    if texto != "":
        paragrafos.append(texto)

with open("data/raw/wikipedia_saneamento.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write("\n".join(paragrafos))

print(f"{len(paragrafos)} parágrafos salvos em data/raw/wikipedia_saneamento.txt")
