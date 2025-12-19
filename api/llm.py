"""
VoiceOps LLM Integration

Handles LLM calls for transcript → JSON conversion.
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional

from .schema import validate_incident, load_schema


PROMPT_DIR = Path(__file__).parent.parent / "prompts"
SCHEMA_SUMMARY_PATH = PROMPT_DIR / "incident_schema_summary.txt"
INCIDENT_PROMPT_PATH = PROMPT_DIR / "incident_prompt.txt"
REPAIR_PROMPT_PATH = PROMPT_DIR / "repair_prompt.txt"


def load_prompt_template(path: Path) -> str:
    """Load prompt template from file."""
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
    
    # Replace placeholders
    prompt = prompt.replace("{{NOW_ISO}}", reported_at)
    prompt = prompt.replace("{{VAPI_CALL_ID}}", call_id)
    prompt = prompt.replace("{{TRANSCRIPT_TEXT}}", transcript)
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
    
    errors_text = "\n".join(f"- {e}" for e in errors)
    bad_json_text = json.dumps(bad_json, indent=2)
    
    prompt = prompt.replace("{{LIST_OF_ERRORS}}", errors_text)
    prompt = prompt.replace("{{BAD_JSON}}", bad_json_text)
    
    return prompt


def call_openai_api(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Call OpenAI API with prompt.
    
    Args:
        prompt: Prompt text
        model: Model name (default: gpt-4o-mini)
        
    Returns:
        LLM response text
        
    Raises:
        ValueError: If API call fails
    """
    try:
        from openai import OpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not set")
        
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts structured incident data from voice transcripts. Always return valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=2000
        )
        
        return response.choices[0].message.content.strip()
        
    except ImportError:
        raise NotImplementedError("OpenAI library not installed. Install with: pip install openai")
    except Exception as e:
        raise ValueError(f"OpenAI API error: {str(e)}")


def call_anthropic_api(prompt: str, model: str = "claude-3-haiku-20240307") -> str:
    """
    Call Anthropic API with prompt.
    
    Args:
        prompt: Prompt text
        model: Model name (default: claude-3-haiku-20240307)
        
    Returns:
        LLM response text
        
    Raises:
        ValueError: If API call fails
    """
    try:
        from anthropic import Anthropic
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")
        
        client = Anthropic(api_key=api_key)
        
        response = client.messages.create(
            model=model,
            max_tokens=2000,
            temperature=0.3,
            messages=[
                {"role": "user", "content": prompt}
            ],
            system="You are a helpful assistant that extracts structured incident data from voice transcripts. Always return valid JSON only."
        )
        
        return response.content[0].text.strip()
        
    except ImportError:
        raise NotImplementedError("Anthropic library not installed. Install with: pip install anthropic")
    except Exception as e:
        raise ValueError(f"Anthropic API error: {str(e)}")


def call_llm_for_incident(transcript: str, call_id: Optional[str] = None) -> Dict:
    """
    Call LLM to extract incident from transcript.
    
    Tries OpenAI first, then Anthropic, then raises NotImplementedError.
    
    Args:
        transcript: Raw transcript text
        call_id: Optional call identifier
        
    Returns:
        Validated incident JSON dict
        
    Raises:
        ValueError: If LLM output cannot be validated even after repair
        NotImplementedError: If no LLM API keys are configured
    """
    # Build prompt
    prompt = build_incident_prompt(transcript, call_id)
    
    # Try OpenAI first
    if os.getenv("OPENAI_API_KEY"):
        try:
            response_text = call_openai_api(prompt)
            # Extract JSON from response (might have markdown code blocks)
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            incident = json.loads(response_text)
            return incident
        except (ValueError, json.JSONDecodeError) as e:
            # If OpenAI fails, try Anthropic
            if os.getenv("ANTHROPIC_API_KEY"):
                try:
                    response_text = call_anthropic_api(prompt)
                    # Extract JSON from response
                    response_text = response_text.strip()
                    if response_text.startswith("```json"):
                        response_text = response_text[7:]
                    if response_text.startswith("```"):
                        response_text = response_text[3:]
                    if response_text.endswith("```"):
                        response_text = response_text[:-3]
                    response_text = response_text.strip()
                    
                    incident = json.loads(response_text)
                    return incident
                except (ValueError, json.JSONDecodeError):
                    raise ValueError(f"Both OpenAI and Anthropic failed. Last error: {str(e)}")
            else:
                raise ValueError(f"OpenAI failed and Anthropic not configured: {str(e)}")
    
    # Try Anthropic if OpenAI not configured
    elif os.getenv("ANTHROPIC_API_KEY"):
        try:
            response_text = call_anthropic_api(prompt)
            # Extract JSON from response
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            incident = json.loads(response_text)
            return incident
        except (ValueError, json.JSONDecodeError) as e:
            raise ValueError(f"Anthropic API error: {str(e)}")
    
    # No API keys configured
    raise NotImplementedError("No LLM API keys configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable.")


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
        # TODO: Call LLM with repair prompt
        # repaired = call_llm_for_repair(repair_prompt)
        # return validate_and_repair(repaired, max_repairs - 1)
    
    # If repair failed or not attempted, raise error
    raise ValueError(f"Invalid incident JSON: {'; '.join(errors)}")

