# Integrated RAG Chatbot for a Published Book

A Retrieval-Augmented Generation (RAG) chatbot embedded within a published book interface. The chatbot answers user questions strictly based on the book's content and can optionally answer questions using only user-selected text.

## Constitutional Principles

This project adheres to the following constitutional principles:

1. **Grounded Responses Only**: All answers are generated strictly from retrieved book content with no external knowledge or hallucinations
2. **Source Faithfulness**: Every response is traceable to specific chunks, pages, or passages from the book
3. **Context Isolation**: When users select text, the chatbot answers only using that selected text, ignoring the rest of the database
4. **Model & API Standards**: Uses Cohere (not OpenAI) for LLM and embedding services
5. **Backend Architecture**: FastAPI with Neon Postgres for metadata and Qdrant for vector storage
6. **Security & Privacy**: API keys in environment variables only, no hardcoded credentials

## Architecture

- **API Framework**: FastAPI
- **Database**: Neon Serverless Postgres (metadata) + Qdrant Cloud (vector embeddings)
- **LLM Provider**: Cohere (Command-R and Embed models)
- **Chunking Strategy**: Semantic chunks (300-500 tokens) with 50-100 token overlap

## API Endpoints

- `POST /api/v1/query` - Query against book content using global RAG mode
- `POST /api/v1/select` - Query using only selected text as context
- `POST /api/v1/upload` - Upload and index book content

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Obtain a valid Cohere API key (required by project constitution - OpenAI is not allowed)
3. Set up environment variables in `.env` file:
   ```
   # Database
   DATABASE_URL=postgresql+asyncpg://username:password@localhost/rag_chatbot

   # Qdrant
   QDRANT_URL=https://your-cluster-url.qdrant.io
   QDRANT_API_KEY=your-qdrant-api-key

   # Cohere (Mandatory - OpenAI not allowed per constitution)
   COHERE_API_KEY=your-valid-cohere-api-key

   # Application
   DEBUG=True
   ```
4. Run the ingestion script: `python memory_efficient_ingest.py`
5. Run the application: `uvicorn src.main:app --reload`

## Development

This project follows constitutional development practices as defined in `.specify/memory/constitution.md`.

## Troubleshooting

**Error: "invalid api token" when running ingestion**
- This error occurs when the COHERE_API_KEY in your `.env` file is invalid or missing
- Obtain a valid Cohere API key and update your `.env` file
- Visit https://dashboard.cohere.com/api-keys to create a new API key

**Ingestion fails during embedding**
- Ensure your Cohere API key has the necessary permissions for embedding
- Check that your account has sufficient quota for the embedding API

**API responses with "does not contain enough information"**
- This is the expected behavior when the query doesn't match content in the vector database
- Verify content was properly ingested before querying