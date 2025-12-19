#!/usr/bin/env python3
"""
Test VAPI API Connection

Verifies that VAPI API keys are configured correctly.
"""

import os
import sys
import requests
from typing import Optional


def test_vapi_connection():
    """Test VAPI API connection with configured keys."""
    
    api_key = os.getenv("VAPI_API_KEY")
    public_key = os.getenv("VAPI_PUBLIC_KEY")
    
    print("=" * 60)
    print("VAPI Connection Test")
    print("=" * 60)
    
    # Check environment variables
    print("\n1. Checking environment variables...")
    if api_key:
        print(f"   [OK] VAPI_API_KEY: {api_key[:8]}...{api_key[-8:]}")
    else:
        print("   [ERROR] VAPI_API_KEY: Not set")
        return False
    
    if public_key:
        print(f"   [OK] VAPI_PUBLIC_KEY: {public_key[:8]}...{public_key[-8:]}")
    else:
        print("   [WARN] VAPI_PUBLIC_KEY: Not set (optional for server-side)")
    
    # Test API connection
    print("\n2. Testing API connection...")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            "https://api.vapi.ai/assistant",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   [OK] API connection successful!")
            print(f"   [INFO] Found {len(data) if isinstance(data, list) else 1} assistant(s)")
            return True
        else:
            print(f"   [ERROR] API connection failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   [ERROR] Connection error: {e}")
        return False


if __name__ == "__main__":
    success = test_vapi_connection()
    sys.exit(0 if success else 1)

