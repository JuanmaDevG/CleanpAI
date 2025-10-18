FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    sqlite3 \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# Instalar dependencias de Python si tienes requirements.txt
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# Crear un volumen para persistir la base de datos
VOLUME /app/data

# Variable de entorno para la base de datos
ENV DB_NAME=sistema_alertas.db

# Comando por defecto (puedes cambiarlo según tus necesidades)
CMD ["python", "app.py"]
