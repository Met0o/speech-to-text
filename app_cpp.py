# Install VS 2022 with C++ build tools, CMake, and CUDA Toolkit 12.6
# git clone https://github.com/ggerganov/whisper.cpp.git
# mkdir build
# cd build
# cmake -B build -DGGML_CUDA=1 -DCUDAToolkit_ROOT="C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6" -DCudaToolkitDir="C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6" ..
# cmake --build build -j --config Release
# C:\dev\whisper.cpp\build\bin\Release>whisper-server.exe --host 127.0.0.1 --port 8080 -m "models/ggml-large-v3-turbo.bin" --convert -t 24 --ov-e-device CUDA -l bg

import requests
import threading
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox

def transcribe_audio(audio_path, model_path="ggml-large-v3.bin", host="127.0.0.1", port=8080):
    """
    Send an audio file to the Whisper server for transcription.
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

def transcription_worker(audio_path):
    """
    Worker function to run in a separate thread.
    It calls the transcribe_audio() function and then schedules an update
    of the GUI with the transcription result.
    """
    try:
        result = transcribe_audio(audio_path)
        text = result.get("text", "No transcription available.")
    except Exception as e:
        text = f"Error: {e}"
    # Schedule the update of the GUI on the main thread
    app.after(0, update_transcription_text, text)

def update_transcription_text(text):
    """
    Update the transcription text widget with the provided text.
    """
    transcription_text.delete(1.0, tk.END)
    transcription_text.insert(tk.END, text)

def start_transcription():
    """
    Start transcription process and display results in a separate thread.
    """
    audio_path = audio_entry.get()
    if not audio_path:
        messagebox.showerror("Error", "Please select an audio file.")
        return

    transcription_text.delete(1.0, tk.END)
    transcription_text.insert(tk.END, "Transcription in progress...")

    # Start the transcription in a new thread
    thread = threading.Thread(target=transcription_worker, args=(audio_path,))
    thread.daemon = True
    thread.start()

def open_github_model_link(event):
    webbrowser.open("https://github.com/openai/whisper")
    
def open_github_dev_link(event):
    webbrowser.open("https://github.com/Met0o")

def open_github_model_gerganov_link(event):
    webbrowser.open("https://github.com/ggerganov/whisper.cpp")

# ------------------- Tkinter GUI -------------------

app = tk.Tk()
app.title("Whisper Transcription")
app.configure(bg="#092642")
app.geometry("800x600")

app.grid_rowconfigure(2, weight=1)
app.grid_columnconfigure(1, weight=1)

dark_bg = "#092642"
dark_fg = "#ffffff"
entry_bg = "#3e3e3e"
button_bg = "#555555"
button_hover_bg = "#777777"

# Row 0: File input, Browse, and Transcribe controls
tk.Label(app, text="Input Audio File:", fg=dark_fg, bg=dark_bg)\
    .grid(row=0, column=0, padx=10, pady=10, sticky="e")

audio_entry = tk.Entry(app, width=50, bg=entry_bg, fg=dark_fg, insertbackground=dark_fg)
audio_entry.grid(row=0, column=1, padx=10, pady=10, sticky="we")

tk.Button(app, text="Browse", bg=button_bg, fg=dark_fg, activebackground=button_hover_bg,
          command=select_audio_file).grid(row=0, column=2, padx=10, pady=10)

tk.Button(app, text="Transcribe", bg=button_bg, fg=dark_fg, activebackground=button_hover_bg,
          command=start_transcription).grid(row=0, column=3, padx=10, pady=10)

# Row 2: Transcription Output Text Widget
transcription_text = tk.Text(app, wrap="word", bg=entry_bg, fg=dark_fg, insertbackground=dark_fg)
transcription_text.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Row 3: Links frame
link_frame = tk.Frame(app, bg=dark_bg)
link_frame.grid(row=3, column=0, columnspan=4, pady=5)

github_model_link = tk.Label(link_frame,
                             text="Based on OpenAI's Whisper Transformer architecture",
                             fg="#ffffff", bg=button_bg, cursor="hand2")
github_model_link.pack(side=tk.LEFT, padx=5)
github_model_link.bind("<Button-1>", open_github_model_link)

github_dev_link = tk.Label(link_frame,
                           text="Powered by Georgi Gerganov's ggml C++ backend",
                           fg="#ffffff", bg=button_bg, cursor="hand2")
github_dev_link.pack(side=tk.LEFT, padx=5)
github_dev_link.bind("<Button-1>", open_github_model_gerganov_link)

github_dev_link = tk.Label(link_frame,
                           text="Developed by Metodi Simeonov",
                           fg="#ffffff", bg=button_bg, cursor="hand2")
github_dev_link.pack(side=tk.LEFT, padx=5)
github_dev_link.bind("<Button-1>", open_github_dev_link)

app.mainloop()


# import requests
# import tkinter as tk
# from tkinter import filedialog, messagebox

# def transcribe_audio(audio_path, model_path="ggml-large-v3.bin", host="127.0.0.1", port=8080):
#     """
#     Send an audio file to the whisper server for transcription.
#     """
#     url = f"http://{host}:{port}/inference"
#     with open(audio_path, 'rb') as audio_file:
#         files = {
#             "file": audio_file,
#             "model": (None, model_path),
#             "language": (None, "bg")
#         }
#         response = requests.post(url, files=files)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         raise RuntimeError(f"Server error: {response.status_code}, {response.text}")

# def select_audio_file():
#     """
#     Prompt the user to select an audio file.
#     """
#     file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
#     if file_path:
#         audio_entry.delete(0, tk.END)
#         audio_entry.insert(0, file_path)

# def start_transcription():
#     """
#     Start transcription process and display results.
#     """
#     audio_path = audio_entry.get()
#     if not audio_path:
#         messagebox.showerror("Error", "Please select an audio file.")
#         return

#     try:
#         result = transcribe_audio(audio_path)
#         transcription_text.delete(1.0, tk.END)
#         transcription_text.insert(tk.END, result.get("text", "No transcription available."))
#     except Exception as e:
#         messagebox.showerror("Error", str(e))

# app = tk.Tk()
# app.title("Whisper Transcription to Bulgarian")

# tk.Label(app, text="Audio File:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
# audio_entry = tk.Entry(app, width=50)
# audio_entry.grid(row=0, column=1, padx=10, pady=10)
# tk.Button(app, text="Browse", command=select_audio_file).grid(row=0, column=2, padx=10, pady=10)

# tk.Button(app, text="Transcribe", command=start_transcription, bg="lightblue").grid(row=1, column=1, pady=10)

# transcription_text = tk.Text(app, width=60, height=15, wrap="word")
# transcription_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

# app.mainloop()
