
SOC2 Controls Overview

Security:
- Input validation via strict JSON Schema
- Access-controlled storage

Confidentiality:
- PII redaction at intake
- No raw transcripts in logs

Availability:
- Retry & backoff for VAPI/LLM
- Deterministic severity routing

Processing Integrity:
- additionalProperties=false
- Required fields enforced
