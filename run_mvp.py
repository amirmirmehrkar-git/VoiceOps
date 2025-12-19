#!/usr/bin/env python3
"""
VoiceOps MVP - Complete Working Demo

This script demonstrates the complete flow:
1. Simulate voice transcript (or use real VAPI)
2. Process transcript → JSON
3. Validate output
4. Display results
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from api.incident import create_incident_from_transcript
from api.schema import validate_incident_strict
from api.scoring import classify_severity

def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_success(text):
    """Print success message."""
    print(f"[OK] {text}")

def print_error(text):
    """Print error message."""
    print(f"[ERROR] {text}")

def demo_with_transcript(transcript, call_id=None):
    """Demo with a transcript."""
    print_header("VoiceOps MVP Demo")
    
    print(f"\n📝 Transcript:")
    print(f"   {transcript}")
    
    print(f"\n🔄 Processing...")
    
    try:
        # Create incident from transcript
        incident = create_incident_from_transcript(
            transcript=transcript,
            call_id=call_id or f"demo_{int(datetime.now().timestamp())}",
            timezone="Europe/Berlin"
        )
        
        print_success("Incident created successfully!")
        
        # Display results
        print_header("Generated Incident JSON")
        print(json.dumps(incident, indent=2, ensure_ascii=False))
        
        # Validate
        print_header("Validation")
        try:
            validate_incident_strict(incident)
            print_success("Schema validation passed!")
        except ValueError as e:
            print_error(f"Schema validation failed: {e}")
            return False
        
        # Show key fields
        print_header("Key Fields")
        print(f"Title: {incident.get('title', 'N/A')}")
        print(f"Category: {incident.get('category', 'N/A')}")
        print(f"Severity: {incident.get('severity', 'N/A')}")
        print(f"Status: {incident.get('status', 'N/A')}")
        print(f"Confidence: {incident.get('confidence', 'N/A')}")
        print(f"PII Detected: {incident.get('pii', {}).get('contains_pii', False)}")
        
        return True
        
    except Exception as e:
        print_error(f"Failed to create incident: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main demo function."""
    # Demo scenarios
    scenarios = [
        {
            "name": "Production Outage",
            "transcript": "از ساعت ۱۸:۰۵ بعد از دیپلوی جدید، checkout-api توی پروداکشن ۵۰۰ می‌دهد. مشتری‌ها نمی‌تونن پرداخت کنن. فکر کنم دیتابیس payments timeout می‌ده. لطفاً فوری رسیدگی کنید.",
            "call_id": "demo_outage_001"
        },
        {
            "name": "Security Incident",
            "transcript": "یک لاگین مشکوک شناسایی شد. کاربر admin از IP غیرمعمول وارد شده. احتمال نشت توکن وجود داره. باید فوری بررسی بشه.",
            "call_id": "demo_security_001"
        },
        {
            "name": "Ambiguous Report",
            "transcript": "یه مشکلی هست… بعضی وقتا سیستم کند می‌شه، دقیق نمی‌دونم از کی شروع شده. فعلاً فقط چند نفر گفتن صفحه دیر لود می‌شه.",
            "call_id": "demo_ambiguous_001"
        }
    ]
    
    print_header("VoiceOps MVP - Working Demo")
    print("\nSelect a scenario:")
    for i, scenario in enumerate(scenarios, 1):
        print(f"  {i}. {scenario['name']}")
    print(f"  {len(scenarios) + 1}. Run all scenarios")
    print(f"  {len(scenarios) + 2}. Custom transcript")
    
    choice = input("\nEnter choice (1-{}): ".format(len(scenarios) + 2))
    
    try:
        choice = int(choice)
    except ValueError:
        print_error("Invalid choice")
        return
    
    if choice == len(scenarios) + 1:
        # Run all scenarios
        for scenario in scenarios:
            print_header(f"Scenario: {scenario['name']}")
            demo_with_transcript(scenario['transcript'], scenario['call_id'])
            input("\nPress Enter to continue to next scenario...")
    elif choice == len(scenarios) + 2:
        # Custom transcript
        transcript = input("\nEnter transcript: ")
        if transcript:
            demo_with_transcript(transcript)
        else:
            print_error("Empty transcript")
    elif 1 <= choice <= len(scenarios):
        # Run selected scenario
        scenario = scenarios[choice - 1]
        demo_with_transcript(scenario['transcript'], scenario['call_id'])
    else:
        print_error("Invalid choice")

if __name__ == "__main__":
    main()

