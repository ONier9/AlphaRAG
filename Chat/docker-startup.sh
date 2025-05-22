#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: ./docker-startup <build/deploy/stop>"
  exit 
fi

if [ "$1" = "build" ]; then
  docker build -t rag-app .
elif [ "$1" = "deploy" ]; then
  # Remove GPU flags and CUDA volume
  docker run --rm --name rag-app \
    -v $PWD:/app \
    -v ollama_models:/root/.ollama \
    -p 11434:11434 -p 8501:8501 \
    -it rag-app
elif [ "$1" = "stop" ]; then
  docker container stop rag-app
fi