# RAG Project

A simple Retrieval-Augmented Generation (RAG) application that retrieves relevant information from a knowledge base before generating responses using a Large Language Model (LLM).

## Features

- Document ingestion
- Text chunking
- Vector embeddings
- Semantic search
- Context-aware response generation

## Tech Stack

- Python
- LangChain
- ChromaDB
- OpenAI / Any LLM API
- Sentence Transformers

## Project Structure

```text
.
├── data/
├── vectorstore/
├── src/
│   ├── ingest.py
│   ├── retrieve.py
│   ├── chat.py
│   └── utils.py
├── requirements.txt
└── README.md
```

## Installation

```bash
git clone <repository-url>
cd rag-project

python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

## Usage

1. Add your documents to the `data/` folder.
2. Run the ingestion script.
3. Start the application.
4. Ask questions about your documents.

## Example

```text
Question:
What is RAG?

Answer:
Retrieval-Augmented Generation (RAG) retrieves relevant information from a knowledge base and provides it as context to an LLM, improving the accuracy of generated responses.
```

## Future Improvements

- Support PDF, DOCX, and TXT files
- Hybrid search
- Chat history
- Source citations
- Web interface

## License

This project is licensed under the MIT License.
