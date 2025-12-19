"""
VoiceOps Integration Handlers

Handles integration with external systems (Jira, PagerDuty, etc.)
"""

import os
import requests
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
PAGERDUTY_ROUTING_KEY = os.getenv("PAGERDUTY_ROUTING_KEY")


def create_jira_ticket(incident: Dict) -> Optional[Dict]:
    """
    Create a Jira ticket from an incident.
    
    Args:
        incident: Validated incident JSON dict
        
    Returns:
        Jira ticket response or None if not configured
    """
    if not all([JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN]):
        return None
    
    # Map severity to Jira priority
    severity_map = {
        "sev1": "Highest",
        "sev2": "High",
        "sev3": "Medium",
        "sev4": "Low"
    }
    
    payload = {
        "fields": {
            "project": {"key": os.getenv("JIRA_PROJECT_KEY", "VO")},
            "summary": incident.get("title", "Incident Report"),
            "description": f"""{incident.get("summary", "")}

**Severity**: {incident.get("severity", "sev3")}
**Category**: {incident.get("category", "other")}
**Affected Systems**: {", ".join(s.get("name", "unknown") for s in incident.get("systems", []))}
**Reported At**: {incident.get("reported_at", "")}
**Incident ID**: {incident.get("incident_id", "")}

{incident.get("description", "")}""",
            "issuetype": {"name": "Incident"},
            "priority": {"name": severity_map.get(incident.get("severity", "sev3"), "Medium")},
            "labels": incident.get("tags", [])
        }
    }
    
    try:
        response = requests.post(
            f"{JIRA_URL}/rest/api/3/issue",
            json=payload,
            auth=(JIRA_EMAIL, JIRA_API_TOKEN),
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Jira integration error: {e}")
        return None


def create_pagerduty_incident(incident: Dict) -> Optional[Dict]:
    """
    Create a PagerDuty incident from an incident.
    
    Args:
        incident: Validated incident JSON dict
        
    Returns:
        PagerDuty response or None if not configured
    """
    if not PAGERDUTY_ROUTING_KEY:
        return None
    
    # Map severity to PagerDuty severity
    severity_map = {
        "sev1": "critical",
        "sev2": "error",
        "sev3": "warning",
        "sev4": "info"
    }
    
    payload = {
        "routing_key": PAGERDUTY_ROUTING_KEY,
        "event_action": "trigger",
        "dedup_key": incident.get("incident_id", ""),
        "payload": {
            "summary": incident.get("title", "Incident Report"),
            "source": "VoiceOps",
            "severity": severity_map.get(incident.get("severity", "sev3"), "warning"),
            "custom_details": {
                "incident_id": incident.get("incident_id", ""),
                "category": incident.get("category", "other"),
                "affected_systems": [s.get("name", "unknown") for s in incident.get("systems", [])],
                "reported_at": incident.get("reported_at", ""),
                "description": incident.get("summary", "")
            }
        },
        "links": [
            {
                "href": f"https://voiceops.ai/incidents/{incident.get('incident_id', '')}",
                "text": "View in VoiceOps"
            }
        ]
    }
    
    try:
        response = requests.post(
            "https://events.pagerduty.com/v2/enqueue",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"PagerDuty integration error: {e}")
        return None


def send_webhook(incident: Dict, webhook_url: str) -> bool:
    """
    Send incident to a generic webhook URL.
    
    Args:
        incident: Validated incident JSON dict
        webhook_url: Webhook URL to send to
        
    Returns:
        True if successful, False otherwise
    """
    try:
        response = requests.post(
            webhook_url,
            json=incident,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Webhook error: {e}")
        return False

