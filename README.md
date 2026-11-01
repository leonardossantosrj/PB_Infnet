# Painel Saneamento Brasil: ODS 6

Aplicação em Python com Streamlit para acompanhar o acesso à água e ao esgoto no Brasil, alinhada ao **ODS 6 (Água potável e saneamento)** da Agenda 2030 e ao pilar **Ambiental** do ESG.

## Organização do projeto: CRISP-DM e TDSP

O projeto segue as fases do ciclo de vida do **TDSP (Team Data Science Process)**. Montei em cada fase tem uma pasta própria. A tabela mostra a fase equivalente do **CRISP-DM**.

| Fase do TDSP | Fase do CRISP-DM | O que acontece neste projeto | Pasta | Artefato |
|---|---|---|---|---|
| 1. Business Understanding | Business Understanding | Definir o problema, o ODS, as metas e o público-alvo | `1_business_understanding/` | Project Charter |
| 2. Data Acquisition and Understanding | Data Understanding e Data Preparation | Coletar os dados (download, web scraping e APIs), entender e preparar | `2_data_acquisition_and_understanding/` e `data/` | Data Summary Report |
| 3. Modeling | Modeling e Evaluation | Usar um LLM com engenharia de prompts para gerar resumos dos dados | `3_modeling/` | Model Report |
| 4. Deployment | Deployment | Publicar o painel em Streamlit | `4_deployment/` e `app.py` | Dashboard |
| 5. Customer Acceptance | Evaluation (do ponto de vista do negócio) | Validar o painel com usuários e fechar o projeto | `5_customer_acceptance/` | Project Final Report |

## Estrutura de diretórios

```
painel-saneamento-ods6/
├── app.py                                  # aplicação Streamlit
├── requirements.txt                        # bibliotecas necessárias
├── data/
│   └── raw/                                # dados originais
├── 1_business_understanding/
│   └── project_charter.md
├── 2_data_acquisition_and_understanding/
│   └── data_summary_report.md
├── 3_modeling/
├── 4_deployment/
└── 5_customer_acceptance/
```

## Como rodar

1. Crie o ambiente virtual: `python -m venv venv`
2. Ative o ambiente:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
3. Instale as bibliotecas: `pip install -r requirements.txt`
4. Rode a aplicação: `streamlit run app.py`
