# Your Study Buddy (NASA RAG + UI)

A simple local RAG web app with 3 interactive sections:
- Today's course (lesson text + video links)
- Questions (student question input + submit feedback)
- Talk to RAG (chat interface hitting local RAG API endpoint)

## 🛠️ Setup

1. Clone your repo
```bash
git clone https://github.com/Qianyu2021/SpaceHubPublic.git
cd SpaceHubPublic
```

2. Install dependencies
```bash
source ./rag_env/bin/activate
pip install -r requirements.txt
```

3. Optional: run setup script if you have it
```bash
chmod +x setup.sh
./setup.sh
```

4. Start API server
```bash
source ./rag_env/bin/activate
uvicorn rag_api:app --host 0.0.0.0 --port 8001 --reload
```

5. Start frontend server
```bash
python3 -m http.server 8000
```

6. Open browser:
- `http://localhost:8000/index.html`

## ▶️ Verify UI

- Home title: `Your Study Buddy`
- Tab 1: `Today's course`
  - lecture text and two video link buttons
- Tab 2: `Questions`
  - type question, submit, feedback message appears
- Tab 3: `Talk to RAG`
  - type question, send, API call to `POST http://localhost:8001/ask`

## 🧪 Optional API test

```bash
curl -X POST "http://localhost:8001/ask" -H "Content-Type: application/json" -d '{"question": "What is NASA?"}'
```

## 📂 File reference
- `index.html` : app UI
- `style.css` : CSS styles
- `script.js` : JS tab + chat + question form
- `rag_api.py` : FastAPI endpoint for RAG
- `build_rag.py` : optional data ingestion for vector store
- `requirements.txt` : Python dependencies

## 🔧 Notes

- Use `python3` in macOS if `python` is not available.
- Update the hardcoded video link to your own video in `index.html`.
- Ensure the RAG backend is running before using `Talk to RAG` tab.

