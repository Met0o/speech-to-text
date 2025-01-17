import requests

# C:\dev\whisper.cpp\build\bin\Release>whisper-server.exe --host 127.0.0.1 --port 8080 -m "models/ggml-large-v3-turbo-q8_0.bin" --convert -t 24
# whisper-server.exe --host 127.0.0.1 --port 8080 -m "models/ggml-large-v3-turbo.bin" --convert -t 24 --ov-e-device CUDA:0 -l bg

def transcribe_audio(audio_path, model_path="ggml-large-v3-turbo.bin", host="127.0.0.1", port=8080):
    
    url = f"http://{host}:{port}/inference"
    
    with open(audio_path, 'rb') as audio_file:
        files = {
            "file": audio_file,
            "model": (None, model_path),
        }
        response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json()
    else:
        raise RuntimeError(f"Server error: {response.status_code}, {response.text}")

try:
    result = transcribe_audio("output.wav")
    print("Transcription result:", result)
except Exception as e:
    print("Error:", e)
