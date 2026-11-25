# Assistente do painel: um LLM local (Ollama) que responde perguntas sobre os dados do projeto
# e lembra a conversa (memória conversacional).

import re

import ollama
import pandas as pd

from dados import carregar_indicadores, carregar_sentimentos, carregar_texto

MODELO_LLM = "qwen3:4b"
JANELA_MEMORIA = 10  # o modelo recebe as últimas 10 mensagens (5 perguntas e 5 respostas)
REGIOES = {"Brazil": "Brasil", "Latin America and the Caribbean": "América Latina e Caribe", "World": "Mundo"}

# Engenharia de prompts: papel, regras, glossário e os dados do projeto como contexto.
PROMPT_SISTEMA = """Você é o assistente do Painel Saneamento Brasil, especializado no ODS 6 (água potável e saneamento).
Seu público são gestores públicos, ONGs e cidadãos sem formação técnica.

Regras:
1. Responda usando apenas os dados abaixo. Se a informação não estiver neles, diga que o painel não tem esse dado.
2. Ao citar um número, informe o ano e a fonte (OMS/UNICEF, notícias coletadas ou Wikipedia).
3. Explique em linguagem simples, em português do Brasil, em no máximo 3 parágrafos curtos.
4. Quando fizer sentido, compare o Brasil com a América Latina, com o mundo e com as metas do Marco Legal.
5. Use o histórico da conversa para entender perguntas de continuação, como "e no mundo?".

Glossário dos indicadores (OMS/UNICEF):
- Água básica: fonte de água melhorada a até 30 minutos de distância, ida e volta.
- Água segura: fonte melhorada no próprio domicílio, disponível quando necessário e livre de contaminação.
- Esgoto básico: banheiro ou instalação sanitária melhorada, não compartilhada com outros domicílios.
- Esgoto seguro: instalação básica em que os dejetos são tratados e descartados com segurança.

Metas do Marco Legal do Saneamento (Lei 14.026/2020), até 2033: 99% da população com água potável
e 90% com coleta e tratamento de esgoto.

=== Indicadores da OMS/UNICEF (% da população; os dados mais recentes são de 2020) ===
{indicadores}

=== Sentimento das notícias sobre saneamento coletadas no Google Notícias ===
Classificação feita pelo modelo de IA local do projeto (cardiffnlp/twitter-xlm-roberta-base-sentiment).
Quantidade de notícias por tema da busca e sentimento:
{sentimento}
Exemplos de notícias:
{exemplos}

=== Trecho da Wikipedia sobre saneamento ===
{wikipedia}
"""


def montar_contexto():
    """Monta o prompt de sistema com os dados coletados e processados no projeto."""
    indicadores = carregar_indicadores()
    tabela = indicadores[indicadores["País"].isin(REGIOES) & indicadores["Ano"].isin([2000, 2010, 2020])]
    tabela = tabela.replace({"País": REGIOES})

    try:
        noticias = carregar_sentimentos()
        sentimento = pd.crosstab(noticias["termo"], noticias["sentimento"]).to_csv()
        # As 5 notícias de maior confiança de cada sentimento
        melhores = noticias.sort_values("confianca", ascending=False).groupby("sentimento").head(5)
        exemplos = "\n".join(f"- [{n.sentimento}] {n.titulo} ({n.veiculo}, {n.data})" for n in melhores.itertuples())
    except FileNotFoundError:
        sentimento = "A análise de sentimento das notícias ainda não foi feita."
        exemplos = "-"

    wikipedia = re.sub(r"\[\d+\]", "", carregar_texto())[:2000]  # tira as marcas de referência, como [1]

    return PROMPT_SISTEMA.format(
        indicadores=tabela.to_csv(index=False),
        sentimento=sentimento,
        exemplos=exemplos,
        wikipedia=wikipedia,
    )


def responder(historico):
    """Envia o prompt de sistema e as últimas mensagens da conversa ao LLM e devolve a resposta."""
    mensagens = [{"role": "system", "content": montar_contexto()}] + historico[-JANELA_MEMORIA:]
    resposta = ollama.chat(
        model=MODELO_LLM,
        messages=mensagens,
        think=False,  # desliga o modo de raciocínio do Qwen3, para responder mais rápido
        options={"temperature": 0.2, "num_ctx": 8192},  # temperatura baixa: respostas mais fiéis aos dados
    )
    return resposta.message.content
