# Project Charter: Painel Saneamento Brasil (ODS 6)

## 1. Problema de negócio

Em 2020, apenas **48,7%** da população brasileira tinha esgotamento sanitário gerenciado de forma segura, abaixo da média mundial de **54,0%**. No acesso à água gerenciada de forma segura, o Brasil estava em **85,8%** (OMS/UNICEF JMP, 2021).

O Marco Legal do Saneamento (Lei 14.026/2020) definiu como meta, até 2033, que **99%** da população tenha água potável e **90%** tenha coleta e tratamento de esgoto.

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
- explicações em linguagem simples geradas por um LLM, com engenharia de prompts.

**Como será usado:** o usuário acessa o painel pelo navegador, consulta os indicadores e as notícias e lê os resumos gerados pela IA.

**Fora do escopo:** previsão de indicadores futuros e dados internos de empresas de saneamento. 

## 5. Objetivos

- Reunir em um único painel os indicadores de acesso à água e ao esgoto do Brasil.
- Comparar o Brasil com outros países e com a média mundial.
- Exibir notícias e conteúdos da web sobre saneamento no Brasil.
- Usar IA generativa (LLM) para explicar os indicadores em linguagem simples.

## 6. Metas e indicadores de sucesso

| Meta | Indicador | Como medir |
|---|---|----|
| Cobrir os indicadores oficiais do ODS 6 | Indicadores 6.1.1 e 6.2.1 disponíveis para o Brasil de 2000 a 2020 | Conferir no painel se as séries estão completas |
| Permitir comparação internacional | Ao menos 5 países e a média mundial disponíveis para comparação | Conferir os filtros do painel |
| Manter o conteúdo atualizado | Notícias coletadas há em um período previamente definido | Data da última coleta registrada nos arquivos |
| Ser fácil de entender | Ao menos 4 de 5 usuários do público-alvo respondem corretamente 3 perguntas sobre o saneamento no Brasil usando só o painel | Teste com usuários na fase de aceitação |

## 7. Stakeholders

| Stakeholder | Papel no projeto |
|---|---|
| Leonardo Santos| Desenvolve o projeto e acumula os papéis do TDSP: Project Lead, Project Manager, Data Scientist e Solution Architect |
| Professor da disciplina | Cliente e avaliador das entregas |
| Público-alvo (gestores, ONGs, jornalistas, cidadãos) | Usuários finais do painel |
| OMS/UNICEF JMP e Our World in Data | Fornecedores dos dados de água e saneamento |
