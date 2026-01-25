#!/bin/bash
set -e

unset LIBRARY_PATH

SERVER_BIN="/app/bin/whisper-server"

if [ ! -f "$MODEL_PATH" ]; then
    echo "WARNING: Model file not found at $MODEL_PATH"
    echo "Please mount a volume to /app/models containing the model file."
    echo "Example: -v ./models:/app/models"
    exit 1
fi

echo "Starting Whisper Server..."
echo "Model: $MODEL_PATH"

THREADS=$(nproc)
echo "Using $THREADS threads"

if [ $# -eq 0 ]; then
    exec "$SERVER_BIN" --host 0.0.0.0 --port 8080 -m "$MODEL_PATH" --convert -t "$THREADS" -l bg
else
    exec "$SERVER_BIN" --host 0.0.0.0 --port 8080 -m "$MODEL_PATH" "$@"
fi
