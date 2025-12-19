"""
VoiceOps API - FastAPI Application

Main entry point for the VoiceOps incident reporting API.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
from typing import Dict, Optional

from api.incident import create_incident_from_transcript
from api.vapi_webhook import handle_vapi_webhook
from api.schema import validate_incident_strict
from api.scoring import classify_severity
from api.config import get_vapi_api_key
from api.demo import router as demo_router

app = FastAPI(
    title="VoiceOps API",
    description="Voice-first incident reporting and management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include demo router
app.include_router(demo_router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "VoiceOps API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check for deployment."""
    return {"status": "healthy"}


@app.post("/api/v1/incidents")
async def create_incident(request: Request):
    """
    Create an incident from a transcript.
    
    Expected JSON body:
    {
        "transcript": "string",
        "call_id": "optional string",
        "timezone": "optional string (default: Europe/Berlin)"
    }
    """
    try:
        body = await request.json()
        transcript = body.get("transcript")
        
        if not transcript:
            raise HTTPException(status_code=400, detail="transcript is required")
        
        call_id = body.get("call_id")
        timezone = body.get("timezone", "Europe/Berlin")
        
        # Create incident
        incident = create_incident_from_transcript(
            transcript=transcript,
            call_id=call_id,
            timezone=timezone
        )
        
        # Ensure severity is set
        if not incident.get("severity"):
            incident["severity"] = classify_severity(incident, transcript)
        
        return JSONResponse(content=incident, status_code=201)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/api/v1/vapi/webhook")
async def vapi_webhook(request: Request):
    """
    Handle webhook from VAPI.
    
    Processes end-of-call reports and creates incidents.
    """
    try:
        webhook_data = await request.json()
        result = handle_vapi_webhook(webhook_data)
        
        if result.get("status") == "error":
            raise HTTPException(status_code=400, detail=result.get("message"))
        
        return JSONResponse(content=result, status_code=200)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook processing error: {str(e)}")


@app.post("/api/v1/incidents/validate")
async def validate_incident_endpoint(request: Request):
    """
    Validate an incident JSON against the schema.
    
    Expected JSON body: incident JSON object
    """
    try:
        incident = await request.json()
        validate_incident_strict(incident)
        return {"valid": True, "message": "Incident is valid"}
        
    except ValueError as e:
        return JSONResponse(
            content={"valid": False, "error": str(e)},
            status_code=400
        )


@app.get("/api/v1/incidents/{incident_id}")
async def get_incident(incident_id: str):
    """
    Get an incident by ID.
    
    TODO: Implement database storage
    """
    return {"message": "Not implemented yet", "incident_id": incident_id}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

