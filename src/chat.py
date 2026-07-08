import sys
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from utils import load_environment, get_llm
from retrieve import get_retriever

def main():
    load_environment()
    
    retriever = get_retriever()
    if not retriever:
        print("Cannot start chat without vectorstore.")
        return
        
    llm = get_llm()
    
    # Define the system prompt for RAG
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer the question. "
        "If you don't know the answer, say that you don't know. "
        "Use three sentences maximum and keep the answer concise."
        "\n\n"
        "{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    print("\n--- RAG Chat Started ---")
    print("Type 'quit' or 'exit' to stop.")
    
    while True:
        try:
            user_input = input("\nQuestion: ")
            if user_input.lower() in ['quit', 'exit']:
                break
                
            if not user_input.strip():
                continue
                
            print("Thinking...")
            response = rag_chain.invoke({"input": user_input})
            
            print(f"\nAnswer:\n{response['answer']}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            
    print("\nGoodbye!")

if __name__ == "__main__":
    main()
