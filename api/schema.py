"""
VoiceOps Schema Validation

Validates incident JSON against the schema using JSON Schema 2020-12.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

from jsonschema import Draft202012Validator, ValidationError


SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "incident.v1.json"


def load_schema() -> Dict:
    """Load the incident schema from file."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_incident(incident: Dict, schema: Optional[Dict] = None) -> List[str]:
    """
    Validate incident JSON against schema.
    
    Args:
        incident: Incident JSON dict to validate
        schema: Optional schema dict (loads from file if not provided)
        
    Returns:
        List of validation error messages (empty if valid)
    """
    if schema is None:
        schema = load_schema()
    
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(incident), key=lambda e: e.path)
    
    return [f"{'.'.join(str(p) for p in e.path)}: {e.message}" for e in errors]


def validate_incident_strict(incident: Dict) -> bool:
    """
    Strict validation that raises exception on error.
    
    Args:
        incident: Incident JSON dict to validate
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If incident doesn't match schema
    """
    errors = validate_incident(incident)
    if errors:
        raise ValueError(f"Schema validation failed: {'; '.join(errors)}")
    return True


def validate_incident_safe(incident: Dict) -> tuple[bool, Optional[str]]:
    """
    Safe validation that returns (is_valid, error_message).
    
    Args:
        incident: Incident JSON dict to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    errors = validate_incident(incident)
    if errors:
        return False, "; ".join(errors)
    return True, None

