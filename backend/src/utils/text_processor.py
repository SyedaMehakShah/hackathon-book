import cohere
import asyncio
from typing import List, Dict, Any
import re

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 75, book_id: str = None, chapter: str = None, page_number: int = None) -> List[Dict[str, Any]]:
    """
    Split text into semantic chunks following constitutional requirements:
    - 300-500 tokens
    - 50-100 token overlap
    Returns list of dictionaries with content and metadata
    """
    # Split text into sentences
    sentences = re.split(r'[.!?]+\s+', text)

    chunks = []
    current_chunk = ""
    current_length = 0
    chunk_idx = 0

    for i, sentence in enumerate(sentences):
        # Estimate token count by character count (rough approximation: 1 token ~ 4 chars)
        sentence_length = len(sentence)

        # If adding this sentence would exceed chunk size
        if current_length + sentence_length > chunk_size * 4:
            if current_chunk.strip():  # If there's content in the current chunk
                # Generate a deterministic positive integer ID for Qdrant compatibility
                id_str = f"{book_id or 'unknown_book'}_chunk_{chunk_idx}"
                chunk_id = abs(hash(id_str)) % (10**9)  # Limit to 9 digits to ensure compatibility
                chunks.append({
                    "chunk_id": chunk_id,
                    "content": current_chunk.strip(),
                    "book_id": book_id,
                    "chapter": chapter,
                    "page_number": page_number,
                    "position": chunk_idx
                })
                chunk_idx += 1

            # Start a new chunk with some overlap
            # Find previous sentences that fit within overlap size
            overlap_sentences = []
            temp_length = 0

            # Work backwards to get overlap sentences
            for j in range(i-1, max(-1, i-10), -1):  # Look back up to 10 sentences
                prev_sentence = sentences[j]
                if temp_length + len(prev_sentence) <= overlap * 4:
                    overlap_sentences.insert(0, prev_sentence)
                    temp_length += len(prev_sentence)
                else:
                    break

            # Create overlap text
            current_chunk = " ".join(overlap_sentences) + " " + sentence
            current_length = temp_length + sentence_length
        else:
            current_chunk += " " + sentence
            current_length += sentence_length

    # Add the last chunk if it has content
    if current_chunk.strip():
        # Generate a deterministic positive integer ID for Qdrant compatibility
        id_str = f"{book_id or 'unknown_book'}_chunk_{chunk_idx}"
        chunk_id = abs(hash(id_str)) % (10**9)  # Limit to 9 digits to ensure compatibility
        chunks.append({
            "chunk_id": chunk_id,
            "content": current_chunk.strip(),
            "book_id": book_id,
            "chapter": chapter,
            "page_number": page_number,
            "position": chunk_idx
        })

    return chunks

async def embed_text(text: str, cohere_client: cohere.AsyncClient) -> List[float]:
    """
    Generate embedding for text using Cohere API (required by constitution)
    """
    try:
        response = await cohere_client.embed(
            texts=[text],
            model="embed-multilingual-v3.0",  # Using latest stable Cohere embedding model
            input_type="search_document"  # Required parameter for the embedding model
        )

        # Extract the embedding from the response
        embedding = response.embeddings[0]
        return embedding
    except Exception as e:
        print(f"Cohere API error: {e}")
        print("Please verify your COHERE_API_KEY in the .env file")
        raise

async def embed_texts(texts: List[str], cohere_client: cohere.AsyncClient, batch_size: int = 20) -> List[List[float]]:
    """
    Generate embeddings for multiple texts using Cohere API (required by constitution)
    Processes texts in batches to manage memory efficiently
    """
    all_embeddings = []

    try:
        # Process in batches to manage memory
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]

            response = await cohere_client.embed(
                texts=batch,
                model="embed-multilingual-v3.0",  # Using latest stable Cohere embedding model
                input_type="search_document"  # Required parameter for the embedding model
            )

            # Extract the embeddings from the response
            batch_embeddings = [embedding for embedding in response.embeddings]
            all_embeddings.extend(batch_embeddings)

        return all_embeddings
    except Exception as e:
        print(f"Cohere API error: {e}")
        print("Please verify your COHERE_API_KEY in the .env file")
        raise