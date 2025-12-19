"""
VAPI Webhook Handler

Handles webhook events from VAPI and processes them into incidents.
"""

import os
from typing import Dict, Optional
from datetime import datetime

from .incident import create_incident_from_transcript


def handle_vapi_webhook(webhook_data: Dict) -> Dict:
    """
    Handle VAPI webhook event.
    
    Supported event types:
    - end-of-call: Process transcript and create incident
    
    Args:
        webhook_data: VAPI webhook payload
        
    Returns:
        Response dict with status and incident_id if created
    """
    event_type = webhook_data.get("type")
    
    if event_type == "end-of-call":
        return handle_end_of_call(webhook_data)
    elif event_type == "call-started":
        return {"status": "acknowledged", "type": "call-started"}
    elif event_type == "speech-update":
        return {"status": "acknowledged", "type": "speech-update"}
    else:
        return {
            "status": "acknowledged",
            "type": event_type,
            "message": f"Event type {event_type} received but not processed"
        }


def handle_end_of_call(webhook_data: Dict) -> Dict:
    """
    Handle end-of-call event from VAPI.
    
    Extracts transcript and creates incident.
    
    Args:
        webhook_data: VAPI webhook payload with call data
        
    Returns:
        Response dict with status and incident_id
    """
    # Extract call data
    call_data = webhook_data.get("call", {})
    call_id = call_data.get("id")
    
    # Extract transcript
    transcript = webhook_data.get("transcript") or call_data.get("transcript", "")
    
    if not transcript:
        return {
            "status": "error",
            "error": "No transcript found in webhook",
            "call_id": call_id
        }
    
    # Extract timezone (default to Europe/Berlin)
    timezone = call_data.get("timezone") or "Europe/Berlin"
    
    try:
        # Create incident from transcript
        incident = create_incident_from_transcript(
            transcript=transcript,
            call_id=call_id,
            timezone=timezone
        )
        
        incident_id = incident.get("incident_id")
        
        return {
            "status": "success",
            "incident_id": incident_id,
            "call_id": call_id,
            "message": "Incident created successfully from VAPI webhook"
        }
        
    except ValueError as e:
        return {
            "status": "error",
            "error": str(e),
            "call_id": call_id
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Internal error: {str(e)}",
            "call_id": call_id
        }


def extract_transcript_from_webhook(webhook_data: Dict) -> Optional[str]:
    """
    Extract transcript from VAPI webhook in various formats.
    
    Args:
        webhook_data: VAPI webhook payload
        
    Returns:
        Transcript text or None
    """
    # Try different possible locations for transcript
    transcript = (
        webhook_data.get("transcript") or
        webhook_data.get("call", {}).get("transcript") or
        webhook_data.get("message", {}).get("transcript") or
        webhook_data.get("data", {}).get("transcript")
    )
    
    return transcript


def extract_call_id_from_webhook(webhook_data: Dict) -> Optional[str]:
    """
    Extract call ID from VAPI webhook.
    
    Args:
        webhook_data: VAPI webhook payload
        
    Returns:
        Call ID or None
    """
    call_id = (
        webhook_data.get("call_id") or
        webhook_data.get("call", {}).get("id") or
        webhook_data.get("call", {}).get("call_id")
    )
    
    return call_id

