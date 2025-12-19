#!/usr/bin/env python3
"""
Test VAPI Call - Make a test call and process webhook
"""

import os
import sys
import requests
import json
import time
from typing import Optional, Dict, Any

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
        return None
    return api_key

def get_assistant_id(api_key: str) -> Optional[str]:
    """Get or create a VoiceOps assistant."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # First, try to find existing VoiceOps assistant
    print("🔍 Looking for existing VoiceOps assistant...")
    try:
        response = requests.get(
            f"{VAPI_API_BASE}/assistant",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            assistants = response.json()
            assistants_list = assistants if isinstance(assistants, list) else assistants.get('data', [])
            
            for assistant in assistants_list:
                if isinstance(assistant, dict) and 'VoiceOps' in assistant.get('name', ''):
                    assistant_id = assistant.get('id')
                    print(f"   ✅ Found existing assistant: {assistant.get('name')} (ID: {assistant_id})")
                    return assistant_id
    except Exception as e:
        print(f"   ⚠️  Error checking existing assistants: {e}")
    
    # Create new assistant
    print("\n📝 Creating new VoiceOps assistant...")
    assistant_data = {
        "name": "VoiceOps Incident Reporter",
        "model": {
            "provider": "openai",
            "model": "gpt-4o-mini",
            "temperature": 0.7,
            "systemPrompt": """You are a voice incident reporter assistant for VoiceOps.

Your job is to collect incident information and output a JSON object matching the VoiceOps incident schema.

Ask the caller exactly 4 questions:
1. What happened? (incident description)
2. When did it occur? (timestamp)
3. What systems are affected? (system names)
4. How severe is the impact? (severity level: sev1, sev2, sev3, or sev4)

After collecting all answers, output ONLY a valid JSON object matching this schema:
{
  "schema_version": "1.0.0",
  "incident_id": "generate-uuid-here",
  "source": {
    "channel": "voice",
    "vendor": "vapi",
    "call_id": "call_id_here"
  },
  "occurred_at": "ISO-8601-timestamp",
  "reported_at": "ISO-8601-timestamp",
  "title": "Brief incident title",
  "summary": "Detailed summary",
  "category": "outage|performance|security_incident|data_issue|unknown",
  "severity": "sev1|sev2|sev3|sev4",
  "status": "new",
  "location": {"site": "site-name"},
  "systems": [{"name": "system-name", "environment": "prod|staging|dev"}],
  "tags": ["tag1", "tag2"],
  "confidence": 0.0-1.0
}

Output ONLY the JSON, no other text."""
        },
        "voice": {
            "provider": "11labs",
            "voiceId": "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
        },
        "firstMessage": "Hello! I'm here to help you report an incident. Let me ask you a few questions.",
        "recordingEnabled": True,
        "endCallFunctionEnabled": True
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
            assistant_id = assistant.get('id')
            print(f"   ✅ Created assistant: {assistant.get('name')}")
            print(f"   📝 Assistant ID: {assistant_id}")
            return assistant_id
        else:
            print(f"   ❌ Failed to create assistant: {response.status_code}")
            print(f"   Response: {response.text[:300]}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error creating assistant: {e}")
        return None

def make_test_call(api_key: str, assistant_id: str, phone_number: Optional[str] = None) -> Optional[str]:
    """Make a test call using VAPI."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # For testing, we can use VAPI's test phone number or user's number
    if not phone_number:
        print("\n📞 Note: To make a real call, provide a phone number.")
        print("   For testing, you can use VAPI's test mode or web interface.")
        print(f"\n💡 Assistant ID: {assistant_id}")
        print(f"   Use this ID in VAPI dashboard or SDK to make calls.")
        return None
    
    call_data = {
        "assistantId": assistant_id,
        "phoneNumberId": phone_number  # This should be a phone number ID from VAPI
    }
    
    try:
        print(f"\n📞 Making test call to {phone_number}...")
        response = requests.post(
            f"{VAPI_API_BASE}/call",
            headers=headers,
            json=call_data,
            timeout=15
        )
        
        if response.status_code == 200 or response.status_code == 201:
            call = response.json()
            call_id = call.get('id')
            print(f"   ✅ Call initiated! Call ID: {call_id}")
            return call_id
        else:
            print(f"   ❌ Failed to make call: {response.status_code}")
            print(f"   Response: {response.text[:300]}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error making call: {e}")
        return None

def main():
    """Main test function."""
    print("=" * 60)
    print("🚀 VAPI Call Test")
    print("=" * 60)
    print()
    
    # Get API key
    api_key = get_api_key()
    if not api_key:
        sys.exit(1)
    
    # Get or create assistant
    assistant_id = get_assistant_id(api_key)
    if not assistant_id:
        print("\n❌ Failed to get/create assistant.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print(f"\n📝 Assistant ID: {assistant_id}")
    print("\n💡 Next steps:")
    print("   1. Use VAPI Dashboard: https://dashboard.vapi.ai")
    print("   2. Or use VAPI SDK/CLI to make calls")
    print("   3. Set up webhook endpoint to receive call events")
    print("   4. Test end-to-end: Voice → Transcript → JSON")
    
    # Optional: Make a test call if phone number provided
    phone_number = os.getenv("VAPI_TEST_PHONE")
    if phone_number:
        call_id = make_test_call(api_key, assistant_id, phone_number)
        if call_id:
            print(f"\n✅ Test call initiated! Call ID: {call_id}")

if __name__ == "__main__":
    main()

