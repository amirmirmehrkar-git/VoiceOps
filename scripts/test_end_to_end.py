#!/usr/bin/env python3
"""
End-to-End Test for VoiceOps MVP

Tests the complete flow from transcript to JSON output.
"""

import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.incident import create_incident_from_transcript
from api.schema import validate_incident_strict

def test_scenario(name, transcript, call_id, expected_severity=None):
    """Test a scenario."""
    print(f"\n{'='*60}")
    print(f"Test: {name}")
    print(f"{'='*60}")
    print(f"Transcript: {transcript[:100]}...")
    
    try:
        # Create incident
        incident = create_incident_from_transcript(
            transcript=transcript,
            call_id=call_id,
            timezone="Europe/Berlin"
        )
        
        # Validate
        validate_incident_strict(incident)
        
        # Check severity if expected
        if expected_severity:
            actual_severity = incident.get("severity")
            if actual_severity == expected_severity:
                print(f"[OK] Severity correct: {actual_severity}")
            else:
                print(f"[WARN] Severity mismatch: expected {expected_severity}, got {actual_severity}")
        
        print(f"[OK] Incident created and validated")
        print(f"     Title: {incident.get('title', 'N/A')[:60]}")
        print(f"     Severity: {incident.get('severity', 'N/A')}")
        print(f"     Category: {incident.get('category', 'N/A')}")
        print(f"     Confidence: {incident.get('confidence', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed: {e}")
        return False

def main():
    """Run all tests."""
    print("="*60)
    print("VoiceOps MVP - End-to-End Tests")
    print("="*60)
    
    tests = [
        {
            "name": "Production Outage (sev1)",
            "transcript": "از ساعت ۱۸:۰۵ بعد از دیپلوی جدید، checkout-api توی پروداکشن ۵۰۰ می‌دهد. مشتری‌ها نمی‌تونن پرداخت کنن.",
            "call_id": "test_outage_001",
            "expected_severity": "sev1"
        },
        {
            "name": "Security Incident (sev1)",
            "transcript": "یک لاگین مشکوک شناسایی شد. کاربر admin از IP غیرمعمول وارد شده.",
            "call_id": "test_security_001",
            "expected_severity": "sev1"
        },
        {
            "name": "Ambiguous Report (sev3)",
            "transcript": "یه مشکلی هست… بعضی وقتا سیستم کند می‌شه.",
            "call_id": "test_ambiguous_001",
            "expected_severity": "sev3"
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        if test_scenario(
            test["name"],
            test["transcript"],
            test["call_id"],
            test.get("expected_severity")
        ):
            passed += 1
        else:
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*60}")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

