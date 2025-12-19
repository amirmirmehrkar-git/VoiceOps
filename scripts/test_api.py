#!/usr/bin/env python3
"""
Test VoiceOps API endpoints
"""

import requests
import json
import sys

# Fix Unicode output for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

API_BASE = "http://localhost:8000"

def test_health():
    """Test health check endpoint."""
    print("🔍 Testing /health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Health check passed: {response.json()}")
            return True
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Cannot connect to API. Is it running?")
        print(f"   💡 Start API with: python main.py")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_create_incident():
    """Test incident creation endpoint."""
    print("\n🔍 Testing POST /api/v1/incidents...")
    try:
        payload = {
            "transcript": "Production API is completely down. All services offline. Started at 6 PM. About 1200 users affected. This is critical.",
            "call_id": "test_call_001",
            "timezone": "Europe/Berlin"
        }
        
        response = requests.post(
            f"{API_BASE}/api/v1/incidents",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 201:
            data = response.json()
            print(f"   ✅ Incident created successfully!")
            print(f"   📝 Incident ID: {data.get('incident_id')}")
            print(f"   📝 Severity: {data.get('incident', {}).get('severity')}")
            print(f"   📝 Category: {data.get('incident', {}).get('category')}")
            return data.get('incident_id')
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def test_get_incident(incident_id):
    """Test get incident endpoint."""
    if not incident_id:
        return
    
    print(f"\n🔍 Testing GET /api/v1/incidents/{incident_id}...")
    try:
        response = requests.get(f"{API_BASE}/api/v1/incidents/{incident_id}", timeout=5)
        
        if response.status_code == 200:
            print(f"   ✅ Incident retrieved successfully!")
            incident = response.json()
            print(f"   📝 Title: {incident.get('title')}")
            print(f"   📝 Severity: {incident.get('severity')}")
            return True
        else:
            print(f"   ❌ Failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_validate_incident():
    """Test incident validation endpoint."""
    print("\n🔍 Testing POST /api/v1/incidents/validate...")
    try:
        # Load demo incident
        with open("demo_incident.json", "r", encoding="utf-8") as f:
            incident = json.load(f)
        
        payload = {"incident": incident}
        
        response = requests.post(
            f"{API_BASE}/api/v1/incidents/validate",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('valid'):
                print(f"   ✅ Incident validation passed!")
                return True
            else:
                print(f"   ⚠️  Validation failed:")
                for error in data.get('errors', []):
                    print(f"      - {error}")
                return False
        else:
            print(f"   ❌ Failed: {response.status_code}")
            return False
            
    except FileNotFoundError:
        print(f"   ⚠️  demo_incident.json not found, skipping validation test")
        return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("🧪 VoiceOps API Tests")
    print("=" * 60)
    print()
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ API is not running. Please start it first:")
        print("   python main.py")
        sys.exit(1)
    
    # Test 2: Create incident
    incident_id = test_create_incident()
    
    # Test 3: Get incident
    if incident_id:
        test_get_incident(incident_id)
    
    # Test 4: Validate incident
    test_validate_incident()
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Tests completed!")
    print("=" * 60)
    print("\n💡 API Documentation:")
    print(f"   Swagger UI: {API_BASE}/docs")
    print(f"   ReDoc: {API_BASE}/redoc")

if __name__ == "__main__":
    main()

