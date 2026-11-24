# Fase 3 (Modeling): Model Report

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
- Os resultados ainda não foram conferidos manualmente em uma amostra de notícias. Isso fica para a etapa final.

## 9. Plano de uso de LLMs

A tabela mostra qual base atende a cada tipo de tarefa. A classificação de sentimento foi implementada no TP4.

| Tarefa com LLM | Dados usados | Exemplo de uso no painel | Status |
|---|---|---|---|
| Classificação de sentimento | Títulos das notícias (`data/raw/noticias_saneamento.csv`) | Classificar cada notícia como positiva, negativa ou neutra e mostrar a proporção por tema | Implementada no TP4 (`POST /processar_texto`) |
| Resumo de texto | Texto da Wikipedia (`data/raw/wikipedia_saneamento.txt`) | Resumo em 5 frases do que é saneamento básico, para quem não é da área | A fazer |
| Perguntas e respostas | Texto da Wikipedia e indicadores da OMS/UNICEF | O usuário pergunta, por exemplo, "Como está o esgoto no Brasil comparado ao mundo?", e o LLM responde com base só nesses dados | A fazer |
| Geração de texto | Indicadores da OMS/UNICEF, consultados pela rota `GET /indicadores` | Relatório automático sobre a evolução de um país entre 2000 e 2020 e a distância para as metas do Marco Legal do Saneamento | A fazer |

### Como os dados já estão preparados

- Os textos estão em arquivos simples (TXT e CSV), fáceis de enviar a um modelo de linguagem.
- As notícias têm o tema da busca na coluna `termo`, o que permite comparar o sentimento entre os temas.
- A API devolve os indicadores em JSON, um formato que pode ser colocado direto no prompt.
- As funções de leitura ficam em `dados.py`, então uma nova página de IA pode reutilizá-las.
