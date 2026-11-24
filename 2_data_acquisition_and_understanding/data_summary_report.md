# Data Summary Report

## 1. Resumo geral das fontes

| # | Fonte | Tipo de dado | Forma de coleta | Arquivo | Objetivo de uso |
|---|---|---|---|---|---|
| 1 | OMS/UNICEF JMP, via Our World in Data | Estruturado, numérico: percentual e número de pessoas com acesso a água e esgoto, por país e ano | Download do CSV no repositório do Our World in Data (github.com/owid/owid-datasets) | `data/raw/oms_unicef_agua_saneamento.csv` | Indicadores do painel (ODS 6.1.1 e 6.2.1), comparação entre países e consulta pela API |
| 2 | Wikipedia: artigo "Saneamento básico" | Não estruturado: texto | Web scraping com Beautiful Soup (`scraping_wikipedia.py`) | `data/raw/wikipedia_saneamento.txt` | Nuvem de palavras, estatísticas do texto e base para resumos e perguntas e respostas com LLM |
| 3 | Google Notícias: buscas "saneamento básico", "água potável" e "tratamento de esgoto" | Semiestruturado: tema da busca, título, veículo, data e link | Web scraping com Beautiful Soup (`scraping_noticias.py`) | `data/raw/noticias_saneamento.csv` | Tabela de notícias com filtro por tema e títulos usados na classificação de sentimento com o modelo local (`POST /processar_texto`) |
| 4 | CSV enviado pelo usuário | Estruturado, numérico | Upload na página "Enviar dados" | Fica na sessão do usuário (não é salvo em disco) | Complementar os indicadores com dados próprios |
| 5 | Dados enviados pela API | Estruturado, numérico | Rota `POST /indicadores` da API | `data/processed/indicadores_api.csv` | Guardar novos registros, como os de estados ou municípios, que passam a aparecer na rota `GET /indicadores` |

**Selenium:** foi avaliado e não foi usado. As fontes 2 e 3 entregam o conteúdo direto no HTML e no RSS, sem depender de JavaScript, então o Beautiful Soup é suficiente.

## 2. Fonte 1: OMS/UNICEF JMP

- **Volume:** 5.118 linhas, 249 países e regiões, anos de 2000 a 2020, 118 colunas.
- **Colunas usadas no painel e na API:**

| Coluna original | Nome no painel | Nome na API | Significado |
|---|---|---|---|
| `Entity` | País | `pais` | País ou região |
| `Year` | Ano | `ano` | Ano |
| `wat_bas` | Água básica (%) | `agua_basica` | % da população com acesso básico a água potável |
| `wat_sm` | Água segura (%) | `agua_segura` | % da população com água potável gerenciada de forma segura (ODS 6.1.1) |
| `san_bas` | Esgoto básico (%) | `esgoto_basico` | % da população com acesso básico a esgotamento sanitário |
| `san_sm` | Esgoto seguro (%) | `esgoto_seguro` | % da população com esgotamento sanitário gerenciado de forma segura (ODS 6.2.1) |

- **Qualidade:** a série do Brasil está completa de 2000 a 2020 nas quatro colunas usadas. Há valores vazios em países com poucas pesquisas, principalmente em "Esgoto seguro (%)". Na API, esses valores vazios aparecem como `null`.
- **Valores de referência do Brasil em 2020:** água segura 85,77% e esgoto seguro 48,71%. A média mundial de esgoto seguro é 53,95%.

## 3. Fonte 2: Wikipedia

- **Conteúdo:** todos os parágrafos do artigo "Saneamento básico" (https://pt.wikipedia.org/wiki/Saneamento_b%C3%A1sico), um parágrafo por linha.
- **Volume da coleta de 01/11/2026:** 85 parágrafos e cerca de 5.700 palavras.
- **Tratamento no app:** o texto é convertido para minúsculas, e são removidas palavras com até 3 letras e palavras muito comuns (stopwords).
- **Qualidade:** o texto inclui marcações de referência, como "[1]", que são ignoradas na contagem de palavras.

## 4. Fonte 3: Google Notícias

- **Colunas:** `termo` (tema da busca), `titulo`, `veiculo`, `data` (data de publicação) e `link`.
- **Volume:** até 100 notícias por busca, que é o limite do feed do Google Notícias. A primeira coleta, de 01/11/2026, com uma única busca, trouxe 100 notícias.
- **Tratamento:** a mesma notícia pode aparecer em mais de uma busca. O script mantém só a primeira ocorrência de cada link.
- **Qualidade:** as notícias mudam a cada coleta, então o script deve ser rodado de novo para atualizar. O feed traz o título, mas não o texto completo da notícia.
- **Uso no modelo de linguagem (TP4):** os títulos são o texto de entrada da análise de sentimento. Na página API do app, o usuário escolhe uma notícia e o título é enviado para a rota `POST /processar_texto`. Como só o título é analisado, títulos muito curtos ou técnicos tendem a ser classificados como neutros.

## 5. Fonte 4: CSV do usuário

- **Formato esperado:** as mesmas colunas do painel: País, Ano, Água básica (%), Água segura (%), Esgoto básico (%) e Esgoto seguro (%).
- **Arquivo de exemplo:** `data/processed/exemplo_upload_brasil_urbano_rural.csv`, com 42 linhas, Brasil urbano e Brasil rural de 2000 a 2020. Foi criado a partir das colunas urbanas e rurais da fonte 1, por exemplo `wat_sm_urban` e `san_sm_rural`.

## 6. Fonte 5: dados enviados pela API

- **Colunas:** `pais`, `ano`, `agua_basica`, `agua_segura`, `esgoto_basico` e `esgoto_seguro`.
- **Validação:** a API só aceita percentuais entre 0 e 100. Fora disso, responde com erro 422.
- **Estado inicial:** o arquivo começa só com o cabeçalho, e cada envio pela rota POST adiciona uma linha.
