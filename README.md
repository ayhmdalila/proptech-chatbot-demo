# Proptech Chatbot Demo

Lightweight Streamlit demo that loads a causal LLM via Hugging Face Transformers and serves a simple chat UI for PropTech use cases.

![ui](https://github.com/ayhmdalila/proptech-chatbot-demo/blob/main/ui.gif)

## Quick facts
- Frameworks: Streamlit frontend, Transformers for model loading, optional FastAPI endpoint.
- Expectation: MODEL environment variable points to a Hugging Face model ID (or path).
- GPU: Recommended for medium/large models. Requires NVIDIA drivers + NVIDIA Container Toolkit on the host.

## Files of interest
- app.py — Streamlit frontend
- model.py — loads model using env var `MODEL`
- generator.py — inference / decoding logic
- server.py — optional FastAPI endpoint (/chat/chat/completions)
- requirements.txt — Python dependencies
- Dockerfile — GPU-ready image (default targets CUDA 12.1 / cu121)

## Environment variables (.env example)
- MODEL=hf-model-id
- HF_TOKEN=your_hf_token  # optional, for private models
Create a `.env` file or pass vars at runtime.

## Build & run (GPU)
1. Build:
   docker build -t proptech-chatbot-demo:gpu .

2. Run:
   docker run --gpus=all --rm -p 8501:8501 \
     --env-file .env \
     -v /path/to/hf_cache:/root/.cache/huggingface \
     proptech-chatbot-demo:gpu

Notes:
- Use `--gpus=all` and ensure the host has NVIDIA Container Toolkit installed.
- Mount HF cache to persist downloads: `-v /local/hf_cache:/root/.cache/huggingface`.

## Build & run (CPU)
- Replace the Docker base image with a CPU image (python:3.11-slim) and install CPU PyTorch, or build a CPU-specific image.

## Running locally (without Docker)
1. Create venv, install requirements:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
2. Set `MODEL` in env or .env then:
   streamlit run app.py

## Troubleshooting
- If model fails to load with CUDA errors: match base CUDA image / PyTorch wheel to host driver (cu121, cu118, etc.).
- Verify GPU visibility: `nvidia-smi`
- If using private HF models, set `HF_TOKEN` or configure `~/.huggingface/token`.

## Tips
- Use small models for testing to save bandwidth and memory.
- For production, serve model weights from persistent storage and restrict access to the UI/API.

## License
Project files and model weights are subject to their respective licenses. Confirm model usage terms before deployment.
