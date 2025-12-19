# Memory Management Solutions

This document outlines the memory management solutions implemented to address Python memory issues in the project.

## Problem Summary

The issue was a Python memory error, which happened because the process exceeded available memory due to loading or processing too much data at once, such as large files, many documents, embeddings, or uncontrolled loops that keep data in memory; as a result, the garbage collector cannot reclaim enough memory and causes performance issues.

## Solutions Implemented

### 1. Memory Optimized Ingestion Scripts

#### Files Created/Modified:
- `memory_efficient_ingest.py` - Latest version with comprehensive memory management including batch processing, memory monitoring, and garbage collection
- `optimized_ingest_script.py` - Enhanced version with memory monitoring and smaller batch processing (deprecated)
- `streamlined_ingest_script.py` - Streaming approach to process documents one at a time (deprecated)
- `src/utils/doc_extractor.py` - Added streaming document processing function

#### Key Optimizations:
- **Batch Processing**: Reduced batch size to 5 documents to minimize memory usage
- **Memory Monitoring**: Added `psutil` to track memory usage during processing
- **Garbage Collection**: Added explicit `gc.collect()` calls between batches
- **Variable Cleanup**: Explicitly deleting large variables (`cleaned_content`) after use
- **Streaming Processing**: Added option to process documents one at a time instead of loading all into memory

### 2. Server Memory Management

#### Files Modified:
- `run_server.py` - Added memory cleanup functions and environment variables
- `run_server_with_memory_management.py` - Enhanced existing memory management

#### Key Improvements:
- Added garbage collection at server startup and shutdown
- Set environment variables for unbuffered output
- Limited to single worker to manage memory better

### 3. Unnecessary File Cleanup

#### Files Removed:
- `ingest_with_fresh_env.py.bak` - Backup file that was not needed
- `extracted_docs_content.json` - Large JSON file with previously extracted content (~173KB)

#### Cleanup Script:
- `cleanup_unused_files.py` - Automated script to remove unnecessary files

### 4. Batch Query Processing

#### File Created:
- `batch_query_processor.py` - Processes queries in batches with memory management

#### Key Features:
- Processes queries one at a time to limit memory usage
- Includes memory monitoring between operations
- Explicit garbage collection after each query

### 5. Dependency Updates

#### File Modified:
- `requirements.txt` - Added `psutil==5.9.5` for memory monitoring

## Best Practices Implemented

1. **Batch Processing**: Instead of loading all documents at once, process them in small batches
2. **Streaming**: For very large datasets, use streaming approaches that process one item at a time
3. **Garbage Collection**: Explicitly call `gc.collect()` at strategic points to free memory
4. **Variable Cleanup**: Use `del` to remove large variables after they're no longer needed
5. **Memory Monitoring**: Track memory usage to identify potential issues early
6. **File Cleanup**: Remove unnecessary files that consume memory or disk space

## Usage Instructions

### For Document Ingestion:
```bash
# Use the latest memory-efficient ingestion script with comprehensive memory management
python memory_efficient_ingest.py

# The following scripts are deprecated and should no longer be used:
# python optimized_ingest_script.py
# python streamlined_ingest_script.py
```

### For Running the Server:
```bash
# Use memory-optimized server
python run_server.py
```

### For Query Processing:
```bash
# Use batch query processor for memory-efficient query handling
python batch_query_processor.py
```

### For Cleanup:
```bash
# Remove unnecessary files
python cleanup_unused_files.py
```

## Additional Node.js Heap Configuration

Although this is primarily a Python application, if you need to run Node.js scripts with increased heap size, use:

```bash
node --max-old-space-size=4096 <file>
```

Or update your npm scripts accordingly in package.json:

```json
{
  "scripts": {
    "start": "node --max-old-space-size=4096 server.js"
  }
}
```

## Performance Monitoring

The optimized scripts include memory monitoring that will report:
- Initial memory usage
- Memory usage before and after each batch
- Memory difference during processing
- Final memory usage

This helps track the effectiveness of the memory optimizations.