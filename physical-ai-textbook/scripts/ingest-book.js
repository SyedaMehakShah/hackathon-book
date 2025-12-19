#!/usr/bin/env node

/**
 * Script to ingest the entire Physical AI & Humanoid Robotics textbook into the vector database.
 * Usage: node scripts/ingest-book.js
 */

require('dotenv').config();
const fs = require('fs').promises;
const path = require('path');
const { chunkText } = require('./utils/text-processing');

// Configuration
const DOCS_DIR = path.join(__dirname, '../docs');
const API_BASE_URL = process.env.API_URL || 'http://localhost:8000/api';

// Simple sleep utility
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function readMarkdownFiles(dir) {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    let files = [];
    
    for (let entry of entries) {
        const fullPath = path.join(dir, entry.name);
        
        if (entry.isDirectory()) {
            files = files.concat(await readMarkdownFiles(fullPath));
        } else if (entry.isFile() && path.extname(entry.name) === '.md') {
            const content = await fs.readFile(fullPath, 'utf-8');
            files.push({
                path: fullPath,
                relativePath: path.relative(DOCS_DIR, fullPath),
                content: content
            });
        }
    }
    
    return files;
}

async function ingestTextbook() {
    console.log('📚 Starting textbook ingestion process...');
    
    try {
        // Read all markdown files
        console.log('📖 Reading textbook content...');
        const files = await readMarkdownFiles(DOCS_DIR);
        console.log(`✅ Found ${files.length} markdown files`);
        
        let processedCount = 0;
        
        for (const file of files) {
            console.log(`📝 Processing: ${file.relativePath}`);
            
            // Chunk the content
            const chunks = chunkText(file.content, 1000, 100);
            
            // Add metadata
            const sourceMetadata = {
                source_file: file.relativePath,
                file_path: file.path,
                type: 'textbook_content',
                title: path.basename(file.relativePath, '.md')
            };
            
            // Process each chunk
            for (let i = 0; i < chunks.length; i++) {
                const chunk = chunks[i];
                
                try {
                    // Prepare the payload
                    const payload = {
                        content: chunk.text,
                        content_id: `${file.relativePath}-${i}`,
                        metadata: { ...sourceMetadata, chunk_index: i }
                    };
                    
                    // Call the API to store the document
                    const response = await fetch(`${API_BASE_URL}/store`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(payload)
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        processedCount++;
                    } else {
                        console.warn(`⚠️ Failed to store chunk ${i} of ${file.relativePath}`);
                    }
                    
                    // Add a small delay to avoid overwhelming the API
                    await sleep(100);
                } catch (error) {
                    console.error(`❌ Error processing chunk ${i} of ${file.relativePath}:`, error.message);
                }
            }
        }
        
        console.log(`🎉 Successfully processed ${processedCount} content chunks from the textbook!`);
        
        // Finalize the process
        const finalizeResponse = await fetch(`${API_BASE_URL}/index-textbook-content`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        if (finalizeResponse.ok) {
            const finalizeResult = await finalizeResponse.json();
            console.log('✅ Textbook content indexing completed:', finalizeResult);
        } else {
            console.error('❌ Error finalizing textbook indexing:', finalizeResponse.status);
        }
        
    } catch (error) {
        console.error('❌ Error during textbook ingestion:', error);
        process.exit(1);
    }
}

// Run the ingestion process
ingestTextbook();