"""
VoiceOps Incident API

Handles incident creation, validation, and processing.
"""

import json
from datetime import datetime, timezone
from typing import Dict, Optional
from uuid import uuid4

from .schema import validate_incident_strict, validate_incident
from .scoring import calculate_confidence
from .llm import call_llm_for_incident, validate_and_repair


def create_incident_from_transcript(
    transcript: str,
    call_id: Optional[str] = None,
    timezone: str = "Europe/Berlin"
) -> Dict:
    """
    Create an incident from a voice transcript.
    
    This function:
    1. Calls LLM with optimized prompt (schema summary, not full schema)
    2. Validates output against full schema file
    3. Attempts repair if invalid
    4. Calculates confidence score
    
    Args:
        transcript: Raw transcript text from VAPI
        call_id: Optional call identifier for idempotency
        timezone: IANA timezone string
        
    Returns:
        Validated incident JSON dict
        
    Raises:
        ValueError: If incident cannot be created or validated
    """
    # Step 1: Call LLM with optimized prompt (schema summary only)
    try:
        incident = call_llm_for_incident(transcript, call_id)
    except NotImplementedError:
        # Fallback for development/testing
        incident = _create_fallback_incident(transcript, call_id, timezone)
    
    # Step 2: Validate against full schema file
    errors = validate_incident(incident)
    
    if errors:
        # Step 3: Attempt repair
        try:
            incident = validate_and_repair(incident, max_repairs=1)
        except (ValueError, NotImplementedError):
            # If repair fails, raise with clear error
            raise ValueError(f"LLM output invalid and repair failed: {'; '.join(errors)}")
    
    # Step 4: Strict validation (guarantees valid output)
    validate_incident_strict(incident)
    
    # Step 5: Calculate confidence
    incident["confidence"] = calculate_confidence(incident, transcript)
    
    return incident


def _create_fallback_incident(
    transcript: str,
    call_id: Optional[str],
    timezone: str
) -> Dict:
    """Fallback incident creation for development/testing."""
    now = datetime.now(timezone.utc).isoformat()
    
    return {
        "schema_version": "1.0.0",
        "incident_id": str(uuid4()),
        "source": {
            "channel": "voice",
            "vendor": "vapi",
            "call_id": call_id or f"call_{uuid4().hex[:8]}"
        },
        "occurred_at": now,
        "reported_at": now,
        "timezone": timezone,
        "title": transcript[:120] if len(transcript) >= 8 else "Incident reported via voice",
        "summary": transcript[:500] if len(transcript) >= 20 else "Incident reported. Details to be confirmed.",
        "category": "other",
        "severity": "sev3",
        "status": "new",
        "location": {
            "site": "unknown"
        },
        "systems": [
            {
                "name": "unknown",
                "environment": "unknown"
            }
        ],
        "tags": [],
        "pii": {
            "contains_pii": False,
            "redaction_applied": False
        },
        "confidence": 0.5
    }


def redact_pii(text: str) -> tuple[str, bool]:
    """
    Redact PII from text.
    
    Args:
        text: Text that may contain PII
        
    Returns:
        Tuple of (redacted_text, had_pii)
    """
    # TODO: Implement PII detection and redaction
    # This is where CodeRabbit would help identify security issues
    return text, False

