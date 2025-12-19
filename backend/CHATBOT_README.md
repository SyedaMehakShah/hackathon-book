# Book Content Chatbot

This is a Python-based chatbot that allows users to ask questions about book content. It uses retrieval-augmented generation (RAG) to find relevant information from markdown documents.

## Features

- Indexes all markdown documents from the 'Docusaurus' book into Qdrant
- Ensures each document chunk has a unique integer ID
- Uses Cohere embeddings to generate vector representations for each chunk
- Creates a Qdrant collection named 'book_chunks' if it doesn't exist
- Implements a chatbot loop in Python:
  - Asks user for input
  - Retrieves top 3 relevant chunks from Qdrant using the query embedding
  - Displays retrieved chunks as context
- Includes proper error handling and retry logic for network issues
- Loads environment variables (QDRANT_URL, QDRANT_API_KEY, COHERE_API_KEY) from a .env file
- Ensures connections are properly closed after execution
- Console-based (runs in terminal)
- Contains a function placeholder for LLM-based response generation using retrieved context

## Prerequisites

- Python 3.8+
- `pip install -r requirements.txt`

## Setup

1. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure your `.env` file contains the following variables:
   ```
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   COHERE_API_KEY=your_cohere_api_key
   ```

3. Ensure your markdown documents are in the `docs/` directory or the extracted JSON file is at `extracted_docs_content.json`

## Running the Chatbot

```bash
python src/chatbot.py
```

## Usage

1. Once the indexing is complete, the chatbot will start in interactive mode
2. Enter your questions about the book content
3. The chatbot will retrieve relevant chunks and display them
4. Type 'quit', 'exit', or 'q' to exit the chatbot
5. Type 'rebuild-index' to reindex the documents

## Architecture

The system consists of:

- **Document Processing**: Parses and chunks markdown documents
- **Embedding Generation**: Uses Cohere to create vector representations
- **Vector Storage**: Stores embeddings in Qdrant for similarity search
- **Retrieval**: Finds relevant chunks based on user queries
- **Response Generation**: Placeholder for LLM-based answer generation

## Notes

- The chatbot includes retry logic for network resilience
- All connections are properly closed on exit
- Unique integer IDs are assigned to each document chunk