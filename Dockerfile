FROM python:3.12-slim

WORKDIR /app

# Install system dependencies (needed by some Python packages)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "monitoring/real_time_detection.py"]