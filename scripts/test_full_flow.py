#!/usr/bin/env python3
"""
Full Flow Test - VoiceOps End-to-End
Tests the complete flow: Transcript → Incident → JSON
"""

import requests
import json
import sys
from datetime import datetime

# Fix Unicode output for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

API_BASE = "http://localhost:8000"

def test_scenario(name, transcript, expected_severity=None, expected_category=None):
    """Test a complete scenario."""
    print(f"\n{'='*60}")
    print(f"📋 Scenario: {name}")
    print(f"{'='*60}")
    print(f"📝 Transcript: {transcript[:100]}...")
    
    try:
        # Create incident
        response = requests.post(
            f"{API_BASE}/api/v1/incidents",
            json={
                "transcript": transcript,
                "call_id": f"test_{datetime.now().timestamp()}",
                "timezone": "Europe/Berlin"
            },
            timeout=30
        )
        
        if response.status_code == 201:
            data = response.json()
            incident = data.get('incident', {})
            
            print(f"   ✅ Incident created!")
            print(f"   📝 ID: {data.get('incident_id')}")
            print(f"   📝 Severity: {incident.get('severity')}")
            print(f"   📝 Category: {incident.get('category')}")
            print(f"   📝 Confidence: {incident.get('confidence', 0):.2f}")
            print(f"   📝 Title: {incident.get('title', 'N/A')[:60]}...")
            
            # Check expectations
            if expected_severity and incident.get('severity') != expected_severity:
                print(f"   ⚠️  Expected severity: {expected_severity}, got: {incident.get('severity')}")
            
            if expected_category and incident.get('category') != expected_category:
                print(f"   ⚠️  Expected category: {expected_category}, got: {incident.get('category')}")
            
            return True
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_vapi_webhook():
    """Test VAPI webhook endpoint."""
    print(f"\n{'='*60}")
    print(f"📋 Testing VAPI Webhook")
    print(f"{'='*60}")
    
    try:
        webhook_data = {
            "type": "end-of-call",
            "call": {
                "id": "vapi_test_call_001",
                "timezone": "Europe/Berlin"
            },
            "transcript": "Production database is experiencing high latency. Response times are 5-10 seconds. Users are reporting slow page loads."
        }
        
        response = requests.post(
            f"{API_BASE}/api/v1/vapi/webhook",
            json=webhook_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                print(f"   ✅ Webhook processed successfully!")
                print(f"   📝 Incident ID: {data.get('incident_id')}")
                return True
            else:
                print(f"   ⚠️  Status: {data.get('status')}")
                print(f"   Response: {data}")
                return False
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("🚀 VoiceOps Full Flow Test")
    print("=" * 60)
    
    # Test health
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code != 200:
            print("\n❌ API is not running. Please start it first:")
            print("   python main.py")
            sys.exit(1)
    except:
        print("\n❌ Cannot connect to API. Please start it first:")
        print("   python main.py")
        sys.exit(1)
    
    results = []
    
    # Scenario 1: Critical Outage
    results.append((
        "Critical Outage (sev1)",
        test_scenario(
            "Critical Outage",
            "Production API is completely down. All services offline. Started at 6 PM. About 1200 users affected. This is critical.",
            expected_severity="sev1"
        )
    ))
    
    # Scenario 2: Performance Issue
    results.append((
        "Performance Issue (sev2)",
        test_scenario(
            "Performance Issue",
            "Database queries are very slow. Response times increased from 200ms to 2 seconds. About 500 users affected.",
            expected_severity="sev2"
        )
    ))
    
    # Scenario 3: Security Incident
    results.append((
        "Security Incident",
        test_scenario(
            "Security Incident",
            "Suspicious login detected. User admin logged in from unknown IP address. Possible token leak. Immediate security review required.",
            expected_category="security_incident"
        )
    ))
    
    # Scenario 4: Ambiguous Report
    results.append((
        "Ambiguous Report (defaults)",
        test_scenario(
            "Ambiguous Report",
            "Something is wrong. Not sure what. Some users mentioned issues.",
            expected_severity="sev3"
        )
    ))
    
    # Test VAPI Webhook
    results.append((
        "VAPI Webhook",
        test_vapi_webhook()
    ))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {status} - {name}")
    
    print(f"\n   Total: {passed}/{total} passed")
    
    if passed == total:
        print("\n✅ All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    print("\n💡 Next steps:")
    print(f"   - View API docs: {API_BASE}/docs")
    print(f"   - View output: file:///{sys.path[0].replace(chr(92), '/')}/view_output.html")

if __name__ == "__main__":
    main()

