# Fase 4 (Deployment): guia de deployment

O painel roda no computador do usuário, com todos os modelos de IA locais. Este guia mostra os componentes, a ordem de execução e como resolver os problemas mais comuns.

## 1. Componentes

| Componente | Arquivo | Função | Como roda |
|---|---|---|---|
| Painel | `app.py` e `paginas/` | Interface com as páginas do projeto | `python -m streamlit run app.py` |
| API | `api.py` | Consulta e envio de indicadores e análise de sentimento | `python -m uvicorn api:app --reload` |
| Modelo de sentimento | Carregado pelo `api.py` | Classifica o sentimento de textos | Baixado da HuggingFace na primeira vez que a API sobe |
| LLM do assistente | `assistente.py` | Responde perguntas sobre os dados com memória | Aplicativo Ollama com o modelo `qwen3:4b` |
| Coleta | `2_data_acquisition_and_understanding/scraping_*.py` | Web scraping da Wikipedia e do Google Notícias | Rodados à mão, quando for preciso atualizar os dados |
| Classificação das notícias | `3_modeling/classificar_noticias.py` | Gera `data/processed/noticias_sentimento.csv` | Rodado à mão, com a API ligada, depois de cada coleta de notícias |

## 2. Requisitos

- Python 3.11 ou mais novo.
- Pelo menos 8 GB de RAM e cerca de 4 GB livres em disco para os dois modelos (1,1 GB do modelo de sentimento e 2,5 GB do `qwen3:4b`).
- Internet só na primeira execução, para instalar as bibliotecas e baixar os modelos.
- Não precisa de GPU.

## 3. Passo a passo

Todos os comandos rodam na raiz do projeto, com a venv ativa.

1. Clone o repositório e crie a venv:
   ```
   git clone https://github.com/leonardossantosrj/PB_Infnet.git
   cd PB_Infnet
   python3 -m venv venv
   source venv/bin/activate
   python -m pip install -r requirements.txt
   ```
2. Instale o Ollama (https://ollama.com/download), abra o aplicativo e baixe o modelo:
   ```
   ollama pull qwen3:4b
   ```
3. Opcional: atualize os dados da web. Os arquivos já coletados estão no repositório.
   ```
   python 2_data_acquisition_and_understanding/scraping_wikipedia.py
   python 2_data_acquisition_and_understanding/scraping_noticias.py
   ```
4. No terminal 1, suba a API. Na primeira vez, ela baixa o modelo de sentimento.
   ```
   python -m uvicorn api:app --reload
   ```
5. No terminal 2, classifique as notícias. São cerca de 230 títulos, o que leva poucos minutos.
   ```
   python 3_modeling/classificar_noticias.py
   ```
6. Ainda no terminal 2, suba o painel:
   ```
   python -m streamlit run app.py
   ```

## 4. Fluxo de atualização dos dados

```
scraping_noticias.py ─> data/raw/noticias_saneamento.csv ─> classificar_noticias.py (usa a API) ─> data/processed/noticias_sentimento.csv ─> painel
```

O painel guarda os arquivos em cache (`st.cache_data`). Depois de coletar ou classificar de novo, use o menu de três pontos do Streamlit, no canto superior direito, e escolha **Clear cache**. Outra opção é reiniciar o painel.

## 5. Por que o painel não foi publicado na nuvem

O plano inicial era publicar no Streamlit Community Cloud. Com a entrada dos modelos de IA locais no TP4 e no TP5, isso deixou de ser viável no plano gratuito: os dois modelos somam cerca de 3,6 GB, e o Ollama precisa rodar como um programa separado. Para publicar, seria preciso trocar o LLM local por uma API paga na nuvem, o que contraria a escolha de manter os dados e o processamento no computador do usuário. Por isso, o deployment do projeto é local e está documentado neste guia.

## 6. Problemas comuns

| Mensagem ou sintoma | Causa | Solução |
|---|---|---|
| "A API não está rodando..." no script ou na página API | A API não foi iniciada | Rodar `python -m uvicorn api:app --reload` em outro terminal |
| Erro 503 em `/processar_texto` | O modelo de sentimento não carregou | Ler o motivo na mensagem. Na primeira vez, é preciso internet para o download |
| "As notícias ainda não foram classificadas" | Falta o arquivo `data/processed/noticias_sentimento.csv` | Rodar o passo 5 com a API ligada |
| "O Ollama não está rodando" | O aplicativo do Ollama está fechado | Abrir o aplicativo do Ollama |
| "O modelo qwen3:4b não foi baixado" | O modelo não está no computador | Rodar `ollama pull qwen3:4b` |
| `KeyError: 'termo'` na página Conteúdo da web | O CSV de notícias é de uma coleta antiga | Rodar `scraping_noticias.py` de novo |
| `command not found: python` no Mac | O comando no Mac é `python3` | Criar a venv com `python3 -m venv venv`. Com a venv ativa, `python` funciona |
