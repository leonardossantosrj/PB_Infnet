# Data Summary Report (primeiro esboço)

## Fontes de dados

| # | Fonte | Tipo de dado | Forma de coleta | Objetivo de uso |
|---|---|---|---|---|
| 1 | OMS/UNICEF JMP, via Our World in Data | Estruturado, numérico: percentual e número de pessoas com acesso a água e esgoto, por país e ano (2000 a 2020) | Download do CSV no repositório do Our World in Data, salvo em `data/raw/` | Indicadores principais do painel (ODS 6.1.1 e 6.2.1) e comparação do Brasil com outros países |
| 2 | Wikipedia: artigo "Saneamento no Brasil" | Não estruturado: texto | Web scraping, salvo em `data/` | Contexto sobre o tema e nuvem de palavras |
| 3 | Google News: busca por "saneamento básico" | Semiestruturado: título, veículo, data e link das notícias | Web scraping, salvo em `data/` | Exibir notícias recentes sobre saneamento |
| 4 | Arquivos CSV enviados pelo usuário (ex.: dados municipais do SNIS/SINISA) | Estruturado, numérico | Upload na aplicação | Complementar o painel com dados locais |

## Principais variáveis da fonte 1

| Coluna | Significado |
|---|---|
| `Entity` | País ou região |
| `Year` | Ano |
| `wat_bas` | % da população com acesso básico a água potável |
| `wat_sm` | % da população com água potável gerenciada de forma segura (indicador ODS 6.1.1) |
| `san_bas` | % da população com acesso básico a esgotamento sanitário |
| `san_sm` | % da população com esgotamento sanitário gerenciado de forma segura (indicador ODS 6.2.1) |


