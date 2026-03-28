# SpaceHuH_Web (NASA RAG)

A 3-section web app for SpaceHuH_Web:
- 2D/3D Design links
- Bevy Integration
- NASA Chat RAG (question-answering using local retrieval + Ollama)

## 🛠️ Quick setup

1. Clone the repo
```bash
git clone <your-repo-url>
cd Hackathon
```

2. Run setup script
```bash
chmod +x setup.sh
./setup.sh
```

3. Ensure Ollama is running and model is available
```bash
ollama serve
ollama list
ollama pull llama3.2  # if missing
```

4. Start the API
```bash
source ./rag_env/bin/activate
uvicorn rag_api:app --host 0.0.0.0 --port 8001 --reload
```

5. Start the frontend server in a second terminal
```bash
cd /Users/qian/Hackathon
python -m http.server 8000
```

6. Open browser

- frontend: `http://localhost:8000`
- RAG API health: `http://localhost:8001/health`

## 💡 Local testing

```bash
curl -X POST "http://localhost:8001/ask" -H "Content-Type: application/json" -d '{"question": "What is NASA?"}'
```

## 📁 Files
- `index.html` web UI
- `style.css` styles
- `script.js` UI + API calls
- `build_rag.py` data ingestion -> Chroma vector store
- `rag_api.py` FastAPI endpoint for RAG
- `setup.sh` installer script
- `requirements.txt` dependencies

## 🧩 RAG improvements

- Add more NASA documents to `build_rag.py` scraping list
- Add source metadata in Chroma documents
- Use a stronger prompt template with explicit instruction to answer from context
- Provide fallback curated goals text in corpus
