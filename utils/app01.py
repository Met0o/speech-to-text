import os
import sys
import time
import torch
import whisper
import threading
import webbrowser

from tkinter import ttk
from tkinter import Tk, filedialog, Label, Button, Text, END, messagebox

# pyinstaller --onefile --noconsole --add-data "ffmpeg;ffmpeg" --add-data "models;models" app.py

if getattr(sys, 'frozen', False):
    project_dir = sys._MEIPASS
else:
    project_dir = os.path.dirname(os.path.abspath(__file__))

ffmpeg_path = os.path.join(project_dir, "ffmpeg", "bin")
os.environ["PATH"] += os.pathsep + ffmpeg_path

models_dir = os.path.join(project_dir, "models")
available_models = {
    "Whisper-Large (Slow, precise)" : "large-v3.pt",
    "Whisper-Turbo (Fast, less precise)" : "large-v3-turbo.pt"
}

def transcribe_file():

    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.m4a")])
    if not file_path:
        return

    selected_model = model_combobox.get()
    if not selected_model or selected_model not in available_models:
        messagebox.showerror("Error", "Please select a valid model before transcribing.")
        return

    model_filename = available_models[selected_model]
    model_path = os.path.join(models_dir, model_filename)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    label_status.config(text=f"Preparing to load model '{selected_model}' on {device.upper()}, please wait...")
    progress_bar.grid(row=3, column=0, pady=5, sticky="ew")
    progress_bar.config(mode="determinate", maximum=100)
    progress_bar["value"] = 0
    root.update()

    def perform_transcription():
        try:
            progress_bar["value"] = 10
            root.update()
            time.sleep(0.5)
            model = whisper.load_model(model_path, device=device)

            label_status.config(text="Transcribing... Please wait.")
            for i in range(11, 90, 10):
                progress_bar["value"] = i
                root.update()
                time.sleep(0.5)

            result = model.transcribe(file_path, language="bg")
            transcription = result["text"]

            progress_bar["value"] = 100
            text_output.delete(1.0, END)
            text_output.insert(END, transcription)
            label_status.config(text="Transcription complete!")
            root.update()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            label_status.config(text="Error during transcription.")
        finally:
            progress_bar.stop()
            progress_bar.grid_remove()

    threading.Thread(target=perform_transcription).start()

def save_output():

    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if not file_path:
        return
    
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text_output.get(1.0, END))
        messagebox.showinfo("Success", "File saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def open_github_model_link(event):
    webbrowser.open("https://github.com/openai/whisper")
    
def open_github_dev_link(event):
    webbrowser.open("https://github.com/Met0o")

root = Tk()
root.title("Bulgarian Speech-to-Text Transcription Application")
root.geometry("1024x768")

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

button_frame = ttk.Frame(root)
button_frame.grid(row=0, column=0, pady=5, sticky="ew")

Button(button_frame, text="Select Audio File", command=transcribe_file, width=20).pack(side='left', padx=5)
Button(button_frame, text="Save Output", command=save_output, width=20).pack(side='left', padx=5)
Label(button_frame, text="Select Model:").pack(side='left', padx=5)

model_combobox = ttk.Combobox(button_frame, values=list(available_models.keys()), state="readonly", width=35)
model_combobox.pack(side='left', padx=5)
model_combobox.set(list(available_models.keys())[0])

label_status = Label(root, text="Status: Idle", font=("Arial", 10))
label_status.grid(row=2, column=0, pady=5)

progress_bar = ttk.Progressbar(root, mode='indeterminate')

text_frame = ttk.Frame(root)
text_frame.grid(row=1, column=0, sticky="nsew", padx=5)
text_frame.grid_rowconfigure(0, weight=1)
text_frame.grid_columnconfigure(0, weight=1)

text_output = Text(text_frame, wrap="word")
text_output.grid(row=0, column=0, sticky="nsew")

scrollb = ttk.Scrollbar(text_frame, command=text_output.yview)
scrollb.grid(row=0, column=1, sticky="ns")
text_output['yscrollcommand'] = scrollb.set

link_frame = ttk.Frame(root)
link_frame.grid(row=4, column=0, pady=5)

github_model_link = Label(link_frame, text="Powered by OpenAI Whisper", fg="blue", cursor="hand2")
github_model_link.pack(pady=2)
github_model_link.bind("<Button-1>", open_github_model_link)

github_dev_link = Label(link_frame, text="Developed by Metodi Simeonov", fg="blue", cursor="hand2")
github_dev_link.pack(pady=2)
github_dev_link.bind("<Button-1>", open_github_dev_link)

root.mainloop()
