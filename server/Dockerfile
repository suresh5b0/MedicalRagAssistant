FROM python:3.12-slim

WORKDIR /app

# system dependencies (FAISS needs these)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# copy requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy backend code
COPY . .

# expose FastAPI port
EXPOSE 8000

# run API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]