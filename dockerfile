FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    tk \
    libtk8.6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/backend/

EXPOSE 5000

CMD ["python", "main.py"]