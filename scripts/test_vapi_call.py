#!/usr/bin/env python3
"""
Test VAPI Call Creation

Creates a test call to VAPI assistant and processes the webhook.
"""

import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")
VOICEOPS_API_URL = os.getenv("VOICEOPS_API_URL", "http://localhost:8000")


def create_vapi_call(assistant_id: str, phone_number_id: str = None):
    """Create a VAPI call."""
    url = "https://api.vapi.ai/call"
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "assistantId": assistant_id
    }
    
    if phone_number_id:
        payload["phoneNumberId"] = phone_number_id
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error creating call: {e}")
        return None


def simulate_webhook(transcript: str, call_id: str):
    """Simulate VAPI webhook to VoiceOps API."""
    webhook_data = {
        "type": "end-of-call-report",
        "call": {
            "id": call_id,
            "transcript": transcript
        }
    }
    
    try:
        response = requests.post(
            f"{VOICEOPS_API_URL}/api/v1/vapi/webhook",
            json=webhook_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error sending webhook: {e}")
        return None


def test_with_transcript(transcript: str):
    """Test incident creation with a transcript."""
    call_id = f"test_call_{int(time.time())}"
    
    print(f"📞 Simulating call: {call_id}")
    print(f"📝 Transcript: {transcript}\n")
    
    result = simulate_webhook(transcript, call_id)
    
    if result:
        print("✅ Incident created successfully!")
        print(f"📄 Incident ID: {result.get('incident', {}).get('incident_id', 'N/A')}")
        print(f"⚡ Severity: {result.get('incident', {}).get('severity', 'N/A')}")
        print(f"📋 Category: {result.get('incident', {}).get('category', 'N/A')}")
        return result
    else:
        print("❌ Failed to create incident")
        return None


if __name__ == "__main__":
    print("=" * 60)
    print("VAPI Call Test")
    print("=" * 60)
    
    # Test 1: Simulate webhook with transcript
    print("\n1. Testing with transcript...")
    transcript = "از ساعت ۱۸:۰۵ checkout-api توی پروداکشن ۵۰۰ می‌دهد"
    test_with_transcript(transcript)
    
    # Test 2: Create actual VAPI call (if assistant ID is set)
    if ASSISTANT_ID:
        print("\n2. Creating actual VAPI call...")
        call = create_vapi_call(ASSISTANT_ID)
        if call:
            print(f"✅ Call created: {call.get('id', 'N/A')}")
            print("⏳ Wait for call to complete, then check webhook...")
        else:
            print("❌ Failed to create call")
    else:
        print("\n2. Skipping actual call (VAPI_ASSISTANT_ID not set)")

