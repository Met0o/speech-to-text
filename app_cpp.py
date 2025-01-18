import requests
import tkinter as tk
from tkinter import filedialog, messagebox


# git clone https://github.com/ggerganov/whisper.cpp.git
# mkdir build
# cd build
# cmake -B build -DGGML_CUDA=1 -DCUDAToolkit_ROOT="C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6" -DCudaToolkitDir="C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6" ..
# cmake --build build -j --config Release
# C:\dev\whisper.cpp\build\bin\Release>whisper-server.exe --host 127.0.0.1 --port 8080 -m "models/ggml-large-v3-turbo.bin" --convert -t 24 --ov-e-device CUDA -l bg


def transcribe_audio(audio_path, model_path="ggml-large-v3-turbo.bin", host="127.0.0.1", port=8080):
    """
    Send an audio file to the whisper server for transcription.
    """
    url = f"http://{host}:{port}/inference"
    with open(audio_path, 'rb') as audio_file:
        files = {
            "file": audio_file,
            "model": (None, model_path),
            "language": (None, "bg")
        }
        response = requests.post(url, files=files)
    if response.status_code == 200:
        return response.json()
    else:
        raise RuntimeError(f"Server error: {response.status_code}, {response.text}")

def select_audio_file():
    """
    Prompt the user to select an audio file.
    """
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
    if file_path:
        audio_entry.delete(0, tk.END)
        audio_entry.insert(0, file_path)

def start_transcription():
    """
    Start transcription process and display results.
    """
    audio_path = audio_entry.get()
    if not audio_path:
        messagebox.showerror("Error", "Please select an audio file.")
        return

    try:
        result = transcribe_audio(audio_path)
        transcription_text.delete(1.0, tk.END)
        transcription_text.insert(tk.END, result.get("text", "No transcription available."))
    except Exception as e:
        messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("Whisper Transcription")

tk.Label(app, text="Audio File:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
audio_entry = tk.Entry(app, width=50)
audio_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(app, text="Browse", command=select_audio_file).grid(row=0, column=2, padx=10, pady=10)

tk.Button(app, text="Transcribe", command=start_transcription, bg="lightblue").grid(row=1, column=1, pady=10)

transcription_text = tk.Text(app, width=60, height=15, wrap="word")
transcription_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

app.mainloop()
