"""
VoiceOps LLM Integration

Handles LLM calls for transcript → JSON conversion.
Supports OpenAI and Anthropic.
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv

from .schema import validate_incident, load_schema

load_dotenv()

PROMPT_DIR = Path(__file__).parent.parent / "prompts"
SCHEMA_SUMMARY_PATH = PROMPT_DIR / "incident_schema_summary.txt"
INCIDENT_PROMPT_PATH = PROMPT_DIR / "incident_prompt.txt"
REPAIR_PROMPT_PATH = PROMPT_DIR / "repair_prompt.txt"

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # "openai" or "anthropic"
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")  # or "claude-3-opus-20240229"


def load_prompt_template(path: Path) -> str:
    """Load prompt template from file."""
    if not path.exists():
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def build_incident_prompt(
    transcript: str,
    call_id: Optional[str] = None,
    timezone: str = "Europe/Berlin",
    reported_at: Optional[str] = None
) -> str:
    """
    Build the LLM prompt for incident extraction.
    
    Args:
        transcript: Raw transcript text
        call_id: Optional call identifier
        timezone: IANA timezone string
        reported_at: ISO-8601 timestamp (uses current time if None)
        
    Returns:
        Complete prompt string
    """
    from datetime import datetime, timezone as tz
    
    if reported_at is None:
        reported_at = datetime.now(tz.utc).isoformat()
    
    if call_id is None:
        from uuid import uuid4
        call_id = f"call_{uuid4().hex[:8]}"
    
    # Load schema summary
    schema_summary = load_prompt_template(SCHEMA_SUMMARY_PATH)
    
    # Load base prompt
    prompt = load_prompt_template(INCIDENT_PROMPT_PATH)
    
    if not prompt:
        # Fallback prompt if file doesn't exist
        prompt = f"""You are an incident-structuring engine. Convert this transcript into a STRICT JSON object that validates against incident.v1.json.

Rules:
- Output MUST be valid JSON only (no markdown, no commentary).
- Follow the schema exactly: required fields must be present; no extra fields.
- If a value is unknown, use safe defaults:
  - category: "other"
  - severity: "sev3"
  - status: "new"
  - location.site: "unknown"
  - systems: [{{"name":"unknown","environment":"unknown"}}]
  - confidence: between 0.5 and 0.9

Schema Summary:
{schema_summary}

Transcript:
{transcript}

Output valid JSON only:"""
    
    # Replace placeholders
    prompt = prompt.replace("{{NOW_ISO}}", reported_at)
    prompt = prompt.replace("{{VAPI_CALL_ID}}", call_id)
    prompt = prompt.replace("{{TRANSCRIPT_TEXT}}", transcript)
    if "<PASTE incident_schema_summary.txt HERE>" in prompt:
        prompt = prompt.replace("<PASTE incident_schema_summary.txt HERE>", schema_summary)
    
    return prompt


def build_repair_prompt(bad_json: Dict, errors: list[str]) -> str:
    """
    Build repair prompt for invalid JSON.
    
    Args:
        bad_json: Invalid JSON dict
        errors: List of validation error messages
        
    Returns:
        Repair prompt string
    """
    prompt = load_prompt_template(REPAIR_PROMPT_PATH)
    
    if not prompt:
        prompt = """Fix this invalid JSON to match the incident.v1.json schema.

Errors:
{{LIST_OF_ERRORS}}

Invalid JSON:
{{BAD_JSON}}

Output ONLY the corrected JSON (no markdown, no explanation):"""
    
    errors_text = "\n".join(f"- {e}" for e in errors)
    bad_json_text = json.dumps(bad_json, indent=2)
    
    prompt = prompt.replace("{{LIST_OF_ERRORS}}", errors_text)
    prompt = prompt.replace("{{BAD_JSON}}", bad_json_text)
    
    return prompt


def call_openai(prompt: str, model: str = "gpt-4o") -> str:
    """Call OpenAI API."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a JSON output generator. Always output valid JSON only, no markdown, no explanation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise ValueError(f"OpenAI API error: {str(e)}")


def call_anthropic(prompt: str, model: str = "claude-3-opus-20240229") -> str:
    """Call Anthropic API."""
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=ANTHROPIC_API_KEY)
        
        response = client.messages.create(
            model=model,
            max_tokens=2000,
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text.strip()
    except Exception as e:
        raise ValueError(f"Anthropic API error: {str(e)}")


def call_llm_for_incident(transcript: str, call_id: Optional[str] = None) -> Dict:
    """
    Call LLM to extract incident from transcript.
    
    Args:
        transcript: Raw transcript text
        call_id: Optional call identifier
        
    Returns:
        Validated incident JSON dict
        
    Raises:
        ValueError: If LLM output cannot be validated even after repair
    """
    # Build prompt
    prompt = build_incident_prompt(transcript, call_id)
    
    # Call LLM
    if LLM_PROVIDER == "anthropic" and ANTHROPIC_API_KEY:
        response_text = call_anthropic(prompt, LLM_MODEL)
    elif OPENAI_API_KEY:
        response_text = call_openai(prompt, LLM_MODEL)
    else:
        raise ValueError("No LLM API key configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY")
    
    # Parse JSON (remove markdown code blocks if present)
    response_text = response_text.strip()
    if response_text.startswith("```"):
        # Remove markdown code blocks
        lines = response_text.split("\n")
        response_text = "\n".join(lines[1:-1]) if lines[-1].startswith("```") else "\n".join(lines[1:])
    
    try:
        incident = json.loads(response_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {str(e)}")
    
    return incident


def validate_and_repair(incident: Dict, max_repairs: int = 1) -> Dict:
    """
    Validate incident and attempt repair if invalid.
    
    Args:
        incident: Incident JSON dict to validate
        max_repairs: Maximum number of repair attempts
        
    Returns:
        Validated incident JSON dict
        
    Raises:
        ValueError: If incident cannot be validated after repairs
    """
    errors = validate_incident(incident)
    
    if not errors:
        return incident
    
    # Attempt repair
    if max_repairs > 0:
        repair_prompt = build_repair_prompt(incident, errors)
        
        try:
            if LLM_PROVIDER == "anthropic" and ANTHROPIC_API_KEY:
                response_text = call_anthropic(repair_prompt, LLM_MODEL)
            elif OPENAI_API_KEY:
                response_text = call_openai(repair_prompt, LLM_MODEL)
            else:
                raise ValueError("No LLM API key for repair")
            
            # Parse JSON
            response_text = response_text.strip()
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(lines[1:-1]) if lines[-1].startswith("```") else "\n".join(lines[1:])
            
            repaired = json.loads(response_text)
            return validate_and_repair(repaired, max_repairs - 1)
        except Exception as e:
            pass  # Fall through to error
    
    # If repair failed or not attempted, raise error
    raise ValueError(f"Invalid incident JSON: {'; '.join(errors)}")
