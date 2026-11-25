# Fase 3 (Modeling): Model Report

O projeto usa dois modelos de IA, os dois rodando no próprio computador:

| Modelo | Tipo | Para que serve | Etapa | Seções |
|---|---|---|---|---|
| `cardiffnlp/twitter-xlm-roberta-base-sentiment` | BERT, classificação | Classificar o sentimento das notícias | TP4 | 1 a 8 |
| `qwen3:4b`, pelo Ollama | LLM generativo (tipo GPT) | Assistente que responde perguntas sobre os dados e lembra a conversa | TP5 | 10 a 16 |

## 1. Tarefa escolhida

No TP3, o plano de uso de LLMs (seção 6) definiu quatro tarefas. A primeira a ser implementada é a **classificação de sentimento das notícias** coletadas do Google Notícias. Ela responde a uma pergunta do público-alvo: as notícias sobre saneamento estão trazendo avanços, problemas ou só informação?

A rota `POST /processar_texto` da API recebe um texto, como o título de uma notícia, e devolve se ele é **positivo, neutro ou negativo**, com o grau de confiança do modelo.

## 2. Modelo escolhido

**`cardiffnlp/twitter-xlm-roberta-base-sentiment`**, da HuggingFace: https://huggingface.co/cardiffnlp/twitter-xlm-roberta-base-sentiment

É um modelo do tipo **BERT** (arquitetura XLM-RoBERTa base), treinado em cerca de 198 milhões de tweets em vários idiomas e depois ajustado para análise de sentimento em 8 idiomas, entre eles o **português**. Ele foi apresentado no artigo *XLM-T: Multilingual Language Models in Twitter for Sentiment Analysis and Beyond* (Barbieri, Espinosa Anke e Camacho-Collados, LREC 2022).

## 3. Critérios de seleção

| Critério | Como o modelo atende |
|---|---|
| **Desempenho: tipo de tarefa** | Foi treinado especificamente para classificar sentimento em 3 classes (positivo, neutro e negativo), que é a tarefa planejada. Modelos generativos, como GPT ou T5, precisariam de um prompt e devolveriam texto livre, que é mais difícil de validar. |
| **Desempenho: idioma e tipo de texto** | O português está entre os 8 idiomas do ajuste. O modelo foi treinado com textos curtos (tweets), parecidos com os títulos de notícias que vamos analisar. |
| **Desempenho: capacidade de resposta** | É um modelo de tamanho base, então responde rápido mesmo na CPU. O modelo é carregado uma única vez, quando a API sobe, e não a cada chamada. |
| **Custo computacional local** | Cerca de 280 milhões de parâmetros. O download tem cerca de 1,1 GB, e o modelo usa entre 1,5 e 2 GB de memória RAM. Não precisa de GPU: roda em um notebook comum. |
| **Acessibilidade local** | Carrega com a função `pipeline` da biblioteca Transformers. É baixado uma vez da HuggingFace e depois roda sem internet. É um dos modelos de sentimento mais usados da plataforma, com cerca de 600 mil downloads por mês. |

## 4. Outros modelos avaliados

| Modelo | Tipo | Por que não foi escolhido |
|---|---|---|
| `lxyuan/distilbert-base-multilingual-cased-sentiments-student` | BERT (DistilBERT), sentimento | É menor e mais rápido, mas a página do modelo não cita o português entre os idiomas avaliados. |
| `tabularisai/multilingual-sentiment-analysis` | BERT, sentimento em 5 classes | Foi treinado com dados sintéticos e tem licença não comercial. |
| `Qwen/Qwen2.5-0.5B-Instruct` | GPT (generativo) | Consegue fazer várias tarefas com prompts, mas a resposta é texto livre, que pode variar de uma execução para outra. Para classificar sentimento, um modelo treinado só para isso é mais simples e mais consistente. |

## 5. Requisitos de hardware e software

- **Memória RAM:** pelo menos 4 GB livres (o modelo usa entre 1,5 e 2 GB).
- **Disco:** cerca de 1,1 GB para o modelo, guardado no cache da HuggingFace (`~/.cache/huggingface`).
- **Bibliotecas:** `transformers`, `torch`, `sentencepiece` e `protobuf` (versões no `requirements.txt`). O `sentencepiece` e o `protobuf` são usados pelo tokenizador do modelo.
- **Versão do Transformers:** fixada na 4.57.6, a última da série 4.

## 6. Como a integração local funciona

1. Quando a API sobe (`python -m uvicorn api:app --reload`), o `api.py` carrega o modelo **uma única vez** com:
   ```python
   classificador = pipeline("text-classification", model=NOME_MODELO, tokenizer=NOME_MODELO)
   ```
2. Na primeira execução, a Transformers baixa o modelo da HuggingFace. Nas próximas, usa a cópia do cache, sem internet.
3. Se o carregamento falhar (sem internet na primeira vez, falta de memória ou biblioteca faltando), a API sobe mesmo assim. As rotas de indicadores continuam funcionando, e a rota `/processar_texto` responde com erro 503, explicando o motivo.
4. A cada chamada de `POST /processar_texto`, o texto passa pelo modelo, e a API traduz o rótulo para o português (`Positive` vira `positivo`) e arredonda a confiança.
5. A resposta é validada pelo Response Model `RespostaProcessamento`, que garante sempre o mesmo formato:
   ```json
   {
     "texto": "Investimento em saneamento cresce 51% após Marco Legal",
     "tipo_analise": "classificação de sentimento",
     "modelo": "cardiffnlp/twitter-xlm-roberta-base-sentiment",
     "resultado": {"sentimento": "positivo", "confianca": 0.9123}
   }
   ```
6. A página **API** do app Streamlit permite escolher uma notícia coletada, editar o texto e ver o resultado.

## 7. Tratamento de erros da rota

| Código | Quando acontece | Mensagem |
|---|---|---|
| 400 | O texto tem só espaços | "O texto não pode conter apenas espaços." |
| 422 | O texto tem menos de 3 ou mais de 2.000 caracteres, ou o campo `texto` não foi enviado | "Dados de entrada inválidos. Confira os campos abaixo.", com a lista de campos com problema |
| 500 | O modelo falhou ao processar o texto | "Erro ao processar o texto no modelo: ..." |
| 503 | O modelo não foi carregado quando a API subiu | "O modelo de linguagem não está disponível. Motivo: ..." |

No app, se a API estiver desligada ou demorar mais de 60 segundos, a página mostra uma mensagem explicando o que fazer, em vez de um erro do Python.

## 8. Limitações

- O modelo foi treinado com tweets, e não com notícias. Títulos muito técnicos tendem a ser classificados como **neutros**.
- Ele analisa só o título, porque o feed do Google Notícias não traz o texto completo da notícia.
- Textos longos são cortados no limite do modelo (512 tokens), com `truncation=True`.
- Os resultados ainda não foram conferidos manualmente em uma amostra de notícias. A conferência está no [Project Final Report](../5_customer_acceptance/README.md).

## 9. Plano de uso de LLMs

A tabela mostra qual base atende a cada tipo de tarefa. A classificação de sentimento foi implementada no TP4, e as outras três tarefas são atendidas pelo assistente do TP5.

| Tarefa com LLM | Dados usados | Exemplo de uso no painel | Status |
|---|---|---|---|
| Classificação de sentimento | Títulos das notícias (`data/raw/noticias_saneamento.csv`) | Classificar cada notícia como positiva, negativa ou neutra e mostrar a proporção por tema | Implementada no TP4 (`POST /processar_texto`) e aplicada a todas as notícias no TP5 |
| Resumo de texto | Texto da Wikipedia (`data/raw/wikipedia_saneamento.txt`) | Resumo em 5 frases do que é saneamento básico, para quem não é da área | Atendida pelo assistente do TP5: o trecho da Wikipedia está no prompt, e o usuário pode pedir um resumo |
| Perguntas e respostas | Texto da Wikipedia e indicadores da OMS/UNICEF | O usuário pergunta, por exemplo, "Como está o esgoto no Brasil comparado ao mundo?", e o LLM responde com base só nesses dados | Implementada no TP5 (assistente com memória) |
| Geração de texto | Indicadores da OMS/UNICEF, consultados pela rota `GET /indicadores` | Relatório automático sobre a evolução de um país entre 2000 e 2020 e a distância para as metas do Marco Legal do Saneamento | Atendida pelo assistente do TP5, com os dados de 2000, 2010 e 2020 que estão no prompt |

### Como os dados foram preparados

- Os textos estão em arquivos simples (TXT e CSV), fáceis de enviar a um modelo de linguagem.
- As notícias têm o tema da busca na coluna `termo`, o que permite comparar o sentimento entre os temas.
- A API devolve os indicadores em JSON, um formato que pode ser colocado direto no prompt.
- As funções de leitura ficam em `dados.py`, então uma nova página de IA pode reutilizá-las.

## 10. TP5: tarefa escolhida

Entre os caminhos do TP5, foi escolhida a **memória conversacional**. O problema do projeto é que os dados de saneamento existem, mas são difíceis de interpretar. Um assistente que conversa, explica em linguagem simples e lembra o que já foi dito permite que o usuário vá aprofundando o assunto sem repetir o contexto. Por exemplo: "Como está o esgoto no Brasil?", depois "E no mundo?" e depois "Vamos bater a meta de 2033?".

O assistente fica na página **Insights com IA**, junto com os gráficos do sentimento das notícias.

## 11. TP5: modelo escolhido

**`qwen3:4b`**, da família Qwen3, rodando pelo **Ollama**: https://ollama.com/library/qwen3:4b

É um LLM generativo, do mesmo tipo do GPT, com cerca de 4 bilhões de parâmetros. O Ollama é um programa que baixa e roda LLMs no próprio computador e oferece uma biblioteca Python (`ollama`) para conversar com eles.

| Critério | Como o modelo atende |
|---|---|
| **Desempenho: tipo de tarefa** | É um modelo de conversa (instruções e chat), que entende um prompt de sistema com regras e responde em texto livre. |
| **Desempenho: idioma** | Suporta mais de 100 idiomas e dialetos, segundo a página do modelo. |
| **Desempenho: capacidade de resposta** | Tem um modo de raciocínio que pode ser desligado (`think=False`). Desligado, responde mais rápido, o que basta para explicar dados que já estão no prompt. |
| **Custo computacional local** | Download de 2,5 GB (versão quantizada Q4_K_M). Roda na CPU ou no chip da Apple, sem GPU dedicada, com pelo menos 8 GB de RAM no computador. |
| **Acessibilidade local** | Instala com o Ollama e baixa com um comando (`ollama pull qwen3:4b`). Depois funciona sem internet e é gratuito. |

### Outras opções avaliadas

| Opção | Por que não foi escolhida |
|---|---|
| Gemini, pela API do Google | Testado em outro projeto com a mesma conta: a API recusou com erro 403 ("free tier is not available for this project"). Além disso, envia os dados para a nuvem. |
| GPT, pela API da OpenAI | É pago por uso e também depende da nuvem. |
| Modelos maiores, como `qwen3:8b` | Respondem melhor, mas o download é de cerca de 5 GB e eles são mais lentos sem GPU. |
| Modelos de 1 bilhão de parâmetros ou menos | São mais leves, mas seguem pior as regras do prompt e erram mais os números. |

## 12. TP5: engenharia de prompts

O prompt de sistema fica no `assistente.py` (constante `PROMPT_SISTEMA`) e é montado a cada pergunta pela função `montar_contexto()`. As técnicas usadas:

| Técnica | Como aparece no prompt | Por que foi usada |
|---|---|---|
| **Papel (persona)** | "Você é o assistente do Painel Saneamento Brasil, especializado no ODS 6", com o público definido | Ajusta o tom e o nível de explicação para quem não é da área |
| **Contexto com os dados do projeto** | Indicadores de Brasil, América Latina e mundo em 2000, 2010 e 2020; resumo do sentimento das notícias por tema e exemplos; trecho da Wikipedia | O modelo responde com os dados oficiais coletados, e não com o que aprendeu no treino, que pode estar desatualizado |
| **Regras explícitas** | Responder só com os dados, dizer quando um dado não existe, citar ano e fonte | Reduz respostas inventadas e deixa as respostas verificáveis |
| **Formato da resposta** | Português do Brasil, linguagem simples, no máximo 3 parágrafos curtos | Respostas curtas e fáceis de ler no painel |
| **Glossário e metas** | Definição de água e esgoto "básico" e "seguro" e as metas do Marco Legal para 2033 | Evita confusão entre os indicadores e permite comparar com as metas |
| **Temperatura baixa (0,2)** | Parâmetro `temperature` na chamada ao modelo | Respostas mais fiéis aos dados e menos criativas |

O prompt montado tem cerca de 6 mil caracteres. Os dados entram em CSV, um formato curto e que o modelo entende bem.

## 13. TP5: como funciona a memória conversacional

1. A página guarda a conversa em `st.session_state["historico_chat"]`, uma lista de mensagens no formato `{"role": "user" ou "assistant", "content": texto}`.
2. A cada pergunta, a função `responder()` envia ao modelo o prompt de sistema e as **últimas 10 mensagens** da conversa (janela de memória).
3. Como o modelo recebe as perguntas e respostas anteriores, ele entende perguntas de continuação, como "e no mundo?".
4. A janela de 10 mensagens mantém o contexto recente sem ultrapassar o limite de texto que o modelo aceita (`num_ctx` de 8.192 tokens).
5. O botão **Limpar conversa** apaga o histórico e começa uma conversa nova.

```
pergunta do usuário ─> historico_chat ─> [prompt de sistema com os dados] + [últimas 10 mensagens] ─> qwen3:4b ─> resposta
                            ↑                                                                                    │
                            └────────────────────────── a resposta também entra no histórico ────────────────────┘
```

## 14. TP5: sentimento de todas as notícias

O script `3_modeling/classificar_noticias.py` envia cada título coletado para a rota `POST /processar_texto` da API (TP4) e salva o resultado em `data/processed/noticias_sentimento.csv`. A classificação roda uma vez, e não a cada abertura da página, porque são mais de 200 notícias. O arquivo gerado alimenta:

- os indicadores de percentual de notícias positivas, neutras e negativas;
- o gráfico de notícias por tema e sentimento e o insight do tema com mais notícias negativas;
- o resumo de sentimento que vai no prompt do assistente.

## 15. TP5: tratamento de erros

| Situação | O que acontece |
|---|---|
| API desligada ao rodar o script de classificação | O script para com a mensagem "A API não está rodando..." e o comando para subir a API |
| API responde com erro (por exemplo, 503 do modelo de sentimento) | O script para e mostra o código e a mensagem da API |
| Notícias ainda não classificadas | A página mostra como rodar o script, e o assistente é avisado no prompt de que a análise ainda não foi feita |
| Ollama desligado | A página mostra "O Ollama não está rodando...", e a pergunta sem resposta sai do histórico |
| Modelo `qwen3:4b` não baixado | A página mostra o comando `ollama pull qwen3:4b` |

## 16. TP5: limitações

- O assistente conhece só os dados que estão no prompt: Brasil, América Latina e mundo em 2000, 2010 e 2020. Perguntas sobre outros países ou anos ficam sem resposta, e ele deve dizer que o painel não tem o dado.
- Modelos pequenos podem errar ao fazer contas, como diferenças entre percentuais. Os números citados devem ser conferidos na página Indicadores.
- A memória dura só enquanto a aba do navegador estiver aberta.
- O sentimento é calculado só a partir do título das notícias, que é o que o feed do Google Notícias oferece.
