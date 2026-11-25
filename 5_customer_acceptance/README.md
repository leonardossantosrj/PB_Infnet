# Fase 5 (Customer Acceptance): Project Final Report

## 1. Resumo

O **Painel Saneamento Brasil** reúne em um único lugar os dados de acesso à água e ao esgoto do Brasil (ODS 6), as notícias e os conteúdos da web sobre o tema e dois modelos de IA que rodam no próprio computador:

- um modelo de sentimento, que mostra se as notícias de cada tema trazem avanços, problemas ou só informação;
- um assistente com memória conversacional, que responde perguntas sobre os dados em linguagem simples.

O resultado é um painel em que gestores públicos, ONGs, jornalistas e cidadãos conseguem entender a situação do saneamento sem precisar interpretar bases técnicas em inglês.

## 2. Problema e solução

| | |
|---|---|
| **Problema** | Em 2020, só 48,7% dos brasileiros tinham esgoto gerenciado de forma segura, abaixo da média mundial (54,0%). O Marco Legal do Saneamento definiu metas para 2033, mas os dados para acompanhá-las estão espalhados e são difíceis de interpretar. |
| **Público-alvo** | Gestores públicos, ONGs, jornalistas, estudantes e cidadãos. |
| **Solução** | Painel em Streamlit com indicadores, conteúdo da web, API em FastAPI, análise de sentimento das notícias e um assistente de IA local com memória conversacional. |
| **ODS e ESG** | ODS 6 (indicadores 6.1.1 e 6.2.1). Pilar Ambiental, com impacto Social. |

## 3. O ciclo de ciência de dados no projeto

| Fase do TDSP | O que foi feito | Artefato |
|---|---|---|
| 1. Business Understanding | Problema, ODS, público, metas e indicadores de sucesso | [Project Charter](../1_business_understanding/project_charter.md) |
| 2. Data Acquisition and Understanding | Download dos indicadores da OMS/UNICEF, web scraping da Wikipedia e do Google Notícias, API para receber novos dados | [Data Summary Report](../2_data_acquisition_and_understanding/data_summary_report.md) |
| 3. Modeling | Modelo de sentimento local (TP4), classificação de todas as notícias e assistente com LLM local, engenharia de prompts e memória (TP5) | [Model Report](../3_modeling/README.md) |
| 4. Deployment | Painel com várias páginas, API documentada e execução local dos modelos | [Guia de deployment](../4_deployment/README.md) |
| 5. Customer Acceptance | Testes com casos reais, insights e avaliação das metas | Este relatório |

## 4. Insights gerados

### Indicadores (OMS/UNICEF, 2000 a 2020)

- **Água básica está quase universal:** 99,3% dos brasileiros tinham acesso básico a água em 2020, acima da América Latina (97,3%) e do mundo (90,1%).
- **Água segura ainda está longe da meta:** 85,8% em 2020. O indicador subiu cerca de 0,5 ponto percentual por ano desde 2000. Para chegar a 99% em 2033, precisaria subir cerca de 1 ponto por ano, o dobro do ritmo histórico.
- **Esgoto seguro é o maior desafio:** 48,7% em 2020, contra 35,7% em 2000. O Brasil está acima da América Latina (34,1%), mas abaixo do mundo (54,0%).
- **No ritmo atual, a meta de esgoto fica distante:** o esgoto seguro subiu cerca de 0,65 ponto por ano. Para chegar a 90% em 2033, precisaria subir cerca de 3,2 pontos por ano, quase cinco vezes mais rápido. (A meta do Marco Legal é de coleta e tratamento de esgoto; o indicador de esgoto seguro da OMS/UNICEF é o mais próximo dela.)

### Sentimento das notícias (modelo local)

Coleta de 24/11/2026: 229 notícias das buscas "água potável", "tratamento de esgoto" e "saneamento básico".

| Sentimento | Percentual das notícias |
|---|---|
| Positivo | **[preencher após rodar o script de classificação]** |
| Neutro | **[preencher]** |
| Negativo | **[preencher]** |

- **Tema com a maior proporção de notícias negativas:** **[preencher com o insight da página Insights com IA]**

### Conferência do modelo de sentimento

Amostra de 10 notícias, comparando a classificação do modelo com uma leitura humana do título.

| Título | Modelo | Leitura humana | Concorda? |
|---|---|---|---|
| **[preencher]** | | | |

## 5. Testes do assistente com casos reais

Testes feitos na página Insights com IA, em uma única conversa, na ordem abaixo.

| # | Pergunta | O que valida | Resposta esperada | Resultado observado |
|---|---|---|---|---|
| 1 | Como está o esgoto tratado no Brasil? | Uso dos dados do prompt | 48,71% em 2020, citando a OMS/UNICEF | **[preencher]** |
| 2 | E comparado ao mundo? | Memória: entende que o assunto continua sendo esgoto | Mundo com 53,95% em 2020; Brasil abaixo | **[preencher]** |
| 3 | E com a América Latina? | Memória | América Latina com 34,07%; Brasil acima | **[preencher]** |
| 4 | O Brasil vai cumprir a meta de esgoto de 2033? | Metas no prompt | Meta de 90%, distância grande para o valor de 2020, sem inventar previsões | **[preencher]** |
| 5 | Qual o percentual de esgoto tratado na Argentina? | Regra de não inventar | Diz que o painel não tem esse dado | **[preencher]** |
| 6 | O que as notícias dizem sobre tratamento de esgoto? | Uso do sentimento das notícias | Resume o sentimento do tema e cita exemplos | **[preencher]** |
| 7 | Resuma o que é saneamento em 3 frases. | Uso do texto da Wikipedia | Resumo com base no trecho da Wikipedia | **[preencher]** |
| 8 | (com o Ollama fechado) Como está a água no Brasil? | Tratamento de erros | Mensagem "O Ollama não está rodando..." | **[preencher]** |

## 6. Como a solução resolve o problema de negócio

- **Dados espalhados:** a coleta reuniu indicadores oficiais, notícias e conteúdo enciclopédico em uma mesma estrutura (`data/raw` e `data/processed`) e em uma API.
- **Números sem contexto:** o modelo de sentimento mostra o tom do noticiário de cada tema, o que ajuda a entender se o assunto está em avanço ou em crise.
- **Dados difíceis de interpretar:** o assistente explica os indicadores em linguagem simples, compara o Brasil com a região, o mundo e as metas, e lembra a conversa. Por isso, o usuário pode ir aprofundando o assunto como faria com um especialista.
- **Confiabilidade:** a engenharia de prompts prende as respostas aos dados oficiais coletados e obriga o assistente a citar ano e fonte e a admitir quando não tem um dado.
- **Custo e privacidade:** os dois modelos rodam no computador do usuário, sem custo por uso e sem enviar dados para a nuvem.

Para o ESG e o ODS 6, isso significa transparência: quem cobra a universalização do saneamento passa a ter os números, o contexto e uma explicação acessível no mesmo lugar.

## 7. Avaliação das metas do Project Charter

| Meta | Resultado |
|---|---|
| Cobrir os indicadores oficiais do ODS 6 | Atingida: 6.1.1 e 6.2.1 do Brasil completos de 2000 a 2020 |
| Permitir comparação internacional | Atingida: 249 países e regiões, incluindo a média mundial |
| Manter o conteúdo atualizado | Atingida: coleta de notícias de 24/11/2026, com os scripts prontos para novas coletas |
| Permitir integração com outros sistemas | Atingida: 3 rotas documentadas em `/docs` |
| Analisar o sentimento das notícias localmente | Atingida: rota `POST /processar_texto` com o modelo local |
| Classificar todas as notícias coletadas | **[confirmar após rodar o script]** |
| Responder perguntas com base nos dados e lembrar a conversa | **[confirmar com os testes da seção 5]** |
| Ser fácil de entender (teste com 5 usuários) | Não realizada nesta entrega. Roteiro na seção 8 |

## 8. Roteiro do teste com usuários

Pedir a 5 pessoas do público-alvo que respondam, usando só o painel:

1. Qual percentual da população brasileira tinha esgoto tratado de forma segura em 2020?
2. O Brasil está melhor ou pior que a média mundial nesse indicador?
3. As notícias sobre tratamento de esgoto são, na maioria, positivas, neutras ou negativas?

A meta é que pelo menos 4 das 5 pessoas acertem as 3 perguntas.

## 9. Limitações e próximos passos

- O assistente conhece só os dados de Brasil, América Latina e mundo em 2000, 2010 e 2020 que estão no prompt. Um próximo passo é deixar o usuário escolher outros países, buscando os dados pela API.
- O sentimento é calculado só pelos títulos. Coletar o texto completo das notícias daria uma análise mais precisa.
- Os indicadores da OMS/UNICEF vão até 2020. Incluir dados mais recentes, como os do SNIS e do Censo 2022, deixaria o acompanhamento das metas mais atual.
- Publicar o painel exigiria trocar o LLM local por uma API na nuvem (ver o [guia de deployment](../4_deployment/README.md)).
