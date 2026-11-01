# Data Summary Report

## 1. Resumo geral das fontes

| # | Fonte | Tipo de dado | Forma de coleta | Arquivo | Objetivo de uso |
|---|---|---|---|---|---|
| 1 | OMS/UNICEF JMP, via Our World in Data | Estruturado, numérico: percentual e número de pessoas com acesso a água e esgoto, por país e ano | Download do CSV no repositório do Our World in Data (github.com/owid/owid-datasets) | `data/raw/oms_unicef_agua_saneamento.csv` | Indicadores do painel (ODS 6.1.1 e 6.2.1) e comparação entre países |
| 2 | Wikipedia: artigo "Saneamento básico" | Não estruturado: texto | Web scraping com Beautiful Soup (`scraping_wikipedia.py`) | `data/raw/wikipedia_saneamento.txt` | Nuvem de palavras e estatísticas do texto |
| 3 | Google Notícias: busca "saneamento básico" | Semiestruturado: título, veículo, data e link | Web scraping com Beautiful Soup (`scraping_noticias.py`) | `data/raw/noticias_saneamento.csv` | Tabela de notícias recentes e contagem por veículo |
| 4 | CSV enviado pelo usuário | Estruturado, numérico | Upload na aplicação | Fica na sessão do usuário (não é salvo em disco) | Complementar os indicadores com dados próprios |

## 2. Fonte 1: OMS/UNICEF JMP

- **Volume:** 5.118 linhas, 249 países e regiões, anos de 2000 a 2020, 118 colunas.
- **Colunas usadas no painel:**

| Coluna original | Nome no painel | Significado |
|---|---|---|
| `Entity` | País | País ou região |
| `Year` | Ano | Ano |
| `wat_bas` | Água básica (%) | % da população com acesso básico a água potável |
| `wat_sm` | Água segura (%) | % da população com água potável gerenciada de forma segura (ODS 6.1.1) |
| `san_bas` | Esgoto básico (%) | % da população com acesso básico a esgotamento sanitário |
| `san_sm` | Esgoto seguro (%) | % da população com esgotamento sanitário gerenciado de forma segura (ODS 6.2.1) |

- **Qualidade:** a série do Brasil está completa de 2000 a 2020 nas quatro colunas usadas. Há valores vazios em países com poucas pesquisas, principalmente em "Esgoto seguro (%)".
- **Valores de referência do Brasil em 2020:** água segura 85,77% e esgoto seguro 48,71%. A média mundial de esgoto seguro é 53,95%.

## 3. Fonte 2: Wikipedia

- **Conteúdo:** todos os parágrafos do artigo "Saneamento básico" (https://pt.wikipedia.org/wiki/Saneamento_b%C3%A1sico), um parágrafo por linha.
- **Tratamento no app:** o texto é convertido para minúsculas, e são removidas palavras com até 3 letras e palavras muito comuns (stopwords).
- **Qualidade:** o texto inclui marcações de referência, como "[1]", que são ignoradas na contagem de palavras.

## 4. Fonte 3: Google Notícias

- **Colunas:** `titulo`, `veiculo`, `data` (data de publicação) e `link`.
- **Volume:** até 100 notícias por coleta, que é o limite do feed do Google Notícias.
- **Qualidade:** a mesma notícia pode aparecer em mais de um veículo. As notícias mudam a cada coleta, então o script deve ser rodado de novo para atualizar.

## 5. Fonte 4: CSV do usuário

- **Formato esperado:** as mesmas colunas do painel: País, Ano, Água básica (%), Água segura (%), Esgoto básico (%) e Esgoto seguro (%).
- **Arquivo de exemplo:** `data/processed/exemplo_upload_brasil_urbano_rural.csv`, com 42 linhas, Brasil urbano e Brasil rural de 2000 a 2020. Foi criado a partir das colunas urbanas e rurais da fonte 1, por exemplo `wat_sm_urban` e `san_sm_rural`.
