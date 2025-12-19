import os
import re
import asyncio
import frontmatter  # For parsing markdown frontmatter
from typing import List, Dict, Any
from pathlib import Path

def extract_text_from_markdown(file_path: str) -> tuple:
    """
    Extract text content and frontmatter from a markdown file.
    Returns (content, frontmatter)
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        post = frontmatter.load(file)
        content = post.content
        metadata = post.metadata
    return content, metadata

def get_chapter_info_from_path(file_path: str, sidebars_config: Dict[str, Any]) -> str:
    """
    Determine chapter information based on the file's path in the documentation structure.
    """
    path_parts = Path(file_path).parts
    # Find the part that corresponds to the main category in the docs folder
    
    # Common patterns based on the sidebars.js structure
    if 'embodied-intelligence' in path_parts:
        return 'Week 1-2: Foundations - Embodied Intelligence'
    elif 'ros2-fundamentals' in path_parts:
        return 'Week 3-4: ROS 2 Fundamentals'
    elif 'gazebo-unity' in path_parts:
        return 'Week 5-6: Simulation Environments'
    elif 'nvidia-isaac' in path_parts:
        return 'Week 7: NVIDIA Isaac'
    elif 'vla-systems' in path_parts:
        return 'Week 8-9: Vision-Language-Action Systems'
    elif 'conversational-robotics' in path_parts:
        return 'Week 10-11: Conversational Robotics'
    elif 'capstone-project' in path_parts:
        return 'Week 12-13: Capstone Project'
    elif 'appendix' in path_parts:
        return 'Appendix'
    else:
        # For files directly in docs folder
        file_name = Path(file_path).stem
        if file_name == 'intro':
            return 'Introduction'
        elif file_name == 'accessibility-statement':
            return 'Accessibility Statement'
        else:
            return 'General'

def get_page_name_from_path(file_path: str) -> str:
    """
    Extract page name from the file path.
    """
    path_obj = Path(file_path)
    # Get the name without extension
    if path_obj.stem == 'index':
        # If it's an index file, use the parent directory name
        return path_obj.parent.name
    else:
        return path_obj.stem

def traverse_docs_directory(docs_path: str) -> List[Dict[str, Any]]:
    """
    Traverse the docs directory and extract all markdown content with metadata.
    Note: This approach loads all documents into memory at once which may not be
    ideal for very large document sets. For better memory management, consider
    using the streaming approach in process_documents_streaming function.
    """
    documents = []

    for root, dirs, files in os.walk(docs_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)

                # Extract content and metadata
                try:
                    content, frontmatter_meta = extract_text_from_markdown(file_path)

                    # Get chapter information based on path
                    chapter = get_chapter_info_from_path(file_path, {})

                    # Get page name
                    page_name = get_page_name_from_path(file_path)

                    # Create document record
                    doc_record = {
                        'file_path': file_path,
                        'relative_path': os.path.relpath(file_path, docs_path),
                        'content': content,
                        'frontmatter': frontmatter_meta,
                        'chapter': chapter,
                        'page_name': page_name,
                        'file_name': file
                    }

                    documents.append(doc_record)

                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")

    return documents


def process_documents_streaming(docs_path: str):
    """
    Process documents in a streaming fashion to minimize memory usage.
    Yields one document at a time instead of loading all into memory.
    """
    import os

    for root, dirs, files in os.walk(docs_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)

                # Extract content and metadata
                try:
                    content, frontmatter_meta = extract_text_from_markdown(file_path)

                    # Get chapter information based on path
                    chapter = get_chapter_info_from_path(file_path, {})

                    # Get page name
                    page_name = get_page_name_from_path(file_path)

                    # Create document record
                    doc_record = {
                        'file_path': file_path,
                        'relative_path': os.path.relpath(file_path, docs_path),
                        'content': content,
                        'frontmatter': frontmatter_meta,
                        'chapter': chapter,
                        'page_name': page_name,
                        'file_name': file
                    }
                    yield doc_record

                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
                    continue

def clean_markdown_content(content: str) -> str:
    """
    Clean markdown content by removing unnecessary formatting for RAG processing.
    """
    # Remove markdown headers markers but keep the text
    content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)
    
    # Remove image references
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    
    # Remove links but keep the text
    content = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', content)
    
    # Remove excessive whitespace while preserving paragraph structure
    content = re.sub(r'\n\s*\n', '\n\n', content)
    
    # Remove code blocks with language indicators but preserve the code
    content = re.sub(r'```.*?\n(.*?)```', r'\1', content, flags=re.DOTALL)
    
    # Remove inline code markers but keep the code
    content = re.sub(r'`(.*?)`', r'\1', content)
    
    return content.strip()

if __name__ == "__main__":
    # Define the path to the docs directory
    docs_path = "../physical-ai-textbook/docs"
    
    if not os.path.exists(docs_path):
        print(f"Docs directory not found at {docs_path}")
        exit(1)
    
    # Extract all documents
    documents = traverse_docs_directory(docs_path)
    
    print(f"Found {len(documents)} markdown documents")
    
    # Print some information about the extracted documents
    for doc in documents[:5]:  # Show first 5 for preview
        print(f"File: {doc['relative_path']}")
        print(f"Chapter: {doc['chapter']}")
        print(f"Page: {doc['page_name']}")
        print(f"Content preview: {doc['content'][:200]}...")
        print("-" * 50)
    
    # Now clean the content for RAG processing
    for doc in documents:
        doc['cleaned_content'] = clean_markdown_content(doc['content'])
    
    # Save the extracted content to a file for review
    import json
    with open("extracted_docs_content.json", "w", encoding="utf-8") as f:
        json.dump(documents, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted content from {len(documents)} documents and saved to extracted_docs_content.json")