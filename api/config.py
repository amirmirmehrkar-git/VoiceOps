"""
VoiceOps Configuration

Loads configuration from environment variables.
"""

import os
from typing import Optional


def get_vapi_api_key() -> Optional[str]:
    """Get VAPI private API key from environment."""
    return os.getenv("VAPI_API_KEY")


def get_vapi_public_key() -> Optional[str]:
    """Get VAPI public API key from environment."""
    return os.getenv("VAPI_PUBLIC_KEY")


def get_vapi_webhook_secret() -> Optional[str]:
    """Get VAPI webhook secret from environment."""
    return os.getenv("VAPI_WEBHOOK_SECRET")


def get_timezone() -> str:
    """Get default timezone."""
    return os.getenv("VOICEOPS_TIMEZONE", "Europe/Berlin")


# Validate required keys on import
VAPI_API_KEY = get_vapi_api_key()
if not VAPI_API_KEY:
    print("WARNING: VAPI_API_KEY not set in environment variables")

