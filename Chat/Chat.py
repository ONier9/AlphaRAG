__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
import RagMain


# Krótki kod komunikatora za pomocą streamlit, głównie w celach prezentacyjnych 

st.set_page_config(page_title="RagChat", page_icon="🤖")
st.title("Rag Sample Chat")
st.caption("Prosty System Rag")

if "query_engine" not in st.session_state:
    with st.spinner("Inicjalizacja systemu AI..."):
        st.session_state.query_engine = RagMain.initialize()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Cześć! Zadawaj mi pytania o mojej firmie!"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Wpisz swoje pytanie..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    # Tutaj warto zobaczyć jak dołączamy kod do naszego silnika 
    with st.chat_message("assistant"):
        response_container = st.empty()
        with st.spinner("Czekaj na odpowiedź...", show_time=True):
            full_response = ""
            query_engine = st.session_state.query_engine
            response = query_engine.query(prompt)
            full_response = response.response
            response_container.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})