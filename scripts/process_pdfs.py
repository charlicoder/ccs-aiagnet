import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore

load_dotenv()

DATA_DIR = "./data/docs"
VECTOR_DB_PATH = "./data/vector_db"

import pdb


def process_and_store_pdfs():
    # pdb.set_trace()
    # embeddings = OpenAIEmbeddings()  # Use your API key
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text", base_url="http://localhost:11434"
    )
    if os.path.exists(VECTOR_DB_PATH) and os.path.exists(
        os.path.join(VECTOR_DB_PATH, "index.faiss")
    ):
        print("Loading existing vector store...")
        vector_store = FAISS.load_local(
            VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True
        )
    else:
        print("No existing vector store found. Initializing a new one...")
        vector_store = None

    all_chunks = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".pdf"):
            print(f"Processing file: {filename}")
            loader = PyPDFLoader(os.path.join(DATA_DIR, filename))
            documents = loader.load()

            # Split into chunks
            splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
            chunks = splitter.split_documents(documents)
            all_chunks.extend(chunks)

    # Check if there are documents to process
    if not all_chunks:
        print("No documents found to process. Exiting...")
        return

    # Create or update the vector store
    if vector_store is None:
        vector_store = FAISS.from_documents(all_chunks, embeddings)
    else:
        vector_store.add_documents(all_chunks)

    vector_store.save_local(VECTOR_DB_PATH)
    print("Vector DB updated successfully.")


if __name__ == "__main__":
    process_and_store_pdfs()
