import os
from langchain_community.vectorstores import Chroma
from utils import get_embeddings

def get_retriever():
    """Initializes and returns the vector store retriever."""
    persist_directory = os.path.join(os.path.dirname(__file__), "..", "vectorstore")
    
    if not os.path.exists(persist_directory):
        print("Vectorstore not found. Please run ingest.py first.")
        return None
        
    embeddings = get_embeddings()
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    
    # Return a retriever that fetches the top 3 most relevant chunks
    return vectorstore.as_retriever(search_kwargs={"k": 3})

if __name__ == "__main__":
    # Test retrieval
    import sys
    from utils import load_environment
    
    load_environment()
    query = "What is RAG?" if len(sys.argv) == 1 else sys.argv[1]
    
    retriever = get_retriever()
    if retriever:
        docs = retriever.invoke(query)
        print(f"\nResults for: '{query}'")
        for i, doc in enumerate(docs):
            print(f"\n--- Result {i+1} ---")
            print(doc.page_content)
            print(f"Source: {doc.metadata.get('source', 'Unknown')}")
