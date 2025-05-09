import streamlit as st
import Ollama
from llama_index.core.llms import ChatMessage


st.title("RAG System Chatbot")
st.write("Ask me anything!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = Ollama.get_ollama_response(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})