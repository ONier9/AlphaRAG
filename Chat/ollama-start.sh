#!/bin/bash

export OLLAMA_HOST=0.0.0.0:11434

ollama serve &

until curl -s http://localhost:11434/api/tags > /dev/null; do
  sleep 1
done

if ! ollama list | grep -q "bielik-7b-instruct"; then
  echo "Pulling Bielik model..."
  ollama pull SpeakLeash/bielik-7b-instruct-v0.1-gguf:Q4_K_S
fi

curl -X POST http://localhost:11434/api/default \
  -H "Content-Type: application/json" \
  -d '{"model": "SpeakLeash/bielik-7b-instruct-v0.1-gguf:Q4_K_S"}'

streamlit run Chat.py --server.port=8501 --server.address=0.0.0.0