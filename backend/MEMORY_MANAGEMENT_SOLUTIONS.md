# Memory Management and Heap Size Solutions for the RAG Chatbot Backend

## Overview
This document outlines the solutions for Python memory issues that might be occurring in the RAG chatbot backend.

## Root Causes of Memory Issues

1. **Large Document Loading**: The ingestion scripts load all documents into memory at once before processing
2. **Embedding Batches**: Large batches of text being sent to Cohere for embedding generation
3. **Qdrant Points Creation**: Creating all Qdrant points in memory before uploading
4. **Python Memory Management**: Lack of explicit garbage collection between batches

## Solutions Implemented

### 1. Optimized Document Ingestion
- Created `memory_efficient_ingest.py` that processes documents in smaller batches with optimized memory management
- Added explicit garbage collection between batches
- Added memory cleanup after processing each document

### 2. Batched Embedding Processing
- Updated `src/utils/text_processor.py` to process embeddings in smaller batches (20 at a time)
- Modified `src/services/rag_service.py` to use batched embedding processing

### 3. Improved Memory Management in RAG Service
- Enhanced resource cleanup in the RAG service
- Added explicit memory management in server startup

## How to Run the Solutions

### To Ingest Documents More Efficiently:
```bash
python memory_efficient_ingest.py
```

### To Run the Server with Memory Management:
```bash
python run_server_with_memory_management.py
```


## Configuration Options

You can adjust the batch sizes in the following files:

1. In `memory_efficient_ingest.py`, change `batch_size` (currently set to 5)
2. In `src/utils/text_processor.py`, change the `batch_size` parameter in `embed_texts` (currently 20)

## Memory Monitoring

To monitor memory usage during document ingestion, you can add this snippet to relevant functions:

```python
import psutil
import os

def log_memory_usage(step_name):
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print(f"{step_name}: RSS={memory_info.rss / 1024 / 1024:.2f} MB, VMS={memory_info.vms / 1024 / 1024:.2f} MB")
```

## Additional Recommendations

1. **Monitor during ingestion**: Keep an eye on memory usage during document processing
2. **Adjust batch sizes**: Reduce batch sizes if running on systems with limited memory
3. **Use swap space**: Ensure adequate swap space is available on the system
4. **Process during off-peak hours**: Run large ingestion processes when system load is low
5. **Monitor the Cohere API**: Ensure API rate limits aren't causing retries that increase memory usage