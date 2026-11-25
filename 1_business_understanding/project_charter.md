# Project Charter: Painel Saneamento Brasil (ODS 6)

## 1. Problema de negócio

Em 2020, apenas **48,7%** da população brasileira tinha esgotamento sanitário gerenciado de forma segura, abaixo da média mundial de **54,0%**. No acesso à água gerenciada de forma segura, o Brasil estava em **85,8%** (OMS/UNICEF JMP, 2021).

O Marco Legal do Saneamento (Lei 14.026/2020) definiu como meta, até 2033, que **99%** da população tenha água potável e **90%** tenha coleta e tratamento de esgoto.

Os dados para acompanhar esse avanço existem, mas estão espalhados em bases técnicas, muitas vezes em inglês, e são difíceis de interpretar para quem não é da área. Por isso, gestores públicos, ONGs e cidadãos têm dificuldade para acompanhar a evolução do saneamento e cobrar resultados.

**Revisão no TP3:** com o FastAPI, o projeto deixa de ser só um painel para leitura. Agora outros sistemas, como sites de ONGs ou a etapa de LLM, podem consultar os indicadores pela API, e novos dados locais, como os de um estado ou município, podem ser enviados por ela. O Selenium foi avaliado e não foi necessário, porque as fontes usadas entregam o conteúdo direto no HTML ou no RSS, sem depender de JavaScript (ver seção 11).

**Revisão no TP4:** além dos números, o público precisa entender o tom do que se fala sobre saneamento. Um modelo de linguagem rodando no próprio computador classifica as notícias coletadas como positivas, neutras ou negativas, mostrando se o noticiário traz avanços ou problemas. Por rodar localmente, não depende de serviços pagos na nuvem (ver seção 12).

**Revisão no TP5:** o problema central é que os dados existem, mas são difíceis de interpretar. Um assistente de IA com memória conversacional, que roda no próprio computador, responde perguntas sobre os indicadores, as notícias e o texto da Wikipedia em linguagem simples. Como ele lembra a conversa, o usuário pode ir aprofundando ("e no mundo?", "e a meta de 2033?") sem repetir o contexto. A página "Insights com IA" junta esse assistente aos gráficos do sentimento das notícias (ver seções 13 e 14).

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
- um assistente de IA local (LLM) com memória conversacional e engenharia de prompts, que explica os dados em linguagem simples;
- uma página "Insights com IA" que mostra o ciclo de ciência de dados, os gráficos do sentimento das notícias e o assistente.

**Como será usado:** o usuário acessa o painel pelo navegador e navega pelo menu lateral entre as páginas de indicadores, conteúdo da web, envio de dados e API. Outros sistemas podem usar os dados diretamente pela API.

**Fora do escopo:** previsão de indicadores futuros, dados internos de empresas de saneamento e publicação na nuvem (os modelos de IA rodam no computador do usuário; ver seção 13).

## 5. Objetivos

- Reunir em um único painel os indicadores de acesso à água e ao esgoto do Brasil.
- Comparar o Brasil com outros países e com a média mundial.
- Exibir notícias e conteúdos da web sobre saneamento no Brasil.
- Disponibilizar os dados por uma API, para que outros sistemas possam consultá-los e enviar novos dados.
- Classificar o sentimento das notícias sobre saneamento com um modelo de linguagem local.
- Usar IA generativa (LLM) com memória conversacional para explicar os dados em linguagem simples.

## 6. Metas e indicadores de sucesso

| Meta | Indicador | Como medir |
|---|---|----|
| Cobrir os indicadores oficiais do ODS 6 | Indicadores 6.1.1 e 6.2.1 disponíveis para o Brasil de 2000 a 2020 | Conferir no painel se as séries estão completas |
| Permitir comparação internacional | Ao menos 5 países e a média mundial disponíveis para comparação | Conferir os filtros do painel |
| Manter o conteúdo atualizado | Notícias coletadas há em um período previamente definido | Data da última coleta registrada nos arquivos |
| Permitir integração com outros sistemas | API com ao menos 2 rotas documentadas: uma de consulta (GET) e uma de envio (POST) | Testar as rotas pela documentação automática em `/docs` |
| Analisar o sentimento das notícias localmente | Rota `POST /processar_texto` respondendo com o modelo rodando no próprio computador, sem serviços na nuvem, e com erros tratados (400, 422, 500 e 503) | Testar a rota em `/docs` e na página API do app |
| Preparar os dados para a etapa de LLM | Cada base de dados com uma tarefa de LLM definida (resumo, sentimento, perguntas e respostas ou geração de texto) | Plano em `3_modeling/README.md` |
| Classificar todas as notícias coletadas | 100% das notícias de `data/raw/noticias_saneamento.csv` com sentimento em `data/processed/noticias_sentimento.csv` | Rodar `3_modeling/classificar_noticias.py` e conferir a página "Insights com IA" |
| Responder perguntas com base nos dados e lembrar a conversa | O assistente acerta os números dos casos de teste, cita ano e fonte e responde perguntas de continuação | Casos de teste no [Project Final Report](../5_customer_acceptance/README.md) |
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
| TP5 | Modeling, Deployment e Customer Acceptance | Classificação de todas as notícias, assistente com memória conversacional (LLM local no Ollama), página "Insights com IA", artefatos do TDSP completos e Project Final Report | Concluída |

## 10. Arquitetura

```
Wikipedia ──────┐
Google Notícias ┴─> scraping (requests + Beautiful Soup) ─> data/raw (TXT e CSV) ─┐
OMS/UNICEF (CSV do Our World in Data) ───────────────────> data/raw (CSV) ────────┤
CSV enviado pelo usuário ─> página Enviar dados ─> estado de sessão ──────────────┼─> app.py (Streamlit, várias páginas) ─> usuário
                                                                                  │
api.py (FastAPI) ─ GET e POST /indicadores ─> data/processed/indicadores_api.csv ─┤
   │  └── POST /processar_texto ─> modelo de sentimento local (Transformers)      │
   │                                   ↑                                           │
   │  3_modeling/classificar_noticias.py ─> data/processed/noticias_sentimento.csv ┤
   ↑                                                                               │
   └── usada pela página API do app e por outros sistemas                          │
                                                                                   │
assistente.py ─> LLM local qwen3:4b (Ollama) com os dados no prompt ───────────────┘
                 e memória da conversa (página Insights com IA)
```

- **Coleta:** os scripts de scraping rodam separados do app e salvam os arquivos em `data/raw/`.
- **Aplicação:** o `app.py` monta o menu de navegação, e cada página fica em um arquivo da pasta `paginas/`. As funções de leitura com `st.cache_data` ficam em `dados.py`, usadas por todas as páginas. Os dados enviados pelo usuário ficam em `st.session_state` e valem para todas as páginas.
- **API:** o `api.py` oferece a consulta (GET) e o envio (POST) de indicadores e a análise de sentimento (`POST /processar_texto`). A página API do app usa essas rotas.
- **Modelo de linguagem:** o modelo `cardiffnlp/twitter-xlm-roberta-base-sentiment` é carregado pela biblioteca Transformers uma vez, quando a API sobe, e roda no próprio computador. A justificativa da escolha está no [Model Report](../3_modeling/README.md).
- **Dados processados pela IA:** o script `classificar_noticias.py` envia cada título de notícia para a rota `/processar_texto` e salva o resultado em `data/processed/`, que alimenta os gráficos e o assistente.
- **Assistente:** o `assistente.py` monta o prompt com os dados do projeto e envia a conversa ao LLM local `qwen3:4b`, pelo Ollama. O histórico fica em `st.session_state`.
- **Versionamento e execução:** o código fica no GitHub e roda localmente, conforme o [guia de deployment](../4_deployment/README.md).

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

## 13. Decisões técnicas do TP5

| Decisão | Motivo |
|---|---|
| Caminho escolhido: memória conversacional | O problema do projeto é a dificuldade de interpretar os dados. Uma conversa em que o usuário vai aprofundando as perguntas resolve isso de forma direta e simples de usar. |
| LLM local `qwen3:4b`, pelo Ollama | É gratuito, roda no computador sem GPU (download de 2,5 GB), suporta mais de 100 idiomas e mantém os dados e as perguntas fora da nuvem, seguindo a linha do TP4. A API do Gemini foi testada e recusada pela conta (erro 403 de camada gratuita indisponível). Detalhes no [Model Report](../3_modeling/README.md). |
| Dados do projeto no prompt (engenharia de prompts) | Os indicadores, o resumo do sentimento das notícias e o trecho da Wikipedia vão no prompt de sistema, com regras para responder só com esses dados e citar ano e fonte. Isso reduz respostas inventadas. |
| Memória em janela das últimas 10 mensagens | Mantém o contexto da conversa sem estourar o limite de texto do modelo, que é pequeno. |
| Classificar as notícias uma vez e salvar em `data/processed/` | Classificar a cada abertura da página seria lento. O resultado fica salvo, como uma camada de dado tratado, e é reaproveitado pelos gráficos e pelo assistente. |
| Rodar localmente, sem publicar no Streamlit Community Cloud | Os dois modelos de IA rodam no computador do usuário (cerca de 3,6 GB no total) e não cabem no plano gratuito da nuvem. A execução local está documentada no guia de deployment. |

## 14. Como dados, IA e engenharia de prompts resolvem o problema

O problema de negócio tem três partes, e cada etapa do ciclo de ciência de dados responde a uma delas:

| Parte do problema | Etapa do ciclo | Como o projeto resolve |
|---|---|---|
| Os dados estão espalhados | Coleta e preparação | Indicadores oficiais da OMS/UNICEF, notícias do Google Notícias e o texto da Wikipedia são coletados por download e web scraping, padronizados e reunidos em `data/` e na API. |
| Os números sozinhos não mostram o contexto | IA aplicada aos dados | O modelo de sentimento classifica todas as notícias, mostrando se o noticiário de cada tema traz avanços, problemas ou só informação. |
| Os dados são difíceis de interpretar | IA generativa e engenharia de prompts | O assistente explica os indicadores em linguagem simples, compara o Brasil com a América Latina, com o mundo e com as metas do Marco Legal, e responde perguntas de continuação graças à memória. |

A engenharia de prompts é o que liga os dados à IA: sem os dados no prompt, o LLM responderia com o que aprendeu no treino, que pode estar desatualizado ou errado. Com os dados do projeto e regras claras, as respostas ficam presas às fontes oficiais e verificáveis. Assim, o projeto passa pelo ciclo completo do TDSP: do problema de negócio (fase 1) e da coleta (fase 2), passando pela modelagem com IA (fase 3), até o painel em uso (fase 4) e a validação dos resultados (fase 5).
