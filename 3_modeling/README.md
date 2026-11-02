# Fase 3 (Modeling): plano de uso de LLMs

Na próxima etapa, os dados já coletados serão usados com um LLM, por meio de engenharia de prompts. A tabela mostra qual base atende a cada tipo de tarefa.

| Tarefa com LLM | Dados usados | Exemplo de uso no painel |
|---|---|---|
| Resumo de texto | Texto da Wikipedia (`data/raw/wikipedia_saneamento.txt`) | Resumo em 5 frases do que é saneamento básico, para quem não é da área |
| Classificação de sentimento | Títulos das notícias (`data/raw/noticias_saneamento.csv`) | Classificar cada notícia como positiva, negativa ou neutra e mostrar a proporção por tema |
| Perguntas e respostas | Texto da Wikipedia e indicadores da OMS/UNICEF | O usuário pergunta, por exemplo, "Como está o esgoto no Brasil comparado ao mundo?", e o LLM responde com base só nesses dados |
| Geração de texto | Indicadores da OMS/UNICEF, consultados pela rota `GET /indicadores` | Relatório automático sobre a evolução de um país entre 2000 e 2020 e a distância para as metas do Marco Legal do Saneamento |

## Como os dados já estão preparados

- Os textos estão em arquivos simples (TXT e CSV), fáceis de enviar a um LLM dentro do prompt.
- As notícias têm o tema da busca na coluna `termo`, o que permite comparar o sentimento entre os temas.
- A API devolve os indicadores em JSON, um formato que pode ser colocado direto no prompt.
- As funções de leitura ficam em `dados.py`, então uma nova página de IA pode reutilizá-las.

Artefato previsto para esta fase: Model Report.
