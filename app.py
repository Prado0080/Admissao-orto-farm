import streamlit as st

st.title("Teste UTI")
formato = st.radio("Selecione o tipo de formatação:", ["Ortopedia", "Clínica médica", "UTI"])
st.write(f"Você selecionou: {formato}")
