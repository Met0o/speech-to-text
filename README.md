# Speech-to-Text Converter

A tool for converting audio files to text using the Whisper AI model.

## Installation

1. Install Visual Studio 2022 with C++ build tools, CMake, and CUDA Toolkit 12.6.
2. Clone the repository:
    ```bash
    git clone https://github.com/ggerganov/whisper.cpp.git
    ```
3. Create and navigate to the build directory:
    ```bash
    mkdir build
    cd build
    ```
4. Configure the project with CMake:
    ```bash
    cmake -B build -DGGML_CUDA=1 -DCUDAToolkit_ROOT="C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6" -DCudaToolkitDir="C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6" ..
    ```
5. Build the project:
    ```bash
    cmake --build build -j --config Release
    ```
6. Run the server:
    ```bash
    C:\dev\whisper.cpp\build\bin\Release\whisper-server.exe --host 127.0.0.1 --port 8080 -m "models/ggml-large-v3-turbo.bin" --convert -t 24 --ov-e-device CUDA -l bg
    ```

## Creating Executable

1. Create a standalone executable for `app_cpp.py`:
    ```bash
    pyinstaller --onefile --noconsole app_cpp.py
    ```
2. Alternatively, use the spec file:
    ```bash
    pyinstaller app_cpp.spec
    ```

## Project Structure

```bash
speech-to-text/
  ├── app_cpp.py
  ├── Release/
  │   ├── build_cpu/
  │   │   ├── models/
  │   │   │   └── ggml-large-v3.bin
  │   │   └── whisper-server-cpu.exe
  │   ├── build_gpu/
  │   │   ├── models/
  │   │   │   └── ggml-large-v3.bin
  │   │   └── whisper-server-gpu.exe
 
```