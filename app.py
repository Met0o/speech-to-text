import os
import sys
import torch
import whisper
import threading
import webbrowser
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox, END
import tkinter.font as tkFont

# pyinstaller --onedir --noconsole --add-data "ffmpeg;ffmpeg" --add-data "models;models" app.py

if getattr(sys, 'frozen', False):
    project_dir = sys._MEIPASS
else:
    project_dir = os.path.dirname(os.path.abspath(__file__))

ffmpeg_path = os.path.join(project_dir, "ffmpeg", "bin")
os.environ["PATH"] += os.pathsep + ffmpeg_path

models_dir = os.path.join(project_dir, "models")
available_models = {
    "Whisper Large (Slow, precise)": "large-v3.pt",
    "Whisper Turbo (Fast, less precise)": "large-v3-turbo.pt"
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
    root.update()

    def perform_transcription():
        try:

            label_status.config(text="Loading model, please wait...")
            root.update()
            model = whisper.load_model(model_path, device=device)

            label_status.config(text="Transcribing audio... Please wait.")
            root.update()
            result = model.transcribe(file_path, language="bg")
            transcription = result["text"]

            text_output.delete(1.0, END)
            text_output.insert(END, transcription)
            label_status.config(text="Transcription complete!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            label_status.config(text="Error during transcription.")

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

root = ttk.Window(themename="darkly")
root.title("Bulgarian Speech-to-Text Transcription Application")
root.geometry("1024x768")
root.style.configure("TFrame", background="#092642")
root.style.configure("TLabel", background="#092642", foreground="#559CE4")
root.style.configure("TButton", background="#559CE4", foreground="white", font=("Helvetica", 10))

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

button_frame = ttk.Frame(root, padding=10)
button_frame.grid(row=0, column=0, pady=5, sticky="ew")

ttk.Button(button_frame, text="Select Audio File", command=transcribe_file, bootstyle=PRIMARY).pack(side='left', padx=5)
ttk.Button(button_frame, text="Save Output", command=save_output, bootstyle=SUCCESS).pack(side='left', padx=5)
ttk.Label(button_frame, text="Select Model:", bootstyle="inverse").pack(side='left', padx=5)

model_combobox = ttk.Combobox(button_frame, values=list(available_models.keys()), state="readonly", width=35)
model_combobox.pack(side='left', padx=5)
model_combobox.set(list(available_models.keys())[0])  # Set first model as default

status_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
label_status = ttk.Label(root, text="Status: Idle", font=status_font, bootstyle="info")
label_status.grid(row=2, column=0, pady=5)

text_frame = ttk.Frame(root, padding=10)
text_frame.grid(row=1, column=0, sticky="nsew", padx=5)
text_frame.grid_rowconfigure(0, weight=1)
text_frame.grid_columnconfigure(0, weight=1)

text_output = ttk.Text(text_frame, wrap="word", height=20, width=80, font=("Helvetica", 10))
text_output.grid(row=0, column=0, sticky="nsew")

scrollb = ttk.Scrollbar(text_frame, command=text_output.yview)
scrollb.grid(row=0, column=1, sticky="ns")
text_output['yscrollcommand'] = scrollb.set

link_frame = ttk.Frame(root, padding=10)
link_frame.grid(row=4, column=0, pady=5)

underline_font = tkFont.Font(family="Helvetica", size=10, underline=True)
github_model_link = ttk.Label(link_frame, text="Powered by OpenAI Whisper", foreground="#559CE4", cursor="hand2", font=underline_font)
github_model_link.pack(pady=2)
github_model_link.bind("<Button-1>", open_github_model_link)

github_dev_link = ttk.Label(link_frame, text="Developed by Metodi Simeonov", foreground="#559CE4", cursor="hand2", font=underline_font)
github_dev_link.pack(pady=2)
github_dev_link.bind("<Button-1>", open_github_dev_link)

root.mainloop()
