# Project Charter: Painel Saneamento Brasil (ODS 6)

## 1. Problema de negócio

Em 2020, apenas **48,7%** da população brasileira tinha esgotamento sanitário gerenciado de forma segura, abaixo da média mundial de **54,0%**. No acesso à água gerenciada de forma segura, o Brasil estava em **85,8%** (OMS/UNICEF JMP, 2021).

O Marco Legal do Saneamento (Lei 14.026/2020) definiu como meta, até 2033, que **99%** da população tenha água potável e **90%** tenha coleta e tratamento de esgoto.

Os dados para acompanhar esse avanço existem, mas estão espalhados em bases técnicas, muitas vezes em inglês, e são difíceis de interpretar para quem não é da área. Por isso, gestores públicos, ONGs e cidadãos têm dificuldade para acompanhar a evolução do saneamento e cobrar resultados.

**Revisão no TP3:** com o FastAPI, o projeto deixa de ser só um painel para leitura. Agora outros sistemas, como sites de ONGs ou a etapa de LLM, podem consultar os indicadores pela API, e novos dados locais, como os de um estado ou município, podem ser enviados por ela. O Selenium foi avaliado e não foi necessário, porque as fontes usadas entregam o conteúdo direto no HTML ou no RSS, sem depender de JavaScript (ver seção 11).

**Revisão no TP4:** além dos números, o público precisa entender o tom do que se fala sobre saneamento. Um modelo de linguagem rodando no próprio computador classifica as notícias coletadas como positivas, neutras ou negativas, mostrando se o noticiário traz avanços ou problemas. Por rodar localmente, não depende de serviços pagos na nuvem (ver seção 12).

## 2. Pilar ESG e ODS atendido

- **Pilar ESG:** Ambiental (E), com impacto também no Social (S).
- **ODS atendido:** **ODS 6, Água potável e saneamento.**

**Justificativa:** o projeto acompanha diretamente os dois indicadores oficiais do ODS 6, o **6.1.1** (população com água potável gerenciada de forma segura) e o **6.2.1** (população com esgotamento sanitário gerenciado de forma segura). Dar transparência a esses números ajuda a sociedade a cobrar a universalização do saneamento, que reduz a poluição de rios e solos (pilar ambiental) e as doenças ligadas à falta de esgoto (pilar social).

## 3. Público-alvo

- Gestores públicos municipais e estaduais da área de saneamento.
- ONGs e projetos do terceiro setor ligados a água e saneamento.
- Jornalistas e estudantes que pesquisam o tema.
- Cidadãos interessados em acompanhar a situação do saneamento no país.

## 4. Escopo

**O que será feito:** um painel web em Python com Streamlit que reúne:
- os indicadores de acesso à água e ao esgoto do Brasil e de outros países;
- notícias e conteúdos da web sobre saneamento, coletados por web scraping;
- uma API com FastAPI para consultar os indicadores e enviar novos dados;
- análise de sentimento das notícias com um modelo de linguagem que roda localmente, pela rota `POST /processar_texto` da API;
- explicações em linguagem simples geradas por um LLM, com engenharia de prompts.

**Como será usado:** o usuário acessa o painel pelo navegador e navega pelo menu lateral entre as páginas de indicadores, conteúdo da web, envio de dados e API. Outros sistemas podem usar os dados diretamente pela API.

**Fora do escopo:** previsão de indicadores futuros e dados internos de empresas de saneamento. 

## 5. Objetivos

- Reunir em um único painel os indicadores de acesso à água e ao esgoto do Brasil.
- Comparar o Brasil com outros países e com a média mundial.
- Exibir notícias e conteúdos da web sobre saneamento no Brasil.
- Disponibilizar os dados por uma API, para que outros sistemas possam consultá-los e enviar novos dados.
- Classificar o sentimento das notícias sobre saneamento com um modelo de linguagem local.
- Usar IA generativa (LLM) para explicar os indicadores em linguagem simples.

## 6. Metas e indicadores de sucesso

| Meta | Indicador | Como medir |
|---|---|----|
| Cobrir os indicadores oficiais do ODS 6 | Indicadores 6.1.1 e 6.2.1 disponíveis para o Brasil de 2000 a 2020 | Conferir no painel se as séries estão completas |
| Permitir comparação internacional | Ao menos 5 países e a média mundial disponíveis para comparação | Conferir os filtros do painel |
| Manter o conteúdo atualizado | Notícias coletadas há em um período previamente definido | Data da última coleta registrada nos arquivos |
| Permitir integração com outros sistemas | API com ao menos 2 rotas documentadas: uma de consulta (GET) e uma de envio (POST) | Testar as rotas pela documentação automática em `/docs` |
| Analisar o sentimento das notícias localmente | Rota `POST /processar_texto` respondendo com o modelo rodando no próprio computador, sem serviços na nuvem, e com erros tratados (400, 422, 500 e 503) | Testar a rota em `/docs` e na página API do app |
| Preparar os dados para a etapa de LLM | Cada base de dados com uma tarefa de LLM definida (resumo, sentimento, perguntas e respostas ou geração de texto) | Plano em `3_modeling/README.md` |
| Ser fácil de entender | Ao menos 4 de 5 usuários do público-alvo respondem corretamente 3 perguntas sobre o saneamento no Brasil usando só o painel | Teste com usuários na fase de aceitação |

## 7. Stakeholders

| Stakeholder | Papel no projeto |
|---|---|
| Leonardo Santos| Desenvolve o projeto e acumula os papéis do TDSP: Project Lead, Project Manager, Data Scientist e Solution Architect |
| Professor da disciplina | Cliente e avaliador das entregas |
| Público-alvo (gestores, ONGs, jornalistas, cidadãos) | Usuários finais do painel |
| OMS/UNICEF JMP e Our World in Data | Fornecedores dos dados de água e saneamento |
| Wikipedia e Google Notícias | Fontes do conteúdo extraído da web |

## 8. Fontes de dados

| Fonte | Uso no projeto |
|---|---|
| OMS/UNICEF JMP, via Our World in Data | Indicadores de acesso à água e ao esgoto por país e ano |
| Wikipedia: artigo "Saneamento básico" | Nuvem de palavras e estatísticas do texto |
| Google Notícias: buscas "saneamento básico", "água potável" e "tratamento de esgoto" | Tabela de notícias recentes, com filtro por tema |
| CSV enviado pelo usuário | Dados complementares, como recortes urbano e rural ou dados municipais |
| Dados enviados pela API (rota POST) | Novos registros de indicadores, salvos em `data/processed/indicadores_api.csv` |

O detalhamento de cada fonte está no [Data Summary Report](../2_data_acquisition_and_understanding/data_summary_report.md).

## 9. Plano do projeto

| Etapa | Fase do TDSP | Entregas | Status |
|---|---|---|---|
| TP1 | Business Understanding | Problema, ODS, metas, público-alvo, estrutura de pastas, primeiros artefatos e app demo | Concluída |
| TP2 | Data Acquisition and Understanding e Deployment | Web scraping, interface interativa, cache, estado de sessão, upload e download, Git e documentação completa | Concluída |
| TP3 | Data Acquisition and Understanding e Deployment | App com múltiplas páginas e menu de navegação, API com FastAPI, melhoria do scraping de notícias e plano de uso de LLMs | Concluída |
| TP4 | Modeling | Escolha de um modelo de linguagem local (Model Report), rota `POST /processar_texto` com classificação de sentimento, Response Models e tratamento de erros na API | Concluída |
| Etapa final | Modeling, Deployment e Customer Acceptance | Demais tarefas de IA (resumos, perguntas e respostas e relatórios), publicação no Streamlit Community Cloud, teste com usuários e Project Final Report | A fazer |

## 10. Arquitetura

```
Wikipedia ──────┐
Google Notícias ┴─> scraping (requests + Beautiful Soup) ─> data/raw (TXT e CSV) ─┐
OMS/UNICEF (CSV do Our World in Data) ───────────────────> data/raw (CSV) ────────┤
CSV enviado pelo usuário ─> página Enviar dados ─> estado de sessão ──────────────┼─> app.py (Streamlit, várias páginas) ─> usuário
                                                                                  │
api.py (FastAPI) ─ GET e POST /indicadores ─> data/processed/indicadores_api.csv ─┘
   │  └── POST /processar_texto ─> modelo de sentimento local (Transformers)
   ↑
   └── usada pela página API do app e por outros sistemas
```

- **Coleta:** os scripts de scraping rodam separados do app e salvam os arquivos em `data/raw/`.
- **Aplicação:** o `app.py` monta o menu de navegação, e cada página fica em um arquivo da pasta `paginas/`. As funções de leitura com `st.cache_data` ficam em `dados.py`, usadas por todas as páginas. Os dados enviados pelo usuário ficam em `st.session_state` e valem para todas as páginas.
- **API:** o `api.py` oferece a consulta (GET) e o envio (POST) de indicadores e a análise de sentimento (`POST /processar_texto`). A página API do app usa essas rotas.
- **Modelo de linguagem:** o modelo `cardiffnlp/twitter-xlm-roberta-base-sentiment` é carregado pela biblioteca Transformers uma vez, quando a API sobe, e roda no próprio computador. A justificativa da escolha está no [Model Report](../3_modeling/README.md).
- **Versionamento e deploy:** o código fica no GitHub e será publicado no Streamlit Community Cloud.

## 11. Decisões técnicas do TP3

| Decisão | Motivo |
|---|---|
| Não usar Selenium | As fontes atuais não dependem de JavaScript: a Wikipedia entrega o texto no HTML, e o Google Notícias, no RSS. O Beautiful Soup resolve com menos código e mais rapidez. |
| Ampliar a coleta de notícias para 3 buscas | Cobre melhor os temas do ODS 6 (esgoto e água potável, além de saneamento básico) e gera mais textos para a etapa de LLM. |
| Separar o app em páginas com `st.navigation` | Cada funcionalidade fica em uma página e em um arquivo, o que facilita encontrar e manter o código. |
| Criar `dados.py` com as funções de leitura | Evita repetir as mesmas funções em várias páginas. |
| API com nomes de colunas sem acento | Nomes como `agua_segura` são mais fáceis de usar em JSON e em outros sistemas do que "Água segura (%)". |

## 12. Decisões técnicas do TP4

| Decisão | Motivo |
|---|---|
| Começar pela classificação de sentimento | Das tarefas do plano de LLMs, é a que tem uma resposta curta e fácil de validar (positivo, neutro ou negativo), e usa os títulos de notícias que já são coletados. |
| Usar o modelo `cardiffnlp/twitter-xlm-roberta-base-sentiment` | Foi treinado para sentimento, inclui o português, roda sem GPU e é baixado com a biblioteca Transformers. Detalhes no [Model Report](../3_modeling/README.md). |
| Carregar o modelo quando a API sobe | Carregar a cada chamada levaria vários segundos. Se o carregamento falhar, a API continua funcionando e a rota de texto responde 503 com o motivo. |
| Fixar a Transformers na versão 4.57.6 | Mantém o projeto estável, sem mudanças inesperadas de uma versão nova. |
| Response Models em todas as rotas | Garantem que a resposta sempre tem os mesmos campos e tipos, o que facilita o uso por outros sistemas. |
