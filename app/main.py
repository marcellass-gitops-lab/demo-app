import os
from fastapi import FastAPI

app = FastAPI(title="demo-app")

# Permite que a versão seja configurada via variável de ambiente no Deployment
APP_VERSION = os.getenv("APP_VERSION", "v1.0.0")

@app.get("/")
def read_root():
    return {
        "app": "demo-app",
        "version": APP_VERSION,
        "message": "Laboratório GitOps ativo e operante!"
    }

@app.get("/health")
def health_check():
    # Endpoint consumido pelos probes (liveness/readiness) do Kubernetes
    return {"status": "healthy", "version": APP_VERSION}
