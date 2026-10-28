# Imagem base oficial leve do Python
FROM python:3.11-slim

# Evita arquivos compilados desnecessários (.pyc) e força logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalação das dependências isolada para acelerar o cache de camadas do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Criação de usuário não-root (boa prática obrigatória de segurança em Kubernetes)
RUN useradd -u 1000 appuser && chown -R appuser /app
USER appuser

# Cópia do código-fonte
COPY --chown=appuser:appuser app/ ./app/

EXPOSE 8000

# Execução do servidor HTTP assíncrono escutando em todas as interfaces internas
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
