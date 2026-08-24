"""
Interface do agente em Streamlit - chat simples usando o agente da etapa 3.
"""

import streamlit as st
from agente import montar_agente

st.set_page_config(page_title="Assistente NexaCommerce")
st.title("Assistente de Onboarding e Buddy Program - NexaCommerce")

if "agente" not in st.session_state:
    st.session_state.agente = montar_agente()
if "historico" not in st.session_state:
    st.session_state.historico = []

for autor, mensagem in st.session_state.historico:
    with st.chat_message(autor):
        st.markdown(mensagem)

pergunta = st.chat_input("Pergunte algo sobre onboarding ou o buddy program...")
if pergunta:
    st.session_state.historico.append(("user", pergunta))
    with st.chat_message("user"):
        st.markdown(pergunta)

    resposta = st.session_state.agente.invoke(pergunta)

    st.session_state.historico.append(("assistant", resposta))
    with st.chat_message("assistant"):
        st.markdown(resposta)
