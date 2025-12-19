#!/usr/bin/env python3
"""
Test VAPI API Connection
Tests basic VAPI API connectivity and authentication.
"""

import os
import sys
import requests
import json
from typing import Optional

# Fix Unicode output for Windows PowerShell
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# VAPI API Base URL
VAPI_API_BASE = "https://api.vapi.ai"

def get_api_key() -> Optional[str]:
    """Get VAPI API key from environment variable."""
    api_key = os.getenv("VAPI_API_KEY")
    if not api_key:
        print("❌ Error: VAPI_API_KEY environment variable not set!")
        print("\n📝 To set it:")
        print("   PowerShell: $env:VAPI_API_KEY = 'your-api-key'")
        print("   Or create a .env file with: VAPI_API_KEY=your-api-key")
        return None
    return api_key

def test_api_connection(api_key: str) -> bool:
    """Test basic API connection by listing assistants."""
    print("🔍 Testing VAPI API connection...")
    print(f"   API Base: {VAPI_API_BASE}")
    print(f"   API Key: {api_key[:10]}...{api_key[-4:]}")
    print()
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Test 1: List Assistants
        print("📋 Test 1: Listing assistants...")
        response = requests.get(
            f"{VAPI_API_BASE}/assistant",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            assistants_data = response.json()
            # Handle both list and dict responses
            if isinstance(assistants_data, dict):
                assistants_list = assistants_data.get('data', [])
            else:
                assistants_list = assistants_data if isinstance(assistants_data, list) else []
            
            print(f"   ✅ Success! Found {len(assistants_list)} assistant(s)")
            if assistants_list:
                print("\n   📝 Existing Assistants:")
                for assistant in assistants_list[:3]:  # Show first 3
                    if isinstance(assistant, dict):
                        print(f"      - {assistant.get('name', 'Unnamed')} (ID: {assistant.get('id', 'N/A')[:8]}...)")
                    else:
                        print(f"      - {assistant}")
            return True
        elif response.status_code == 401:
            print(f"   ❌ Authentication failed (401)")
            print(f"   Response: {response.text}")
            return False
        else:
            print(f"   ⚠️  Unexpected status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection error: {e}")
        return False

def test_create_assistant(api_key: str) -> bool:
    """Test creating a simple assistant."""
    print("\n📋 Test 2: Creating a test assistant...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Simple test assistant for VoiceOps
    assistant_data = {
        "name": "VoiceOps Test Assistant",
        "model": {
            "provider": "openai",
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "systemPrompt": """You are a voice incident reporter assistant. 
Ask the caller exactly 4 questions:
1. What happened? (incident description)
2. When did it occur? (timestamp)
3. What systems are affected? (system names)
4. How severe is the impact? (severity level)

After collecting answers, output a JSON object matching the VoiceOps incident schema."""
        },
        "voice": {
            "provider": "11labs",
            "voiceId": "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
        },
        "firstMessage": "Hello! I'm here to help you report an incident. Let me ask you a few questions.",
        "recordingEnabled": True
    }
    
    try:
        response = requests.post(
            f"{VAPI_API_BASE}/assistant",
            headers=headers,
            json=assistant_data,
            timeout=15
        )
        
        if response.status_code == 200 or response.status_code == 201:
            assistant = response.json()
            assistant_id = assistant.get('id', 'N/A')
            print(f"   ✅ Success! Created assistant: {assistant.get('name')}")
            print(f"   📝 Assistant ID: {assistant_id}")
            print(f"\n   💡 You can use this assistant ID for testing calls.")
            return True
        else:
            print(f"   ⚠️  Status: {response.status_code}")
            print(f"   Response: {response.text[:300]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Main test function."""
    print("=" * 60)
    print("🚀 VAPI Connection Test")
    print("=" * 60)
    print()
    
    # Get API key
    api_key = get_api_key()
    if not api_key:
        sys.exit(1)
    
    print()
    
    # Test 1: Basic connection
    connection_ok = test_api_connection(api_key)
    
    if not connection_ok:
        print("\n❌ Basic connection test failed. Please check your API key.")
        sys.exit(1)
    
    # Test 2: Create assistant (optional)
    print("\n" + "=" * 60)
    create_ok = test_create_assistant(api_key)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print(f"   Connection Test: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    print(f"   Create Assistant: {'✅ PASS' if create_ok else '⚠️  SKIP'}")
    print()
    
    if connection_ok:
        print("✅ VAPI is ready to use!")
        print("\n📝 Next steps:")
        print("   1. Use the assistant ID above to make test calls")
        print("   2. Set up webhook endpoint for call events")
        print("   3. Test end-to-end voice → JSON flow")
    else:
        print("❌ Please fix connection issues before proceeding.")
        sys.exit(1)

if __name__ == "__main__":
    main()

