"""
VoiceOps MVP Models

Pydantic models for incident data structures.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime

Category = Literal[
    "operational_outage",
    "performance_degradation",
    "security_incident",
    "data_issue",
    "unknown",
]

Severity = Literal["sev1", "sev2", "sev3", "sev4"]


class PII(BaseModel):
    contains_pii: bool = False
    pii_types: List[str] = Field(default_factory=list)
    redacted: bool = False


class Notes(BaseModel):
    severity_reasoning: Optional[str] = None
    category_reasoning: Optional[str] = None


class Incident(BaseModel):
    incident_id: str
    title: str
    summary: str
    category: Category
    severity: Severity
    confidence: float = Field(ge=0, le=1)
    pii: PII
    notes: Optional[Notes] = None


class CallData(BaseModel):
    """VAPI call data structure."""
    id: Optional[str] = None
    transcript: Optional[str] = None
    call_id: Optional[str] = None


class VapiWebhookPayload(BaseModel):
    """
    VAPI webhook payload structure.
    
    VAPI sends:
    {
      "type": "end-of-call",
      "call": {
        "id": "call_abc123",
        "transcript": "Full transcript text here..."
      }
    }
    """
    type: str = Field(..., description="Webhook event type (e.g., 'end-of-call')")
    call: Optional[CallData] = None
    transcript: Optional[str] = None  # Sometimes transcript is at root level

