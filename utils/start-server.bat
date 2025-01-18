@echo off
rem Start the Whisper server
start "" whisper-server.exe --host 127.0.0.1 --port 8080 -m "models/ggml-large-v3.bin" --convert -t 24 --ov-e-device CUDA -l bg

rem Start the main application
start "" main.exe
