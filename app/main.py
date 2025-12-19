"""
VoiceOps MVP FastAPI Application

Main FastAPI app with VAPI webhook endpoint.
"""

import os
import uuid
from fastapi import FastAPI, Request, HTTPException
from dotenv import load_dotenv

from app.models import Incident, VapiWebhookPayload, Notes, PII
from app.scoring import score_severity
from app.security import detect_pii, redact_pii
from app.validator import validate_against_schema

load_dotenv()

app = FastAPI(title="VoiceOps MVP")


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"ok": True}


@app.post("/webhook/vapi")
async def vapi_webhook(req: Request):
    """
    VAPI webhook endpoint.
    
    Accepts VAPI webhook payload and returns validated incident JSON.
    
    Expected VAPI payload structure:
    {
      "type": "end-of-call",
      "call": {
        "id": "call_abc123",
        "transcript": "Full transcript text here..."
      }
    }
    """
    try:
        payload_json = await req.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    
    # Parse VAPI payload
    try:
        payload = VapiWebhookPayload(**payload_json)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid payload structure: {str(e)}")
    
    # Extract transcript from VAPI payload (flexible extraction)
    # VAPI may send transcript in call.transcript or at root level
    transcript = (
        (payload.call.transcript if payload.call else None) or
        payload.transcript or
        ""
    ).strip()
    
    # Extract call_id
    call_id = (
        (payload.call.id if payload.call else None) or
        (payload.call.call_id if payload.call else None) or
        None
    )
    
    # 1) Detect + redact PII
    pii_types = detect_pii(transcript)
    contains_pii = len(pii_types) > 0
    redacted_text = redact_pii(transcript)
    
    # 2) Category (MVP heuristic)
    category = "security_incident" if any(
        k in transcript.lower() for k in ["token", "suspicious login", "breach"]
    ) else "operational_outage"
    
    # 3) Severity (deterministic)
    severity = score_severity(transcript, category)
    
    # 4) Build incident
    incident = Incident(
        incident_id=f"inc_{uuid.uuid4().hex[:8]}",
        title=(redacted_text[:110] or "Voice incident"),
        summary=(redacted_text or "No transcript provided"),
        category=category,
        severity=severity,
        confidence=0.75 if transcript else 0.4,
        pii=PII(contains_pii=contains_pii, pii_types=pii_types, redacted=contains_pii),
        notes=Notes(
            severity_reasoning=f"Rule-based scoring for category={category}.",
            category_reasoning="Heuristic keyword routing based on transcript."
        ),
    )
    
    # 5) Schema validate (the "production grade" point)
    incident_dict = incident.model_dump()
    try:
        validate_against_schema(incident_dict)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {"ok": True, "incident": incident_dict}

