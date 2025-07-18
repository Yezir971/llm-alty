import subprocess
import time
from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests

app = FastAPI()

# Démarrer Ollama au lancement de l'app
@app.on_event("startup")
def start_ollama():
    subprocess.Popen(["ollama", "serve"])
    time.sleep(5)
    subprocess.run(["ollama", "create", "alty-llm", "-f", "model-alty"])  

# Définir le format attendu
class GenerateRequest(BaseModel):
    prompt: str

@app.post("/api/generate")
def generate(req: GenerateRequest):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "alty-llm", "prompt": req.prompt, "stream": False}
    )
    return response.json()
