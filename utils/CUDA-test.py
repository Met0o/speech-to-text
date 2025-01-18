import torch
import whisper

print(torch.__version__)
print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU found")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

model = whisper.load_model("large-v3", device=device)
print("Successfully loaded{model}")

result = model.transcribe("11min.mp3")
print(result["text"])

# [
    # 'tiny.en', 
    # 'tiny', 
    # 'base.en', '
    # base', 
    # 'small.en', 
    # 'small', 
    # 'medium.en', 
    # 'medium', 
    # 'large-v1', 
    # 'large-v2', 
    # 'large-v3', 
    # 'large', 
    # 'large-v3-turbo', 
    # 'turbo'
# ]