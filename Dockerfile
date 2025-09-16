# Simple CPU Dockerfile for the Streamlit + Transformers app.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501

WORKDIR /app

# Install system dependencies required by some Python packages and git-lfs for large models
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential git git-lfs curl ca-certificates \
    && git lfs install --skip-smudge || true \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python deps
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy application files
COPY . /app

# Expose Streamlit default port
EXPOSE 8501

# NOTE: this container expects an environment variable MODEL set at runtime (used by model.py),
# and/or a mounted .env file with MODEL=<hf-model-id>. Large model weights will be downloaded to the HF cache.
CMD ["streamlit", "run", "app.py"]