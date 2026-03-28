#!/usr/bin/env bash
set -euo pipefail

echo "=== Space Hub NASA RAG Setup ==="

# 1) Create + activate Python venv
if [ ! -d "./rag_env" ]; then
  echo "Creating virtual environment..."
  python3 -m venv rag_env
else
  echo "Virtual environment already exists."
fi

source ./rag_env/bin/activate

# 2) Upgrade pip
pip install --upgrade pip

# 3) Install project dependencies
pip install -r requirements.txt

# 4) Optional: Pull Ollama model
if command -v ollama >/dev/null 2>&1; then
  echo "Ollama found. Listing available models..."
  ollama list
  echo "If you do not have a model, run: ollama pull llama3.2"
else
  echo "Warning: Ollama not installed. Please install from https://ollama.com/"
fi

# 5) Build the Chroma vector store
echo "Running build_rag.py to create vector store (this may take a few minutes)..."
python build_rag.py

echo "Setup completed. Start the server with: uvicorn rag_api:app --host 0.0.0.0 --port 8001 --reload"
