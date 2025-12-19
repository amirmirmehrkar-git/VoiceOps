#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple MVP Test - Non-interactive

Tests MVP with a single scenario.
"""

import sys
import json
import os
from pathlib import Path

# Set UTF-8 encoding for Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent))

from api.incident import create_incident_from_transcript
from api.schema import validate_incident_strict

def test_mvp():
    """Test MVP with a simple scenario."""
    print("="*60)
    print("VoiceOps MVP Test")
    print("="*60)
    
    # Test transcript
    transcript = "از ساعت ۱۸:۰۵ بعد از دیپلوی جدید، checkout-api توی پروداکشن ۵۰۰ می‌دهد. مشتری‌ها نمی‌تونن پرداخت کنن."
    call_id = "test_mvp_001"
    
    print(f"\n[TRANSCRIPT]")
    print(f"   {transcript}")
    print(f"\n[PROCESSING]...\n")
    
    try:
        # Create incident
        incident = create_incident_from_transcript(
            transcript=transcript,
            call_id=call_id,
            timezone="Europe/Berlin"
        )
        
        print("[OK] Incident created successfully!")
        
        # Validate
        validate_incident_strict(incident)
        print("[OK] Schema validation passed!")
        
        # Display JSON
        print("\n" + "="*60)
        print("Generated JSON:")
        print("="*60)
        print(json.dumps(incident, indent=2, ensure_ascii=False))
        
        # Key fields
        print("\n" + "="*60)
        print("Key Fields:")
        print("="*60)
        print(f"Title: {incident.get('title', 'N/A')}")
        print(f"Category: {incident.get('category', 'N/A')}")
        print(f"Severity: {incident.get('severity', 'N/A')}")
        print(f"Status: {incident.get('status', 'N/A')}")
        print(f"Confidence: {incident.get('confidence', 'N/A')}")
        print(f"PII Detected: {incident.get('pii', {}).get('contains_pii', False)}")
        
        print("\n" + "="*60)
        print("[SUCCESS] MVP is working!")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_mvp()
    sys.exit(0 if success else 1)

