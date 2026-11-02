# Painel Saneamento Brasil: ODS 6

Aplicação em Python com Streamlit para acompanhar o acesso à água e ao esgoto no Brasil, alinhada ao **ODS 6 (Água potável e saneamento)** da Agenda 2030 e ao pilar **Ambiental** do ESG.

## Organização do projeto: CRISP-DM e TDSP

O projeto segue as fases do ciclo de vida do **TDSP (Team Data Science Process)**. Montei em cada fase tem uma pasta própria. A tabela mostra a fase equivalente do **CRISP-DM**.

| Fase do TDSP | Fase do CRISP-DM | O que acontece neste projeto | Pasta | Artefato |
|---|---|---|---|---|
| 1. Business Understanding | Business Understanding | Definir o problema, o ODS, as metas e o público-alvo | `1_business_understanding/` | Project Charter |
| 2. Data Acquisition and Understanding | Data Understanding e Data Preparation | Coletar os dados (download, web scraping e APIs), entender e preparar | `2_data_acquisition_and_understanding/` e `data/` | Data Summary Report |
| 3. Modeling | Modeling e Evaluation | Usar um LLM com engenharia de prompts para resumos, sentimento, perguntas e respostas e relatórios (plano em `3_modeling/README.md`) | `3_modeling/` | Model Report |
| 4. Deployment | Deployment | Publicar o painel em Streamlit e a API em FastAPI | `4_deployment/`, `app.py`, `paginas/` e `api.py` | Dashboard e API |
| 5. Customer Acceptance | Evaluation (do ponto de vista do negócio) | Validar o painel com usuários e fechar o projeto | `5_customer_acceptance/` | Project Final Report |

## Estrutura de diretórios

```
painel-saneamento-ods6/
├── app.py                                  # menu de navegação do app Streamlit
├── paginas/                                # uma página do app por arquivo
│   ├── sobre.py
│   ├── indicadores.py
│   ├── conteudo_web.py
│   ├── enviar_dados.py
│   └── integracao_api.py
├── dados.py                                # funções de leitura usadas por todas as páginas
├── api.py                                  # API FastAPI
├── requirements.txt                        # bibliotecas necessárias
├── .gitignore                              # arquivos que o Git ignora (venv, __pycache__)
├── data/
│   ├── raw/                                # dados originais e dados extraídos da web
│   └── processed/                          # arquivo de exemplo para upload e dados enviados pela API
├── 1_business_understanding/
│   └── project_charter.md
├── 2_data_acquisition_and_understanding/
│   ├── data_summary_report.md
│   ├── scraping_wikipedia.py
│   └── scraping_noticias.py
├── 3_modeling/
│   └── README.md                           # plano de uso de LLMs
├── 4_deployment/
└── 5_customer_acceptance/
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
| Conteúdo da web | Nuvem de palavras da Wikipedia, palavras mais frequentes e notícias com filtro por tema |
| Enviar dados | Upload de CSV com dados complementares, que aparecem na página Indicadores |
| API | Consulta e envio de indicadores usando a API FastAPI |

## Como rodar o app e a API

A página API do app depende da API rodando. Use dois terminais, ambos na raiz do projeto e com a venv ativa.

1. No terminal 1, suba a API:
   ```
   uvicorn api:app --reload
   ```
2. No terminal 2, suba o app:
   ```
   streamlit run app.py
   ```

## API

Documentação automática (Swagger), com a API rodando: http://127.0.0.1:8000/docs

| Método | Rota | Função |
|---|---|---|
| GET | `/indicadores?pais=Brazil` | Consulta os indicadores de água e esgoto de um país ou região, ano a ano. O nome do país é em inglês, como no arquivo da OMS/UNICEF. Também traz os registros enviados pela rota POST. |
| POST | `/indicadores` | Envia um novo registro de indicadores, por exemplo de um estado ou município. O registro é salvo em `data/processed/indicadores_api.csv`. Os percentuais devem estar entre 0 e 100. |

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
