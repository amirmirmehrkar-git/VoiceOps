"""
VoiceOps MVP Validator Module

JSON Schema validation for production-grade incident data.
"""

import json
from pathlib import Path
from jsonschema import Draft202012Validator, ValidationError


_SCHEMA = None
_VALIDATOR = None


def load_schema(path: str = "schemas/incident.v1.mvp.json") -> dict:
    """
    Load JSON Schema from file.
    
    Args:
        path: Path to schema file
        
    Returns:
        Schema dictionary
    """
    schema_path = Path(path)
    if not schema_path.exists():
        # Try relative to app directory
        schema_path = Path(__file__).parent.parent / "schemas" / "incident.v1.mvp.json"
    
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    return schema


def get_validator():
    """
    Get or create schema validator (singleton).
    
    Returns:
        Draft202012Validator instance
    """
    global _SCHEMA, _VALIDATOR
    
    if _VALIDATOR is None:
        _SCHEMA = load_schema()
        _VALIDATOR = Draft202012Validator(_SCHEMA)
    
    return _VALIDATOR


def validate_against_schema(obj: dict) -> None:
    """
    Validate object against JSON Schema.
    
    Args:
        obj: Dictionary to validate
        
    Raises:
        ValueError: If validation fails
    """
    validator = get_validator()
    errors = sorted(validator.iter_errors(obj), key=lambda e: e.path)
    
    if errors:
        msg = " | ".join([f"{'/'.join(map(str, e.path))}: {e.message}" for e in errors])
        raise ValueError(f"Schema validation failed: {msg}")

