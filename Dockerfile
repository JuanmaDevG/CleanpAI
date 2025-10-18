FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY "json files/" .
COPY api/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /app/data
ENV DB_NAME=data.db

CMD ["python3", "api/app.py"]
