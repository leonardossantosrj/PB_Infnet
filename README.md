# Painel Saneamento Brasil: ODS 6

Aplicação em Python com Streamlit para acompanhar o acesso à água e ao esgoto no Brasil, alinhada ao **ODS 6 (Água potável e saneamento)** da Agenda 2030 e ao pilar **Ambiental** do ESG.

## Organização do projeto: CRISP-DM e TDSP

O projeto segue as fases do ciclo de vida do **TDSP (Team Data Science Process)**. Montei em cada fase tem uma pasta própria. A tabela mostra a fase equivalente do **CRISP-DM**.

| Fase do TDSP | Fase do CRISP-DM | O que acontece neste projeto | Pasta | Artefato |
|---|---|---|---|---|
| 1. Business Understanding | Business Understanding | Definir o problema, o ODS, as metas e o público-alvo | `1_business_understanding/` | Project Charter |
| 2. Data Acquisition and Understanding | Data Understanding e Data Preparation | Coletar os dados (download, web scraping e APIs), entender e preparar | `2_data_acquisition_and_understanding/` e `data/` | Data Summary Report |
| 3. Modeling | Modeling e Evaluation | Classificar o sentimento das notícias com um modelo local (TP4) e criar um assistente com LLM local e memória conversacional (TP5) | `3_modeling/` e `assistente.py` | Model Report |
| 4. Deployment | Deployment | Rodar o painel em Streamlit, a API em FastAPI e os modelos de IA no computador | `4_deployment/`, `app.py`, `paginas/` e `api.py` | Dashboard, API e guia de deployment |
| 5. Customer Acceptance | Evaluation (do ponto de vista do negócio) | Testar a solução com casos reais, apresentar os resultados e fechar o projeto | `5_customer_acceptance/` | Project Final Report |

## Estrutura de diretórios

```
painel-saneamento-ods6/
├── app.py                                  # menu de navegação do app Streamlit
├── paginas/                                # uma página do app por arquivo
│   ├── sobre.py
│   ├── indicadores.py
│   ├── insights_ia.py                      # gráficos de sentimento e assistente com memória
│   ├── conteudo_web.py
│   ├── enviar_dados.py
│   └── integracao_api.py
├── dados.py                                # funções de leitura usadas por todas as páginas
├── assistente.py                           # LLM local (Ollama): prompt com os dados e memória
├── api.py                                  # API FastAPI
├── requirements.txt                        # bibliotecas necessárias
├── .gitignore                              # arquivos que o Git ignora (venv, __pycache__)
├── data/
│   ├── raw/                                # dados originais e dados extraídos da web
│   └── processed/                          # exemplo para upload, dados enviados pela API e notícias com sentimento
├── 1_business_understanding/
│   └── project_charter.md
├── 2_data_acquisition_and_understanding/
│   ├── data_summary_report.md
│   ├── scraping_wikipedia.py
│   └── scraping_noticias.py
├── 3_modeling/
│   ├── README.md                           # Model Report: modelos de IA, prompt e memória
│   └── classificar_noticias.py             # classifica o sentimento de todas as notícias
├── 4_deployment/
│   └── README.md                           # guia de deployment
└── 5_customer_acceptance/
    └── README.md                           # Project Final Report
```

## Coleta de dados da web

Os scripts de web scraping rodam separados do app. Execute na raiz do projeto, antes de abrir o app:

```
python 2_data_acquisition_and_understanding/scraping_wikipedia.py
python 2_data_acquisition_and_understanding/scraping_noticias.py
```

## Páginas do app

| Página | O que faz |
|---|---|
| Sobre o projeto | Problema de negócio, objetivos, links e amostra dos dados |
| Indicadores | Filtros de país, indicador e período, gráfico, tabela e download em CSV |
| Insights com IA | Ciclo de ciência de dados do projeto, gráficos do sentimento das notícias por tema e assistente que responde perguntas sobre os dados e lembra a conversa |
| Conteúdo da web | Nuvem de palavras da Wikipedia, palavras mais frequentes e notícias com filtro por tema |
| Enviar dados | Upload de CSV com dados complementares, que aparecem na página Indicadores |
| API | Análise de sentimento de notícias com o modelo local e consulta e envio de indicadores usando a API FastAPI |

## Como rodar o app e a API

A página API do app depende da API rodando, e o assistente da página Insights com IA depende do Ollama. Use dois terminais, ambos na raiz do projeto e com a venv ativa. O passo a passo completo está no [guia de deployment](4_deployment/README.md).

1. Instale as bibliotecas (só na primeira vez):
   ```
   python -m pip install -r requirements.txt
   ```
2. No terminal 1, suba a API:
   ```
   python -m uvicorn api:app --reload
   ```
   Na primeira vez, a API baixa o modelo de linguagem da HuggingFace (cerca de 1,1 GB), então precisa de internet e pode levar alguns minutos. Depois, o modelo fica salvo no computador e a API sobe sem internet.
3. Instale o Ollama (https://ollama.com/download) e baixe o modelo do assistente (só na primeira vez, cerca de 2,5 GB):
   ```
   ollama pull qwen3:4b
   ```
4. Com a API ligada, classifique o sentimento das notícias (repita sempre que coletar notícias novas):
   ```
   python 3_modeling/classificar_noticias.py
   ```
5. No terminal 2, suba o app:
   ```
   python -m streamlit run app.py
   ```

## Inteligência artificial no projeto

| Modelo | Onde roda | O que faz no painel |
|---|---|---|
| `cardiffnlp/twitter-xlm-roberta-base-sentiment` (Transformers) | Na API, rota `POST /processar_texto` | Classifica o sentimento das notícias. O resultado aparece nos gráficos da página Insights com IA |
| `qwen3:4b` (Ollama) | No app, pelo `assistente.py` | Responde perguntas sobre os indicadores, as notícias e o texto da Wikipedia em linguagem simples e lembra as últimas mensagens da conversa |

A escolha dos modelos, o prompt e o funcionamento da memória estão no [Model Report](3_modeling/README.md). Os testes e os resultados estão no [Project Final Report](5_customer_acceptance/README.md).

## API

Documentação automática (Swagger), com a API rodando: http://127.0.0.1:8000/docs

| Método | Rota | Função |
|---|---|---|
| GET | `/indicadores?pais=Brazil` | Consulta os indicadores de água e esgoto de um país ou região, ano a ano. O nome do país é em inglês, como no arquivo da OMS/UNICEF. Também traz os registros enviados pela rota POST. |
| POST | `/indicadores` | Envia um novo registro de indicadores, por exemplo de um estado ou município. O registro é salvo em `data/processed/indicadores_api.csv`. Os percentuais devem estar entre 0 e 100. |
| POST | `/processar_texto` | Classifica o sentimento de um texto (positivo, neutro ou negativo) com um modelo de linguagem que roda localmente. A escolha do modelo está no [Model Report](3_modeling/README.md). |

**Exemplo de consulta:**
```
curl "http://127.0.0.1:8000/indicadores?pais=Brazil"
```

**Exemplo de envio:**
```
curl -X POST "http://127.0.0.1:8000/indicadores" \
  -H "Content-Type: application/json" \
  -d '{"pais": "Rio de Janeiro", "ano": 2024, "agua_basica": 97.5, "agua_segura": 90.1, "esgoto_basico": 85.0, "esgoto_seguro": 60.2}'
```

**Exemplo de análise de sentimento:**
```
curl -X POST "http://127.0.0.1:8000/processar_texto" \
  -H "Content-Type: application/json" \
  -d '{"texto": "Investimento em saneamento cresce 51% após Marco Legal"}'
```

Resposta:
```json
{
  "texto": "Investimento em saneamento cresce 51% após Marco Legal",
  "tipo_analise": "classificação de sentimento",
  "modelo": "cardiffnlp/twitter-xlm-roberta-base-sentiment",
  "resultado": {"sentimento": "positivo", "confianca": 0.9123}
}
```

### Respostas e erros

Todas as rotas usam Response Models do Pydantic, então as respostas têm sempre o mesmo formato, que aparece na documentação em `/docs`. Quando algo dá errado, a API responde com um código HTTP e uma mensagem explicando o problema:

| Código | Significado | Exemplo |
|---|---|---|
| 400 | Requisição com problema | Texto com só espaços em `/processar_texto` |
| 404 | Não encontrado | País sem dados em `GET /indicadores`, como "Brasil" em vez de "Brazil" |
| 422 | Dados de entrada inválidos | Percentual acima de 100 ou texto com menos de 3 caracteres. A resposta lista os campos com problema |
| 500 | Erro interno | O modelo falhou ao processar o texto |
| 503 | Serviço indisponível | O modelo de linguagem não carregou ou o arquivo de dados não foi encontrado |
