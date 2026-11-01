import pandas as pd
import streamlit as st

st.title("Painel Saneamento Brasil: ODS 6")

st.header("Problema de negócio")
st.write(
    "Em 2020, apenas 48,7% da população brasileira tinha esgotamento sanitário gerenciado "
    "de forma segura, abaixo da média mundial de 54,0% (OMS/UNICEF). O Marco Legal do "
    "Saneamento (Lei 14.026/2020) definiu como meta, até 2033, levar água potável a 99% da "
    "população e coleta e tratamento de esgoto a 90%. Os dados para acompanhar esse avanço "
    "existem, mas estão espalhados em bases técnicas, muitas vezes em inglês, e são difíceis "
    "de interpretar. Isso dificulta que gestores públicos, ONGs e cidadãos acompanhem a "
    "evolução do saneamento e cobrem resultados."
)

st.header("Objetivos do projeto")
st.markdown(
    """
- Reunir em um único painel os indicadores de acesso à água e ao esgoto do Brasil.
- Comparar o Brasil com outros países e com a média mundial.
- Exibir notícias e conteúdos da web sobre saneamento no Brasil.
- Usar IA generativa (LLM) para explicar os indicadores em linguagem simples.
"""
)

st.header("Links úteis")
st.markdown(
    """
- [ONU: Objetivo 6, Água potável e saneamento](https://unric.org/pt/objetivo-6-agua-potavel-e-saneamento-2/)
- [Lei 14.026/2020: Marco Legal do Saneamento](https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2020/lei/L14026.htm)
- [OMS/UNICEF JMP: dados de água e saneamento](https://washdata.org)
- [Our World in Data: Clean Water and Sanitation](https://ourworldindata.org/clean-water-sanitation)
- [Instituto Trata Brasil](https://tratabrasil.org.br)
- [Conecta Brasil](https://conectabrasil.org/home)
- [Observatório do Terceiro Setor: projetos sociais](https://observatorio3setor.org.br/carrossel/lista-conheca-projetos-sociais-de-15-causas-diferentes/)
"""
)

st.header("Amostra dos dados")
st.write("Fonte: OMS/UNICEF JMP, via Our World in Data. Percentual da população com acesso a cada serviço.")

dados = pd.read_csv("data/raw/oms_unicef_agua_saneamento.csv")

colunas = {
    "Entity": "País",
    "Year": "Ano",
    "wat_bas": "Água básica (%)",
    "wat_sm": "Água segura (%)",
    "san_bas": "Esgoto básico (%)",
    "san_sm": "Esgoto seguro (%)",
}
amostra = dados[list(colunas)].rename(columns=colunas)

st.dataframe(amostra[amostra["País"] == "Brazil"].tail(10), hide_index=True)
