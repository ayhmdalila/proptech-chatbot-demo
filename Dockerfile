# Lightweight CPU-friendly Dockerfile.
# To keep the image small by default, torch is NOT installed here.
# If you want to include CPU torch at build time: docker build --build-arg INSTALL_TORCH=1 -t proptech-chatbot-demo .
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    MODEL=Qwen/Qwen3-0.6B-MLX-4bit

WORKDIR /app

# Minimal system deps needed by many Python packages and git-lfs for HF models
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl git git-lfs build-essential \
    && git lfs install --skip-smudge || true \
    && rm -rf /var/lib/apt/lists/*

# Optionally install torch during build (keep default OFF to reduce image size)
ARG INSTALL_TORCH=1

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
 && if [ "$INSTALL_TORCH" = "1" ]; then \
      # small/portable CPU wheel index; for GPU you'll build a different image / use host GPU tooling
      pip install --no-cache-dir torch --extra-index-url https://download.pytorch.org/whl/cpu ; \
    fi \
 && pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]