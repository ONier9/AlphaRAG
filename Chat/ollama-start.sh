#!/bin/bash
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_NUM_PARALLEL=1       
export OLLAMA_CPU=true
export OLLAMA_HOST=0.0.0.0:11434

ollama serve &
ollama list

until curl -s http://localhost:11434/api/tags > /dev/null; do
  sleep 1
done
if  ollama list | grep -q "bielik-7b-instruct"; then
  echo "Removing Bielik model..."
  ollama remove hf.co/speakleash/Bielik-7B-Instruct-v0.1-GGUF:Q2_K
fi
if ! ollama list | grep -q "herbert"; then
  echo "Pulling klej model..."
  FROM ./herbert-base-cased.gguf
  ollama create herbert -f Modelfile
  ollama run herbert
fi

if ! ollama list | grep -q "nomic-embed-text"; then
  echo "Pulling Nomic Embed Text model..."
  ollama pull nomic-embed-text
fi

curl -X POST http://localhost:11434/api/default \
  -H "Content-Type: application/json" \
  -d '{"model": "allegro/klej-herbert-base"}'

streamlit run Chat.py --server.port=8501 --server.address=0.0.0.0