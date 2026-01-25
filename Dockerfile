ARG USE_GPU=1
ARG BASE_IMAGE=nvidia/cuda:13.0.0-devel-ubuntu24.04

FROM ubuntu:22.04 AS base-cpu
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    sysstat \
    git \
    cmake \
    build-essential \
    wget \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

FROM nvidia/cuda:13.0.0-devel-ubuntu24.04 AS base-gpu
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    sysstat \
    git \
    cmake \
    build-essential \
    wget \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

FROM ${BASE_IMAGE} AS builder

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    git \
    cmake \
    build-essential \
    wget \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone https://github.com/ggerganov/whisper.cpp.git

WORKDIR /app/whisper.cpp

ARG USE_GPU=1
ARG CUDA_ARCH

ENV LIBRARY_PATH=/usr/local/cuda/lib64/stubs
RUN ln -sf /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/stubs/libcuda.so.1 2>/dev/null || true

RUN if [ "$USE_GPU" = "1" ]; then \
        echo "Building with CUDA support..."; \
        export LD_LIBRARY_PATH=/usr/local/cuda/lib64/stubs; \
        CMAKE_ARGS="-DGGML_CUDA=1 -DGGML_NATIVE=0"; \
        if [ -n "$CUDA_ARCH" ]; then \
            CMAKE_ARGS="$CMAKE_ARGS -DCMAKE_CUDA_ARCHITECTURES=$CUDA_ARCH"; \
        fi; \
        cmake -B build $CMAKE_ARGS; \
    else \
        echo "Building for CPU..."; \
        cmake -B build; \
    fi && \
    LD_LIBRARY_PATH=/usr/local/cuda/lib64/stubs cmake --build build --config Release -j $(nproc)

ENV LIBRARY_PATH=

RUN mkdir -p /app/bin && \
    cp build/bin/whisper-server /app/bin/whisper-server

WORKDIR /app
EXPOSE 8080

ENV MODEL_PATH=/app/models/ggml-large-v3-turbo-q8_0.bin

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
