from langchain.tools.retriever import create_retriever_tool
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode, tools_condition

# Load environment variables
load_dotenv()

# Initialize embeddings
embeddings = OpenAIEmbeddings()

# # Define ChromaDB storage path
PERSIST_DIR = "chroma_db_storage"

# # Load existing vector store
vectorstore = Chroma(
    persist_directory=PERSIST_DIR,
    collection_name="rag-chroma-01",
    embedding_function=embeddings,
)

# Create retriever
# retriever = vectorstore.as_retriever()

# # Create retriever tool
# retriever_tool = create_retriever_tool(
#     retriever,
#     "retrieve_blog_posts",
#     "Search and return information about CCS, its services and products",
# )


# Store tools in a list
# tools = [retriever_tool]

from langchain_core.tools import tool


@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    retrieved_docs = vectorstore.similarity_search(query, k=2)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


tools = [retrieve]

tool_nodes = ToolNode(tools=tools)

print("Retriever is ready to use.")
