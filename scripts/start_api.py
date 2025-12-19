#!/usr/bin/env python3
"""
Start VoiceOps API Server

Simple script to start the API server with proper configuration.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def check_env():
    """Check environment variables."""
    required = ["OPENAI_API_KEY"]  # or ANTHROPIC_API_KEY
    missing = []
    
    for key in required:
        if not os.getenv(key) and not os.getenv("ANTHROPIC_API_KEY"):
            missing.append(key)
    
    if missing:
        print("WARNING: Missing environment variables:")
        for key in missing:
            print(f"  - {key}")
        print("\nThe API will use fallback mode (no LLM).")
        print("Set OPENAI_API_KEY or ANTHROPIC_API_KEY for full functionality.")
        return False
    
    return True

def main():
    """Start the API server."""
    print("="*60)
    print("VoiceOps API Server")
    print("="*60)
    
    # Check environment
    has_keys = check_env()
    
    if has_keys:
        print("\n[OK] API keys configured")
    else:
        print("\n[WARN] Running in fallback mode")
    
    print("\nStarting server on http://localhost:8000")
    print("API docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop\n")
    
    # Import and run
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()

