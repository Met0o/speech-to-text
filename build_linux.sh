#!/bin/bash
set -e

if [ ! -d "whisper.cpp" ]; then
    echo "Cloning whisper.cpp..."
    git clone https://github.com/ggerganov/whisper.cpp.git
fi

mkdir -p Release/build_cpu/models

cd whisper.cpp
echo "Building whisper.cpp..."
cmake -B build -DGGML_NACTIVE=1
cmake --build build --config Release -j $(nproc)

if [ -f "build/bin/server" ]; then
    cp build/bin/server ../Release/build_cpu/whisper-server-cpu
elif [ -f "build/bin/whisper-server" ]; then
    cp build/bin/whisper-server ../Release/build_cpu/whisper-server-cpu
else
    echo "Error: Could not find server executable in whisper.cpp/build/bin/"
    exit 1
fi

cd ..

echo "Build complete. Please place your model file in Release/build_cpu/models/"
echo "You can download a model using: wget -P Release/build_cpu/models/ https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q8_0.bin"
