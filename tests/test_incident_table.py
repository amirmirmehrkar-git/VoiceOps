"""
Table-driven tests for VoiceOps incident processing.

These tests cover the 5 required scenarios plus edge cases.
"""

import pytest
from api.incident import create_incident_from_transcript
from api.schema import validate_incident_strict
from api.scoring import classify_severity


# Test Case 1: Clear sev1 outage
TEST_CASE_1 = {
    "name": "Clear sev1 outage",
    "transcript": "Production API is completely down. All services offline. Started at 6 PM. About 1200 users affected. This is critical.",
    "expected": {
        "severity": "sev1",
        "category": "service_outage",
        "status": "new",
        "impact.services_down": True
    }
}

# Test Case 2: Ambiguous report -> defaults
TEST_CASE_2 = {
    "name": "Ambiguous report -> defaults",
    "transcript": "Something is wrong. Not sure what.",
    "expected": {
        "severity": "sev3",
        "category": "other",
        "status": "new",
        "location.site": "unknown",
        "systems": [{"name": "unknown", "environment": "unknown"}]
    }
}

# Test Case 3: Contains PII -> redaction + pii flags
TEST_CASE_3 = {
    "name": "Contains PII -> redaction + pii flags",
    "transcript": "Patient John Doe, phone 555-1234, email john@example.com reported an issue in room 205.",
    "expected": {
        "pii.contains_pii": True,
        "pii.redaction_applied": True,
        "summary_contains_redacted": True  # Should contain [REDACTED]
    }
}

# Test Case 4: security_incident category
TEST_CASE_4 = {
    "name": "security_incident category",
    "transcript": "Security breach detected. Unauthorized access to user database. Potential data exposure.",
    "expected": {
        "category": "security_incident",
        "severity": "sev1"
    }
}

# Test Case 5: Missing system/location -> fallback values
TEST_CASE_5 = {
    "name": "Missing system/location -> fallback values",
    "transcript": "Something broke. Need help.",
    "expected": {
        "location.site": "unknown",
        "systems": [{"name": "unknown", "environment": "unknown"}]
    }
}

# Test Case 6: Invalid tags (should fail validation)
TEST_CASE_6 = {
    "name": "Invalid tags (should fail)",
    "transcript": "API is down",
    "invalid_tags": ["Invalid Tag", "tag with spaces", "TAG_UPPERCASE"],
    "should_fail": True
}

# Test Case 7: Invalid enum (should fail validation)
TEST_CASE_7 = {
    "name": "Invalid enum (should fail)",
    "transcript": "API is down",
    "invalid_enum": {
        "severity": "INVALID_SEVERITY",
        "category": "invalid_category"
    },
    "should_fail": True
}


@pytest.mark.parametrize("test_case", [
    TEST_CASE_1,
    TEST_CASE_2,
    TEST_CASE_3,
    TEST_CASE_4,
    TEST_CASE_5
])
def test_incident_extraction(test_case):
    """Table-driven test for incident extraction."""
    transcript = test_case["transcript"]
    expected = test_case["expected"]
    
    # Create incident from transcript
    incident = create_incident_from_transcript(transcript)
    
    # Validate schema
    validate_incident_strict(incident)
    
    # Check expected values
    for key, expected_value in expected.items():
        if "." in key:
            # Nested key (e.g., "impact.services_down")
            parts = key.split(".")
            value = incident
            for part in parts:
                value = value.get(part)
            assert value == expected_value, f"{key}: expected {expected_value}, got {value}"
        elif key == "systems":
            # Special handling for systems array
            assert len(incident["systems"]) > 0
            if expected_value[0].get("name") == "unknown":
                assert incident["systems"][0]["name"] == "unknown"
        elif key == "summary_contains_redacted":
            # Check if summary contains [REDACTED]
            assert "[REDACTED]" in incident.get("summary", "")
        else:
            assert incident.get(key) == expected_value, f"{key}: expected {expected_value}, got {incident.get(key)}"


def test_invalid_tags_fails():
    """Test that invalid tags cause validation failure."""
    incident = {
        "schema_version": "1.0.0",
        "source": {"channel": "voice", "vendor": "vapi"},
        "occurred_at": "2025-01-27T14:30:00Z",
        "reported_at": "2025-01-27T14:30:00Z",
        "title": "Test incident",
        "summary": "Test summary for validation",
        "category": "other",
        "severity": "sev3",
        "status": "new",
        "location": {"site": "test"},
        "systems": [{"name": "test"}],
        "tags": ["Invalid Tag", "tag with spaces"],  # Invalid tags
        "confidence": 0.5
    }
    
    with pytest.raises(ValueError):
        validate_incident_strict(incident)


def test_invalid_enum_fails():
    """Test that invalid enum values cause validation failure."""
    incident = {
        "schema_version": "1.0.0",
        "source": {"channel": "voice", "vendor": "vapi"},
        "occurred_at": "2025-01-27T14:30:00Z",
        "reported_at": "2025-01-27T14:30:00Z",
        "title": "Test incident",
        "summary": "Test summary for validation",
        "category": "invalid_category",  # Invalid enum
        "severity": "INVALID_SEVERITY",  # Invalid enum
        "status": "new",
        "location": {"site": "test"},
        "systems": [{"name": "test"}],
        "confidence": 0.5
    }
    
    with pytest.raises(ValueError):
        validate_incident_strict(incident)


def test_severity_classification():
    """Test deterministic severity classification."""
    test_cases = [
        {
            "incident": {
                "category": "service_outage",
                "impact": {"services_down": True}
            },
            "expected": "sev1"
        },
        {
            "incident": {
                "category": "security_incident"
            },
            "expected": "sev1"
        },
        {
            "incident": {
                "category": "performance_degradation",
                "impact": {"users_affected_estimate": 200}
            },
            "expected": "sev2"
        },
        {
            "incident": {
                "category": "data_issue"
            },
            "expected": "sev3"
        },
        {
            "incident": {
                "category": "other"
            },
            "expected": "sev4"
        }
    ]
    
    for test_case in test_cases:
        result = classify_severity(test_case["incident"])
        assert result == test_case["expected"], f"Expected {test_case['expected']}, got {result}"

