"""
VoiceOps MVP Scoring Module

Rule-based severity scoring for consistency and auditability.
"""


def score_severity(transcript: str, category: str) -> str:
    """
    Deterministic severity scoring based on transcript and category.
    
    Args:
        transcript: Voice transcript text
        category: Incident category
        
    Returns:
        Severity level: "sev1", "sev2", "sev3", or "sev4"
    """
    t = (transcript or "").lower()
    
    # Security incidents are always sev1
    if category == "security_incident":
        return "sev1"
    
    # Critical keywords for sev1
    if any(k in t for k in ["down", "outage", "500", "payment failed", "cannot checkout"]):
        return "sev1"
    
    # Performance issues for sev2
    if any(k in t for k in ["slow", "latency", "degraded", "timeouts"]):
        return "sev2"
    
    # General issues for sev3
    if any(k in t for k in ["bug", "issue", "error"]):
        return "sev3"
    
    # Default to sev4
    return "sev4"

