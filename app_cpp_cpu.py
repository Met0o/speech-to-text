import os
import sys
import time
import requests
import threading
import webbrowser
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

server_process = None
timer_running = False
start_time = None

def start_whisper_server():
    """
    Start the CPU-only Whisper server in a separate process.
    Returns the process object.
    """
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    internal_path = os.path.join(base_path, "_internal")
    if os.path.exists(internal_path):
        base_path = internal_path

    ffmpeg_path = os.path.join(base_path, "ffmpeg", "bin")
    os.environ["PATH"] += os.pathsep + ffmpeg_path

    exe_name = "whisper-server-cpu.exe"
    build_folder = "build_cpu"
    extra_args = []

    server_exe = os.path.join(base_path, "Release", build_folder, exe_name)
    model_path = os.path.join(base_path, "Release", build_folder, "models", "ggml-large-v3-turbo-q8_0.bin")

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
    Terminate any existing server process and start a new one.
    """
    global server_process
    if server_process is not None:
        try:
            server_process.terminate()
        except Exception:
            pass
        server_process = None

    server_process = start_whisper_server()

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

def update_timer():
    """
    Update the elapsed time (HH:MM:SS) in the transcription text widget.
    """
    if timer_running:
        elapsed = time.time() - start_time
        hrs, rem = divmod(elapsed, 3600)
        mins, secs = divmod(rem, 60)
        timer_text = f"Inference Duration: {int(hrs):02d}:{int(mins):02d}:{int(secs):02d}\n"
        current = transcription_text.get("1.0", tk.END)
        lines = current.split("\n")
        if lines and lines[0].startswith("Inference Duration:"):
            remaining_text = "\n".join(lines[1:])
        else:
            remaining_text = current
        transcription_text.delete("1.0", tk.END)
        transcription_text.insert(tk.END, timer_text + remaining_text)
        app.after(1000, update_timer)

def transcription_worker(audio_path):
    """
    Worker function to run in a separate thread.
    Calls the transcription service, then stops the timer and updates the GUI.
    """
    global timer_running
    try:
        result = transcribe_audio(audio_path)
        text = result.get("text", "No transcription available.")
    except Exception as e:
        text = f"Error: {e}"
    timer_running = False
    app.after(0, update_transcription_text, text)

def update_transcription_text(text):
    """
    Update the transcription text widget with the provided text.
    The timer line remains as the first line.
    """
    current = transcription_text.get("1.0", tk.END)
    lines = current.split("\n")
    if lines and lines[0].startswith("Inference Duration:"):
        timer_line = lines[0] + "\n"
    else:
        timer_line = ""
    formatted_text = text.replace("\n", " ").strip()
    transcription_text.delete("1.0", tk.END)
    transcription_text.insert(tk.END, timer_line + formatted_text)

def start_transcription():
    """
    Start the transcription process.
    Initialize and display the timer, then start a background thread.
    """
    global timer_running, start_time
    audio_path = audio_entry.get()
    if not audio_path:
        messagebox.showerror("Error", "Please select an audio file.")
        return

    start_time = time.time()
    timer_running = True
    transcription_text.delete("1.0", tk.END)
    transcription_text.insert(tk.END, "Inference Duration: 00:00:00\nTranscription in progress...")
    app.after(1000, update_timer)

    # Start transcription on a separate thread.
    thread = threading.Thread(target=transcription_worker, args=(audio_path,))
    thread.daemon = True
    thread.start()

def open_github_model_link(event):
    webbrowser.open("https://github.com/openai/whisper")

def open_github_dev_link(event):
    webbrowser.open("https://github.com/Met0o/speech-to-text")

def open_github_model_gerganov_link(event):
    webbrowser.open("https://github.com/ggerganov/whisper.cpp")

# ------------------- Tkinter GUI -------------------

app = tk.Tk()
app.title("Whisper Transcription")
app.configure(bg="#092642")
app.geometry("815x600")

app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)

dark_bg = "#092642"
dark_fg = "#ffffff"
entry_bg = "#3e3e3e"
button_bg = "#555555"
button_hover_bg = "#777777"
transcription_text_fg = "#000000"

# --- Top Frame: Audio File Input and Buttons ---
top_frame = tk.Frame(app, bg=dark_bg)
top_frame.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky="we")

input_label = tk.Label(top_frame, text="Input Audio File:", fg=dark_fg, bg=dark_bg)
input_label.pack(side=tk.LEFT, padx=5)

audio_entry = tk.Entry(top_frame, width=40, bg=entry_bg, fg=dark_fg, insertbackground=dark_fg)
audio_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

browse_btn = tk.Button(top_frame, text="Browse", bg=button_bg, fg=dark_fg, activebackground=button_hover_bg, command=select_audio_file)
browse_btn.pack(side=tk.LEFT, padx=5)

transcribe_btn = tk.Button(top_frame, text="Transcribe", bg=button_bg, fg=dark_fg, activebackground=button_hover_bg, command=start_transcription)
transcribe_btn.pack(side=tk.LEFT, padx=5)

save_btn = tk.Button(top_frame, text="Save Output", bg=button_bg, fg=dark_fg, activebackground=button_hover_bg, command=save_output)
save_btn.pack(side=tk.LEFT, padx=5)

# --- Transcription Output Text Widget ---
transcription_text = tk.Text(app, wrap="word", bg=dark_fg, fg=transcription_text_fg, insertbackground=transcription_text_fg)
transcription_text.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

# --- Links Frame ---
link_frame = tk.Frame(app, bg=dark_bg)
link_frame.grid(row=2, column=0, columnspan=5, pady=5)

github_model_link = tk.Label(link_frame, text="Based on OpenAI's Whisper Transformer architecture", fg="#ffffff", bg=button_bg, cursor="hand2")
github_model_link.pack(side=tk.LEFT, padx=5)
github_model_link.bind("<Button-1>", open_github_model_link)

github_gerganov_link = tk.Label(link_frame, text="Powered by Georgi Gerganov's ggml C++ backend", fg="#ffffff", bg=button_bg, cursor="hand2")
github_gerganov_link.pack(side=tk.LEFT, padx=5)
github_gerganov_link.bind("<Button-1>", open_github_model_gerganov_link)

github_dev_link = tk.Label(link_frame, text="Developed by Metodi Simeonov", fg="#ffffff", bg=button_bg, cursor="hand2")
github_dev_link.pack(side=tk.LEFT, padx=5)
github_dev_link.bind("<Button-1>", open_github_dev_link)

if __name__ == "__main__":
    server_process = start_whisper_server()
    try:
        app.mainloop()
    finally:
        if server_process is not None:
            server_process.terminate()
