import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

def load_environment():
    """Loads environment variables from a .env file."""
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY is not set in the environment.")

def get_llm():
    """Returns the Language Model instance."""
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

def get_embeddings():
    """Returns the embeddings model."""
    # Using a popular and fast sentence transformer model
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
