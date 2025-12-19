#!/usr/bin/env python3
"""
Book Content Chatbot Runner (Memory Optimized)

This script provides a simple way to run the book content chatbot with memory management.
"""

import sys
import os
import asyncio
import gc

# Add the src directory to the path so we can import the chatbot
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import main

def memory_cleanup():
    """Perform garbage collection to free memory"""
    collected = gc.collect()
    print(f"Garbage collector: collected {collected} objects")

if __name__ == "__main__":
    print("Starting Book Content Chatbot with memory management...")
    print("Make sure your .env file contains the required API keys.")
    print("Press Ctrl+C to exit the chatbot at any time.")
    print("-" * 50)
    
    # Clean up memory before starting
    memory_cleanup()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nChatbot interrupted by user. Goodbye!")
        memory_cleanup()
    except Exception as e:
        print(f"An error occurred: {e}")
        memory_cleanup()
        sys.exit(1)
    finally:
        # Cleanup memory at exit
        memory_cleanup()
        print("Chatbot shutdown complete.")