#!/bin/bash

# Usage: ./run_docker.sh [cpu|gpu] [model_variant]
MODE=${1:-gpu}
MODEL_VARIANT=${2:-q8_0}

MODEL_DIR="Release/build_cpu/models"
MODEL_FILENAME="ggml-large-v3-turbo-${MODEL_VARIANT}.bin"
MODEL_URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/${MODEL_FILENAME}"

MODEL_FILE="${MODEL_DIR}/${MODEL_FILENAME}"

if [ ! -f "$MODEL_FILE" ]; then
    echo "Model file not found: $MODEL_FILE"
    echo "Downloading model (${MODEL_VARIANT})..."
    mkdir -p "$MODEL_DIR"
    wget -O "$MODEL_FILE" "$MODEL_URL"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to download model. Check if variant '${MODEL_VARIANT}' exists."
        rm -f "$MODEL_FILE"
        exit 1
    fi
    echo "Download complete."
else
    echo "Model found: $MODEL_FILE"
fi

export MODEL_FILENAME

if [ "$MODE" == "gpu" ]; then
    echo "Starting Whisper Server with GPU support..."
    docker-compose up --build whisper-gpu
else
    echo "Starting Whisper Server with CPU support..."
    docker-compose up --build whisper-cpu
fi
