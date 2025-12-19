import gc
import os
import sys
import asyncio
import uvicorn
from src.main import app

# Add memory management environment variables
os.environ["PYTHONUNBUFFERED"] = "1"  # Enable unbuffered output

def memory_cleanup():
    """Perform garbage collection to free memory"""
    collected = gc.collect()
    print(f"Garbage collector: collected {collected} objects")

if __name__ == "__main__":
    print("Starting server with memory management...")

    # Add resource cleanup at startup
    memory_cleanup()

    try:
        # Run the server with uvicorn
        uvicorn.run(
            "src.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            # Additional memory management options
            workers=1,  # Start with single worker to manage memory better
        )
    except KeyboardInterrupt:
        print("\nServer interrupted by user")
        memory_cleanup()
    except Exception as e:
        print(f"Server error: {e}")
        memory_cleanup()
        raise
    finally:
        # Cleanup at shutdown
        memory_cleanup()
        print("Server shutdown complete")