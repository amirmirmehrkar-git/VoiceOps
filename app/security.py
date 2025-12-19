"""
VoiceOps MVP Security Module

PII detection and redaction for compliance.
"""

import re

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(r"(\+?\d[\d\s\-]{7,}\d)")
IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def detect_pii(text: str) -> list[str]:
    """
    Detect PII types in text.
    
    Args:
        text: Text to scan for PII
        
    Returns:
        List of detected PII types: ["email", "phone", "ip_address"]
    """
    types = []
    if EMAIL_RE.search(text):
        types.append("email")
    if PHONE_RE.search(text):
        types.append("phone")
    if IP_RE.search(text):
        types.append("ip_address")
    return types


def redact_pii(text: str) -> str:
    """
    Redact PII from text.
    
    Args:
        text: Text containing potential PII
        
    Returns:
        Text with PII redacted
    """
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = PHONE_RE.sub("[REDACTED_PHONE]", text)
    text = IP_RE.sub("[REDACTED_IP]", text)
    return text

