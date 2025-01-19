import os
import sys
import requests
import threading
import webbrowser
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

# Install VS 2022 with C++ build tools, CMake, and CUDA Toolkit 12.6
# git clone https://github.com/ggerganov/whisper.cpp.git
# mkdir build
# cd build
# cmake -B build -DGGML_CUDA=1 -DCUDAToolkit_ROOT="C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6" -DCudaToolkitDir="C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6" ..
# cmake --build build -j --config Release
# C:\dev\whisper.cpp\build\bin\Release>whisper-server.exe --host 127.0.0.1 --port 8080 -m "models/ggml-large-v3-turbo-q8_0.bin" --convert -t 24 --ov-e-device CUDA -l bg


server_process = None

def start_whisper_server(device="cpu"):
    """
    Start the Whisper server in a separate process (CPU or GPU).
    Returns the process object.
    """
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    internal_path = os.path.join(base_path, "_internal")
    if os.path.exists(internal_path):
        base_path = internal_path

    if device == "gpu":
        exe_name = "whisper-server-gpu.exe"
        build_folder = "build_gpu"
        extra_args = ["--ov-e-device", "CUDA"]
    else:
        exe_name = "whisper-server-cpu.exe"
        build_folder = "build_cpu"
        extra_args = []

    server_exe = os.path.join(base_path, "Release", build_folder, exe_name)
    model_path = os.path.join(
        base_path, "Release", build_folder, "models", "ggml-large-v3-turbo-q8_0.bin"
    )

    cmd = [
        server_exe,
        "--host", "127.0.0.1",
        "--port", "8080",
        "-m", model_path,
        "--convert",
        "-t", "24",
        "-l", "bg"
    ]

    cmd.extend(extra_args)

    creation_flags = 0
    if sys.platform.startswith("win"):
        creation_flags = subprocess.CREATE_NO_WINDOW

    return subprocess.Popen(cmd, creationflags=creation_flags)

def restart_whisper_server(*args):
    """
    Terminate existing server (if any) and start a new one
    with the selected device (cpu/gpu).
    """
    global server_process
    device = device_var.get()

    if server_process is not None:
        try:
            server_process.terminate()
        except Exception:
            pass
        server_process = None

    server_process = start_whisper_server(device=device)

def transcribe_audio(audio_path, model_path="ggml-large-v3-turbo-q8_0.bin", host="127.0.0.1", port=8080):
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
    file_path = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.wav *.mp3 *.ogg *.flac *.m4a")]
    )
    if file_path:
        audio_entry.delete(0, tk.END)
        audio_entry.insert(0, file_path)

def save_output():
    """
    Prompt the user to select a location to save the transcription output.
    """
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )
    if file_path:
        text = transcription_text.get("1.0", tk.END)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Success", "Output saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")

def transcription_worker(audio_path):
    """
    Worker function to run in a separate thread.
    It calls the transcribe_audio() function and then schedules
    an update of the GUI with the transcription result.
    """
    try:
        result = transcribe_audio(audio_path)
        text = result.get("text", "No transcription available.")
    except Exception as e:
        text = f"Error: {e}"

    app.after(0, update_transcription_text, text)

def update_transcription_text(text):
    """
    Update the transcription text widget with the provided text.
    """
    formatted_text = text.replace("\n", " ").strip()
    transcription_text.delete("1.0", tk.END)
    transcription_text.insert(tk.END, formatted_text)

def start_transcription():
    """
    Start transcription process and display results in a separate thread.
    """
    audio_path = audio_entry.get()
    if not audio_path:
        messagebox.showerror("Error", "Please select an audio file.")
        return

    transcription_text.delete("1.0", tk.END)
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

# Let row 1 (the transcription text) and column 0 expand
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)

dark_bg = "#092642"
dark_fg = "#ffffff"
entry_bg = "#3e3e3e"
button_bg = "#555555"
button_hover_bg = "#777777"
transcription_text_fg = "#000000"

# --- 1) Top Frame for CPU/GPU radio + audio input + buttons on the same line ---
top_frame = tk.Frame(app, bg=dark_bg)
top_frame.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="we")

device_var = tk.StringVar()
device_var.set("cpu")

# Device selection label
device_label = tk.Label(top_frame, text="Select Device:", fg=dark_fg, bg=dark_bg)
device_label.pack(side=tk.LEFT, padx=5)

# CPU radio
cpu_radio = tk.Radiobutton(
    top_frame, text="CPU", variable=device_var, value="cpu",
    fg=dark_fg, bg=dark_bg, selectcolor=dark_bg,
    command=restart_whisper_server
)
cpu_radio.pack(side=tk.LEFT, padx=2)

# GPU radio
gpu_radio = tk.Radiobutton(
    top_frame, text="GPU", variable=device_var, value="gpu",
    fg=dark_fg, bg=dark_bg, selectcolor=dark_bg,
    command=restart_whisper_server
)
gpu_radio.pack(side=tk.LEFT, padx=2)

# Input Audio File label
input_label = tk.Label(top_frame, text="Input Audio File:", fg=dark_fg, bg=dark_bg)
input_label.pack(side=tk.LEFT, padx=15)

# Audio entry field
audio_entry = tk.Entry(top_frame, width=40, bg=entry_bg, fg=dark_fg, insertbackground=dark_fg)
audio_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

# "Browse" button
browse_btn = tk.Button(top_frame, text="Browse", bg=button_bg, fg=dark_fg,
                       activebackground=button_hover_bg, command=select_audio_file)
browse_btn.pack(side=tk.LEFT, padx=5)

# "Transcribe" button
transcribe_btn = tk.Button(top_frame, text="Transcribe", bg=button_bg, fg=dark_fg,
                           activebackground=button_hover_bg, command=start_transcription)
transcribe_btn.pack(side=tk.LEFT, padx=5)

# "Save Output" button
save_btn = tk.Button(top_frame, text="Save Output", bg=button_bg, fg=dark_fg,
                     activebackground=button_hover_bg, command=save_output)
save_btn.pack(side=tk.LEFT, padx=5)

# --- 2) Transcription Output Text Widget (in row=1) ---
transcription_text = tk.Text(
    app, wrap="word", bg=dark_fg, fg=transcription_text_fg, insertbackground=transcription_text_fg
)
transcription_text.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

# --- 3) Links frame (in row=2) ---
link_frame = tk.Frame(app, bg=dark_bg)
link_frame.grid(row=2, column=0, columnspan=5, pady=5)

github_model_link = tk.Label(
    link_frame,
    text="Based on OpenAI's Whisper Transformer architecture",
    fg="#ffffff", bg=button_bg, cursor="hand2"
)
github_model_link.pack(side=tk.LEFT, padx=5)
github_model_link.bind("<Button-1>", open_github_model_link)

github_gerganov_link = tk.Label(
    link_frame,
    text="Powered by Georgi Gerganov's ggml C++ backend",
    fg="#ffffff", bg=button_bg, cursor="hand2"
)
github_gerganov_link.pack(side=tk.LEFT, padx=5)
github_gerganov_link.bind("<Button-1>", open_github_model_gerganov_link)

github_dev_link = tk.Label(
    link_frame, text="Developed by Metodi Simeonov",
    fg="#ffffff", bg=button_bg, cursor="hand2"
)
github_dev_link.pack(side=tk.LEFT, padx=5)
github_dev_link.bind("<Button-1>", open_github_dev_link)

if __name__ == "__main__":
    server_process = start_whisper_server(device_var.get())
    try:
        app.mainloop()
    finally:
        if server_process is not None:
            server_process.terminate()

