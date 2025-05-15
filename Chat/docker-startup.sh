#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: ./docker-startup <build/deploy/deploy-gpu>"
  exit 
fi

if [ "$1" = "build" ]; then
  docker build -t rag-app .
elif [ "$1" = "deploy" ]; then
  docker run --rm --name rag-app -v $PWD:/root -p 11434:11434 -p 8501:8501 -it rag-app
elif [ "$1" = "deploy-gpu" ]; then
  docker run --rm --name rag-app -d --gpus=all -v $PWD:/root -p 11434:11434 -p 8501:8501 -it rag-app
fi