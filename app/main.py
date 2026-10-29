from fastapi import FastAPI
import os

app = FastAPI(title="GitOps Demo App", version="2.0.0")

VERSION = os.getenv("APP_VERSION", "v2.0.0")

@app.get("/")
def read_root():
    return {
        "app": "demo-app",
        "version": VERSION,
        "message": "GitOps em acao! Atualizacao automatica via ArgoCD realizada com sucesso!"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": VERSION}
