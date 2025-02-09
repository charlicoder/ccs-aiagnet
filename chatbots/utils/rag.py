from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set user agent for web scraping
os.environ["USER_AGENT"] = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)

# Define ChromaDB persistent storage path
PERSIST_DIR = "chroma_db_storage"

# Define URLs to scrape
urls = [
    "https://www.cloudcustomsolutions.com/services/",
    "https://www.cloudcustomsolutions.com/products/",
    "https://www.cloudcustomsolutions.com/about-us/",
    "https://www.cloudcustomsolutions.com/business-matchmaking-software/",
    "https://www.cloudcustomsolutions.com/blog/",
]

# Load documents
docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

# Split documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=100, chunk_overlap=50
)
doc_splits = text_splitter.split_documents(docs_list)

# Initialize embeddings
embeddings = OpenAIEmbeddings()

# Check if ChromaDB already exists
# if not os.path.exists(PERSIST_DIR):
#     print("Loading existing ChromaDB vector store...")

# print("Creating new ChromaDB vector store...")

vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma-01",
    embedding=embeddings,
    persist_directory=PERSIST_DIR,  # Save vectors persistently
)
vectorstore.persist()

# Get retriever
retriever = vectorstore.as_retriever()

print("Vector database is ready for retrieval.")
