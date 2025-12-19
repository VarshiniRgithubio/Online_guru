FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install small set of system deps often required by Python packages (adjust if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libsndfile1 \
    curl \
 && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app
COPY . /app

EXPOSE 8000

CMD ["uvicorn", "simple_api:app", "--host", "0.0.0.0", "--port", "8000"]
