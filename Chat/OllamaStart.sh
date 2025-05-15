#!/bin/bash

echo "Starting the Ollama Server"
ollama serve &
echo "Waiting for Ollama downloads"
sleep 5 
ollama pull SpeakLeash/bielik-7b-instruct-v0.1-gguf:Q4_K_S

echo "Starting the Streamlit server"
streamlit run Chat.py --server.port=8501 --server.address=0.0.0.0