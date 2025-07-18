import subprocess
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests

# Gestion du cycle de vie de l'application
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Démarrage - Démarrer Ollama
    subprocess.Popen(["ollama", "serve"])
    time.sleep(5)
    subprocess.run(["ollama", "create", "alty-llm", "-f", "model-alty"])
    yield
    # Arrêt - Nettoyage si nécessaire
    pass

app = FastAPI(lifespan=lifespan)

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

@app.get("/")
def read_root():
    return {"message": "LLM Alty API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
