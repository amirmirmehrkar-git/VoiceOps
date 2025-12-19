"""
VAPI Webhook Handler

Receives webhooks from VAPI and processes incident reports.
"""

import json
from datetime import datetime, timezone
from typing import Dict, Optional

from .incident import create_incident_from_transcript
from .schema import validate_incident_strict
from .integrations import create_jira_ticket, create_pagerduty_incident


def handle_vapi_webhook(webhook_data: Dict) -> Dict:
    """
    Handle webhook from VAPI.
    
    Expected webhook events:
    - end-of-call-report: Contains transcript
    - conversation-update: Real-time updates
    
    Args:
        webhook_data: Webhook payload from VAPI
        
    Returns:
        Processed incident JSON dict
    """
    event_type = webhook_data.get("type")
    
    if event_type == "end-of-call-report":
        return handle_end_of_call(webhook_data)
    elif event_type == "conversation-update":
        return handle_conversation_update(webhook_data)
    else:
        return {"status": "ignored", "event_type": event_type}


def handle_end_of_call(webhook_data: Dict) -> Dict:
    """
    Handle end-of-call-report webhook.
    
    Extracts transcript and creates incident.
    """
    call = webhook_data.get("call", {})
    transcript = call.get("transcript", "")
    call_id = call.get("id")
    
    if not transcript:
        return {"status": "error", "message": "No transcript in webhook"}
    
    # Create incident from transcript
    try:
        incident = create_incident_from_transcript(
            transcript=transcript,
            call_id=call_id,
            timezone="Europe/Berlin"
        )
        
        # Validate
        validate_incident_strict(incident)
        
        # Send to integrations (optional, non-blocking)
        jira_ticket = create_jira_ticket(incident)
        pagerduty_incident = create_pagerduty_incident(incident)
        
        return {
            "status": "success",
            "incident": incident,
            "integrations": {
                "jira": jira_ticket is not None,
                "pagerduty": pagerduty_incident is not None
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def handle_conversation_update(webhook_data: Dict) -> Dict:
    """
    Handle conversation-update webhook (real-time).
    
    Can be used for live incident updates.
    """
    # TODO: Implement real-time processing if needed
    return {"status": "received", "type": "conversation-update"}

