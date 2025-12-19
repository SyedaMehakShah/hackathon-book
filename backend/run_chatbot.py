#!/usr/bin/env python3
"""
Book Content Chatbot Runner

This script provides a simple way to run the book content chatbot.
"""

import sys
import os
import asyncio

# Add the src directory to the path so we can import the chatbot
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import main

if __name__ == "__main__":
    print("Starting Book Content Chatbot...")
    print("Make sure your .env file contains the required API keys.")
    print("Press Ctrl+C to exit the chatbot at any time.")
    print("-" * 50)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nChatbot interrupted by user. Goodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)