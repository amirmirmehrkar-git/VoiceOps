"""
VoiceOps Incident API

Handles incident creation, validation, and processing.
"""

import json
import re
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple
from uuid import uuid4

from .schema import validate_incident_strict, validate_incident
from .scoring import calculate_confidence, classify_severity
from .llm import call_llm_for_incident, validate_and_repair


def redact_pii(text: str) -> Tuple[str, bool]:
    """
    Redact PII from text.
    
    Detects:
    - Email addresses
    - Phone numbers (Iranian format: 09xx-xxx-xxxx)
    - Names (simple heuristic)
    
    Args:
        text: Text that may contain PII
        
    Returns:
        Tuple of (redacted_text, had_pii)
    """
    had_pii = False
    redacted = text
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.search(email_pattern, redacted):
        redacted = re.sub(email_pattern, "[REDACTED]", redacted)
        had_pii = True
    
    # Phone number patterns (Iranian)
    phone_patterns = [
        r'09\d{2}[\s\-]?\d{3}[\s\-]?\d{4}',  # 09123456789
        r'\+98[\s\-]?9\d{2}[\s\-]?\d{3}[\s\-]?\d{4}',  # +989123456789
        r'0\d{2}[\s\-]?\d{3}[\s\-]?\d{4}',  # 02112345678
    ]
    for pattern in phone_patterns:
        if re.search(pattern, redacted):
            redacted = re.sub(pattern, "[REDACTED]", redacted)
            had_pii = True
    
    # Simple name detection (Persian/English names with common patterns)
    # This is a basic heuristic - in production, use a proper NER model
    name_patterns = [
        r'\b(?:آقای|خانم|دکتر|مهندس)\s+[آ-ی]{2,}\s+[آ-ی]{2,}\b',  # Persian titles + names
        r'\b(?:Mr|Mrs|Ms|Dr)\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b',  # English titles + names
    ]
    for pattern in name_patterns:
        if re.search(pattern, redacted, re.IGNORECASE):
            # Don't redact everything, just flag it
            had_pii = True
    
    return redacted, had_pii


def create_incident_from_transcript(
    transcript: str,
    call_id: Optional[str] = None,
    timezone: str = "Europe/Berlin"
) -> Dict:
    """
    Create an incident from a voice transcript.
    
    This function:
    1. Checks for PII and redacts if found
    2. Calls LLM with optimized prompt (schema summary, not full schema)
    3. Validates output against full schema file
    4. Attempts repair if invalid
    5. Calculates confidence score
    6. Classifies severity
    
    Args:
        transcript: Raw transcript text from VAPI
        call_id: Optional call identifier for idempotency
        timezone: IANA timezone string
        
    Returns:
        Validated incident JSON dict
        
    Raises:
        ValueError: If incident cannot be created or validated
    """
    # Step 1: Check and redact PII
    redacted_transcript, has_pii = redact_pii(transcript)
    
    # Step 2: Call LLM with optimized prompt (schema summary only)
    try:
        incident = call_llm_for_incident(redacted_transcript, call_id)
    except (NotImplementedError, ValueError) as e:
        # Fallback for development/testing
        incident = _create_fallback_incident(redacted_transcript, call_id, timezone, has_pii)
    
    # Step 3: Validate against full schema file
    errors = validate_incident(incident)
    
    if errors:
        # Step 4: Attempt repair
        try:
            incident = validate_and_repair(incident, max_repairs=1)
        except (ValueError, NotImplementedError):
            # If repair fails, raise with clear error
            raise ValueError(f"LLM output invalid and repair failed: {'; '.join(errors)}")
    
    # Step 5: Strict validation (guarantees valid output)
    validate_incident_strict(incident)
    
    # Step 6: Set PII flags
    if has_pii:
        incident["pii"] = {
            "contains_pii": True,
            "redaction_applied": True
        }
        # Redact PII in summary/description if present
        if "summary" in incident:
            incident["summary"], _ = redact_pii(incident["summary"])
        if "description" in incident:
            incident["description"], _ = redact_pii(incident["description"])
    
    # Step 7: Calculate confidence
    incident["confidence"] = calculate_confidence(incident, redacted_transcript)
    
    # Step 8: Classify severity (if not already set or needs override)
    if not incident.get("severity") or incident.get("severity") == "sev3":
        incident["severity"] = classify_severity(incident, redacted_transcript)
    
    return incident


def _create_fallback_incident(
    transcript: str,
    call_id: Optional[str],
    timezone: str,
    has_pii: bool = False
) -> Dict:
    """Fallback incident creation for development/testing."""
    from datetime import timezone as tz
    now = datetime.now(tz.utc).isoformat()
    
    # Basic severity classification (improved for Persian)
    text_lower = transcript.lower()
    
    # Check for critical keywords (Persian + English)
    critical_keywords = ["down", "outage", "500", "emergency", "خراب", "خطا", "نمی‌شه", "نمی‌تونن", "۵۰۰"]
    major_keywords = ["slow", "degradation", "performance", "کند", "آهسته"]
    security_keywords = ["security", "breach", "hack", "suspicious", "امنیت", "نفوذ", "مشکوک"]
    
    if any(kw in text_lower for kw in critical_keywords) or "۵۰۰" in transcript or "500" in text_lower:
        severity = "sev1"
        category = "service_outage"
    elif any(kw in text_lower for kw in security_keywords):
        severity = "sev1"
        category = "security_incident"
    elif any(kw in text_lower for kw in major_keywords):
        severity = "sev2"
        category = "performance_degradation"
    else:
        severity = "sev3"
        category = "other"
    
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
        "title": (transcript[:120] if len(transcript) >= 8 else "Incident reported via voice")[:120],
        "summary": (transcript[:500] if len(transcript) >= 20 else "Incident reported. Details to be confirmed.")[:500],
        "category": category,
        "severity": severity,
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
            "contains_pii": has_pii,
            "redaction_applied": has_pii
        },
        "confidence": 0.5
    }
