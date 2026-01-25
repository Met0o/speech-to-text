import os
import time
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

WHISPER_BACKENDS = {
    "gpu": os.environ.get("WHISPER_GPU_URL", "http://whisper-gpu:8080"),
    "cpu": os.environ.get("WHISPER_CPU_URL", "http://whisper-cpu:8080"),
}

DEFAULT_BACKEND = os.environ.get("DEFAULT_BACKEND", "gpu")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    audio_file = request.files["file"]
    if audio_file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    
    language = request.form.get("language", "bg")
    backend = request.form.get("backend", DEFAULT_BACKEND)
    
    server_url = WHISPER_BACKENDS.get(backend, WHISPER_BACKENDS[DEFAULT_BACKEND])
    
    try:
        start_time = time.time()
        
        response = requests.post(
            f"{server_url}/inference",
            files={"file": (audio_file.filename, audio_file.stream, audio_file.mimetype)},
            data={"language": language}
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                "text": result.get("text", ""),
                "duration": f"{elapsed:.2f}s",
                "backend": backend
            })
        else:
            return jsonify({"error": f"Server error: {response.status_code}"}), 500
            
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cannot connect to Whisper server. Is it running?"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health")
def health():
    try:
        response = requests.get(f"{WHISPER_SERVER_URL}/", timeout=5)
        return jsonify({"status": "healthy", "server": "connected"})
    except:
        return jsonify({"status": "unhealthy", "server": "disconnected"}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
