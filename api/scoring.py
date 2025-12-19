"""
VoiceOps Scoring Module

Calculates confidence scores and severity classification.
"""

from typing import Dict


def calculate_confidence(incident: Dict, transcript: str) -> float:
    """
    Calculate confidence score (0.0 to 1.0) for incident extraction.
    
    Args:
        incident: Incident JSON dict
        transcript: Original transcript text
        
    Returns:
        Confidence score between 0.0 and 1.0
    """
    score = 0.5  # Base score
    
    # Increase confidence if required fields are well-populated
    if incident.get("title") and len(incident["title"]) >= 20:
        score += 0.1
    
    if incident.get("summary") and len(incident["summary"]) >= 50:
        score += 0.1
    
    if incident.get("systems") and len(incident["systems"]) > 0:
        if incident["systems"][0].get("name") != "unknown":
            score += 0.1
    
    if incident.get("location", {}).get("site") != "unknown":
        score += 0.1
    
    # Decrease confidence if PII detected
    if incident.get("pii", {}).get("contains_pii"):
        score -= 0.1
    
    return min(max(score, 0.0), 1.0)


def classify_severity(incident: Dict, transcript: str = "") -> str:
    """
    Deterministic severity classification (sev1-sev4).
    
    Rule-based for speed + explainability.
    
    sev1 if:
    - "down / outage / cannot / 500 / emergency / patient at risk / fire" keywords
    - impact.services_down == true
    - category in {security_incident, patient_safety} with serious text
    
    sev2 if:
    - Severe degradation, high user count, or hard workaround
    
    sev3 default
    
    sev4 only if:
    - minor, cosmetic, low impact
    
    Args:
        incident: Incident JSON dict
        transcript: Optional transcript text for keyword detection
        
    Returns:
        Severity level: "sev1", "sev2", "sev3", or "sev4"
    """
    category = incident.get("category", "other")
    impact = incident.get("impact", {})
    title = incident.get("title", "").lower()
    summary = incident.get("summary", "").lower()
    text = f"{title} {summary} {transcript}".lower()
    
    # Critical keywords for sev1
    critical_keywords = [
        "down", "outage", "cannot", "500", "emergency",
        "patient at risk", "fire", "critical", "urgent",
        "completely down", "not working", "failed"
    ]
    
    # Major keywords for sev2
    major_keywords = [
        "degradation", "slow", "timeout", "high impact",
        "many users", "severe"
    ]
    
    # Minor keywords for sev4
    minor_keywords = [
        "minor", "cosmetic", "low impact", "small issue",
        "not urgent"
    ]
    
    # Check for critical keywords
    has_critical_keywords = any(keyword in text for keyword in critical_keywords)
    
    # sev1 conditions
    if impact.get("services_down") or has_critical_keywords:
        return "sev1"
    
    if category in ["security_incident", "patient_safety"]:
        if has_critical_keywords or impact.get("patient_safety_risk"):
            return "sev1"
    
    # sev2 conditions
    if category == "performance_degradation":
        users = impact.get("users_affected_estimate", 0)
        has_major_keywords = any(keyword in text for keyword in major_keywords)
        if users > 100 or has_major_keywords:
            return "sev2"
    
    # sev4 conditions
    has_minor_keywords = any(keyword in text for keyword in minor_keywords)
    if has_minor_keywords and category == "other":
        return "sev4"
    
    # Default to sev3
    return "sev3"

