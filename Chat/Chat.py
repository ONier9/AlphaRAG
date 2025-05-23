import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
import RagMain
import time
from llama_index.core.llms import ChatMessage

st.set_page_config(page_title="RagChat", page_icon="🤖")
st.title("Rag Sample Chat")
st.caption("Prosty System Rag")

if "query_engine" not in st.session_state:
    with st.spinner("Inicjalizacja systemu AI..."):
        st.session_state.query_engine = RagMain.initialize()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Cześć! Zadawaj mi pytania o dokumentację techniczną!"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Wpisz swoje pytanie..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        query_engine = st.session_state.query_engine
        response = query_engine.query(prompt)
        full_response = response.response
        response_container.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})