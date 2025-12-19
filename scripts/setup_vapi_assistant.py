#!/usr/bin/env python3
"""
Setup VAPI Assistant for VoiceOps

Creates a VAPI assistant with the 4-question prompt.
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VOICEOPS_WEBHOOK_URL = os.getenv("VOICEOPS_WEBHOOK_URL", "http://localhost:8000/api/v1/vapi/webhook")

PROMPT_PATH = Path(__file__).parent.parent / "engineering" / "vapi_agent_prompt_4questions.txt"


def load_prompt():
    """Load VAPI agent prompt."""
    if not PROMPT_PATH.exists():
        print(f"❌ Prompt file not found: {PROMPT_PATH}")
        return None
    
    with open(PROMPT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def create_vapi_assistant():
    """Create VAPI assistant for VoiceOps."""
    prompt = load_prompt()
    if not prompt:
        return None
    
    url = "https://api.vapi.ai/assistant"
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "name": "VoiceOps Incident Intake",
        "firstMessage": "سلام، من VoiceOps هستم. برای گزارش حادثه، لطفاً به ۴ سؤال من پاسخ دهید.",
        "model": {
            "provider": "openai",
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "system",
                    "content": prompt
                }
            ],
            "temperature": 0.3
        },
        "voice": {
            "provider": "vapi",
            "voiceId": "Elliot"
        },
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-3",
            "language": "fa"
        },
        "serverUrl": VOICEOPS_WEBHOOK_URL,
        "serverUrlSecret": os.getenv("VAPI_WEBHOOK_SECRET", ""),
        "endCallFunctionEnabled": True
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error creating assistant: {e}")
        if hasattr(e, 'response'):
            print(f"Response: {e.response.text}")
        return None


def list_assistants():
    """List all VAPI assistants."""
    url = "https://api.vapi.ai/assistant"
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error listing assistants: {e}")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("VAPI Assistant Setup for VoiceOps")
    print("=" * 60)
    
    if not VAPI_API_KEY:
        print("❌ VAPI_API_KEY not set in environment")
        exit(1)
    
    # List existing assistants
    print("\n📋 Existing assistants:")
    assistants = list_assistants()
    if assistants:
        if isinstance(assistants, list):
            for a in assistants:
                print(f"  - {a.get('name', 'N/A')} (ID: {a.get('id', 'N/A')})")
        else:
            print(f"  - {assistants.get('name', 'N/A')} (ID: {assistants.get('id', 'N/A')})")
    
    # Create new assistant
    print("\n🔧 Creating VoiceOps assistant...")
    assistant = create_vapi_assistant()
    
    if assistant:
        print("✅ Assistant created successfully!")
        print(f"📝 Name: {assistant.get('name', 'N/A')}")
        print(f"🆔 ID: {assistant.get('id', 'N/A')}")
        print(f"\n💡 Add this to your .env file:")
        print(f"VAPI_ASSISTANT_ID={assistant.get('id', '')}")
        print(f"\n🔗 Webhook URL: {VOICEOPS_WEBHOOK_URL}")
    else:
        print("❌ Failed to create assistant")

