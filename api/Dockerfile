# api/Dockerfile
FROM python:3.11-slim

# 1) Fijamos carpeta de trabajo DENTRO de la imagen
WORKDIR /app

# 2) Dependencias del sistema (solo si alguna lib lo necesita). Mantener mínimo.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl git && \
    rm -rf /var/lib/apt/lists/*

# 3) Copiamos SOLO requirements para maximizar la caché de pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copiamos el resto del código (tu árbol completo de api/)
#    Ojo: esto incluirá pesos .h5 y .joblib salvo que los ignores en .dockerignore
COPY . /app/

# 5) Documentamos puerto; no publica, solo ayuda/guía
EXPOSE 8000

# 6) Comando por defecto: lanza tu app (API + IA si están en app.py)
CMD ["python", "app.py"]
