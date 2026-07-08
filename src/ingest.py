import os
import glob
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from utils import load_environment, get_embeddings

def main():
    load_environment()
    
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    persist_directory = os.path.join(os.path.dirname(__file__), "..", "vectorstore")
    
    if not os.path.exists(data_dir):
        print(f"Data directory '{data_dir}' not found. Please create it and add documents.")
        return
        
    documents = []
    
    # Load PDF files
    for filepath in glob.glob(os.path.join(data_dir, "*.pdf")):
        print(f"Loading PDF: {filepath}")
        loader = PyPDFLoader(filepath)
        documents.extend(loader.load())
        
    # Load TXT files
    for filepath in glob.glob(os.path.join(data_dir, "*.txt")):
        print(f"Loading Text file: {filepath}")
        loader = TextLoader(filepath, encoding="utf-8")
        documents.extend(loader.load())
        
    if not documents:
        print("No documents found in the data directory. Please add some .txt or .pdf files.")
        return
        
    print(f"Loaded {len(documents)} document pages/sections.")
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Split documents into {len(chunks)} chunks.")
    
    print("Generating embeddings and storing in ChromaDB...")
    embeddings = get_embeddings()
    
    # Create or update vector store
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    
    print(f"Successfully ingested data into vectorstore at {persist_directory}")

if __name__ == "__main__":
    main()
