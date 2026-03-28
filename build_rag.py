import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_ollama import OllamaLLM
import os

def collect_nasa_data():
    """Collect NASA-related text data"""
    urls = [
        "https://www.nasa.gov/missions/",
        "https://www.nasa.gov/audience/forstudents/5-8/index.html",
        "https://www.nasa.gov/audience/forstudents/9-12/index.html"
    ]

    all_text = ""
    for url in urls:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract text from paragraphs
            paragraphs = soup.find_all('p')
            text = ' '.join([p.get_text() for p in paragraphs])
            all_text += text + " "
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    return all_text

def create_vector_store(text):
    """Create and populate ChromaDB vector store"""
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    # Create embeddings
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    # Create vector store
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    return vectorstore

def test_rag(vectorstore):
    """Test the RAG system"""
    llm = OllamaLLM(model="llama2")

    test_questions = [
        "What is NASA's mission?",
        "What are some NASA missions?",
        "Tell me about space exploration"
    ]

    for question in test_questions:
        print(f"\nQuestion: {question}")

        # Retrieve relevant documents
        docs = vectorstore.similarity_search(question, k=3)
        context = "\n".join([doc.page_content for doc in docs])

        # Create prompt
        prompt = f"""Use the following context to answer the question. If you don't know, say so.

Context: {context}

Question: {question}

Answer:"""

        try:
            answer = llm.invoke(prompt)
            print(f"Answer: {answer}")
        except Exception as e:
            print(f"Error: {e}")

def main():
    print("Building NASA RAG system...")

    # Collect data
    print("Collecting NASA data...")
    nasa_text = collect_nasa_data()

    if not nasa_text:
        print("No data collected. Using sample data...")
        nasa_text = """
        NASA is the National Aeronautics and Space Administration. Founded in 1958, NASA leads the United States in space exploration.
        NASA's mission includes understanding Earth's systems, exploring other worlds, and protecting our planet.
        Key missions include the Space Shuttle program, International Space Station, Mars rovers, and the Artemis program to return humans to the Moon.
        NASA has sent astronauts to the Moon, probes to Mars, and telescopes like Hubble to study the universe.
        """

    # Create vector store
    print("Creating vector store...")
    vectorstore = create_vector_store(nasa_text)

    # Test the system
    print("Testing RAG system...")
    test_rag(vectorstore)

    print("\nRAG system built successfully!")

if __name__ == "__main__":
    main()