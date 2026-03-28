from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_ollama import OllamaLLM
import os

app = FastAPI(title="NASA RAG API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

# Global variables for the RAG system
vectorstore = None
qa_chain = None

def load_rag_system():
    """Load the pre-built RAG system"""
    global vectorstore

    if os.path.exists("./chroma_db"):
        try:
            embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
            print("Vector store loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading vector store: {e}")
            return False
    else:
        print("ChromaDB not found. Please run build_rag.py first.")
        return False

@app.on_event("startup")
async def startup_event():
    load_rag_system()

@app.get("/")
async def root():
    return {"message": "NASA RAG API", "status": "running"}

@app.post("/ask")
async def ask_nasa(request: QueryRequest):
    if not vectorstore:
        raise HTTPException(status_code=500, detail="Vector store not loaded")

    try:
        # Retrieve relevant documents
        docs = vectorstore.similarity_search(request.question, k=3)
        context = "\n".join([doc.page_content for doc in docs])

        # Initialize Ollama LLM
        llm = OllamaLLM(model="llama3.2")

        # Create prompt
        prompt = f"""Use the following context to answer the question. If you don't know, say so.

Context: {context}

Question: {request.question}

Answer:"""

        answer = llm.invoke(prompt)
        return {"answer": answer, "question": request.question}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if vectorstore else "unhealthy",
        "vectorstore_loaded": vectorstore is not None
    }