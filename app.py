"""
Interface do agente em Streamlit - chat simples usando o agente da etapa 3.
"""

import os
import streamlit as st
from agente import montar_agente
from carregar_documentos import carregar_documentos
from processar_e_indexar import dividir_em_chunks, criar_indice

st.set_page_config(page_title="Assistente NexaCommerce")
st.title("Assistente de Onboarding e Buddy Program - NexaCommerce")

# --- PASSO NOVO: Verificar e criar o banco de dados na nuvem ---
@st.cache_resource
def inicializar_banco():
    """Garante que o banco vetorial exista antes do agente ligar."""
    if not os.path.exists("./indice_vetorial"):
        with st.spinner("Primeiro acesso detectado: Baixando documentos e criando banco de dados..."):
            docs = carregar_documentos()
            chunks = dividir_em_chunks(docs)
            criar_indice(chunks)
        st.success("Banco de dados criado com sucesso!")

inicializar_banco()
# ----------------------------------------------------------------

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

    # O spinner dá um feedback visual enquanto o agente pensa
    with st.spinner("Procurando nos documentos..."):
        resposta = st.session_state.agente.invoke(pergunta)

    st.session_state.historico.append(("assistant", resposta))
    with st.chat_message("assistant"):
        st.markdown(resposta)