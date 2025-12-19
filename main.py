"""
VoiceOps FastAPI Application

Main FastAPI app for VoiceOps incident management API.
"""

import os
import sys
from datetime import datetime
from typing import Dict, Optional
from uuid import uuid4

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Load environment variables from .env.local
load_dotenv('.env.local')

from api.incident import create_incident_from_transcript
from api.schema import validate_incident, validate_incident_strict
from api.vapi_webhook import handle_vapi_webhook

# Fix Unicode output for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Initialize FastAPI app
app = FastAPI(
    title="VoiceOps API",
    description="Voice-first incident ingestion system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for incidents (replace with database in production)
incidents_store: Dict[str, Dict] = {}


# Request Models
class IncidentCreateRequest(BaseModel):
    """Request model for creating an incident from transcript."""
    transcript: str = Field(..., min_length=1, description="Voice transcript text")
    call_id: Optional[str] = Field(None, description="VAPI call ID for idempotency")
    timezone: Optional[str] = Field("Europe/Berlin", description="IANA timezone string")


class IncidentValidateRequest(BaseModel):
    """Request model for validating incident JSON."""
    incident: Dict = Field(..., description="Incident JSON to validate")


class VAPIWebhookRequest(BaseModel):
    """Request model for VAPI webhook."""
    type: str = Field(..., description="Webhook event type")
    call: Optional[Dict] = Field(None, description="Call data")
    transcript: Optional[str] = Field(None, description="Call transcript")
    assistant: Optional[Dict] = Field(None, description="Assistant data")


# Response Models
class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    version: str


class IncidentResponse(BaseModel):
    """Incident creation response."""
    incident: Dict
    created: bool
    incident_id: str


class ValidationResponse(BaseModel):
    """Validation response."""
    valid: bool
    errors: list


# Error Handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": str(exc), "type": "validation_error"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "type": "server_error"}
    )


# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "message": "VoiceOps API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"], response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat() + "Z",
        version="1.0.0"
    )


@app.post("/api/v1/incidents", tags=["Incidents"], response_model=IncidentResponse, status_code=status.HTTP_201_CREATED)
async def create_incident(request: IncidentCreateRequest):
    """
    Create an incident from a voice transcript.
    
    This endpoint:
    1. Processes the transcript using LLM
    2. Validates against schema
    3. Calculates severity and confidence
    4. Stores the incident
    
    Args:
        request: Incident creation request with transcript
        
    Returns:
        Created incident JSON
        
    Raises:
        HTTPException: If incident creation fails
    """
    try:
        # Check for idempotency (if call_id provided)
        if request.call_id:
            # Look for existing incident with same call_id
            for incident_id, incident in incidents_store.items():
                source = incident.get("source", {})
                if source.get("call_id") == request.call_id:
                    return IncidentResponse(
                        incident=incident,
                        created=False,
                        incident_id=incident_id
                    )
        
        # Create incident from transcript
        incident = create_incident_from_transcript(
            transcript=request.transcript,
            call_id=request.call_id,
            timezone=request.timezone or "Europe/Berlin"
        )
        
        # Get incident_id from created incident
        incident_id = incident.get("incident_id")
        if not incident_id:
            incident_id = str(uuid4())
            incident["incident_id"] = incident_id
        
        # Store incident
        incidents_store[incident_id] = incident
        
        return IncidentResponse(
            incident=incident,
            created=True,
            incident_id=incident_id
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create incident: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/api/v1/incidents/{incident_id}", tags=["Incidents"])
async def get_incident(incident_id: str):
    """
    Get an incident by ID.
    
    Args:
        incident_id: Incident identifier
        
    Returns:
        Incident JSON
        
    Raises:
        HTTPException: If incident not found
    """
    if incident_id not in incidents_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident {incident_id} not found"
        )
    
    return incidents_store[incident_id]


@app.post("/api/v1/incidents/validate", tags=["Incidents"], response_model=ValidationResponse)
async def validate_incident_endpoint(request: IncidentValidateRequest):
    """
    Validate an incident JSON against the schema.
    
    Args:
        request: Validation request with incident JSON
        
    Returns:
        Validation result with errors if any
    """
    errors = validate_incident(request.incident)
    
    return ValidationResponse(
        valid=len(errors) == 0,
        errors=errors
    )


@app.post("/api/v1/vapi/webhook", tags=["VAPI"], status_code=status.HTTP_200_OK)
async def vapi_webhook(request: VAPIWebhookRequest):
    """
    Handle VAPI webhook events.
    
    Supported event types:
    - end-of-call: Process transcript and create incident
    
    Args:
        request: VAPI webhook request
        
    Returns:
        Success response
    """
    # Convert Pydantic model to dict for webhook handler
    webhook_data = request.dict()
    
    # Use dedicated webhook handler
    result = handle_vapi_webhook(webhook_data)
    
    # If incident was created, store it
    if result.get("status") == "success" and result.get("incident_id"):
        # Fetch the incident (it should be created by handle_vapi_webhook)
        # For now, we'll need to get it from the incident creation
        pass
    
    # Return result
    if result.get("status") == "error":
        status_code = status.HTTP_400_BAD_REQUEST if "No transcript" in result.get("error", "") else status.HTTP_500_INTERNAL_SERVER_ERROR
        return JSONResponse(
            status_code=status_code,
            content=result
        )
    
    return result


@app.get("/api/v1/incidents", tags=["Incidents"])
async def list_incidents(limit: int = 10, offset: int = 0):
    """
    List all incidents (paginated).
    
    Args:
        limit: Maximum number of incidents to return
        offset: Number of incidents to skip
        
    Returns:
        List of incidents
    """
    incidents_list = list(incidents_store.values())
    
    # Pagination
    start = offset
    end = offset + limit
    
    return {
        "incidents": incidents_list[start:end],
        "total": len(incidents_list),
        "limit": limit,
        "offset": offset
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )

