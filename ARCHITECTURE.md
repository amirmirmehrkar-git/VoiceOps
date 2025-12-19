# VoiceOps Architecture

**Voice is the input. Production-grade incidents are the output.**

---

## System Overview

VoiceOps transforms voice incident reports into structured, production-ready JSON incidents.

```
┌─────────────┐
│ Voice Input │ (Phone/Web/Mobile via VAPI)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ VAPI Agent  │ (Voice → Transcript)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ LLM Parser  │ (Transcript → Structured Data)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Validator   │ (Schema + Business Logic)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Webhook     │ (Jira/PagerDuty/SIEM)
└─────────────┘
```

---

## Components

### `/api/` - Core API

- **`incident.py`**: Incident creation and processing
- **`scoring.py`**: Confidence calculation and severity classification
- **`schema.py`**: JSON Schema validation

### `/schemas/` - Data Schemas

- **`incident.v1.json`**: Strict JSON Schema for incidents (JSON Schema 2020-12)

### `/tests/` - Tests

- Table-driven tests for validation
- Severity classification tests
- Schema validation tests

---

## Key Design Principles

### 1. Schema-First
- Strict JSON Schema with `additionalProperties: false`
- All validation happens before storage
- Forward-compatible versioning

### 2. Deterministic Severity
- Rules-based classification (not AI guessing)
- Auditable and testable
- Conservative escalation

### 3. PII Safety
- Detection and redaction at intake
- No raw transcripts stored long-term
- Audit trail for compliance

### 4. Idempotency
- `call_id` prevents duplicate incidents
- Safe retries and webhook delivery

---

## Data Flow

1. **Voice Input** → VAPI processes audio
2. **Transcript** → LLM extracts structured data (using prompt from `engineering/llm_incident_prompt.md`)
3. **Validation** → Schema validation + business rules
4. **Storage** → Validated incident stored
5. **Delivery** → Webhooks to Jira/PagerDuty
6. **Confirmation** → Status update to user

---

## Security

- All voice data encrypted in transit (TLS 1.3)
- Transcripts encrypted at rest (AES-256)
- PII redaction for compliance
- Audit logging for all operations

---

## Scalability

- Horizontal scaling for API
- Queue-based webhook delivery
- Stateless design
- Auto-scaling based on load

---

## Technology Stack

- **Language**: Python
- **Validation**: jsonschema library
- **Voice Processing**: VAPI
- **LLM**: For transcript → JSON conversion
- **Storage**: PostgreSQL (for incident records)
- **Queue**: Redis (for webhook delivery)

---

## How CodeRabbit Improved This Code

CodeRabbit AI code review helped ensure production-ready code quality:

### Security Improvements
- **PII Redaction**: CodeRabbit identified missing PII handling in `incident.py`
- **Input Validation**: Enhanced validation in `schema.py` to prevent injection
- **Error Handling**: Improved error messages to avoid information leakage

### Code Quality
- **Type Safety**: Added type hints throughout
- **Error Handling**: Proper exception handling with clear messages
- **Code Organization**: Suggested better module structure

### Testing
- **Table-Driven Tests**: CodeRabbit recommended table-driven test strategy
- **Edge Cases**: Identified missing test cases for boundary conditions
- **Schema Validation**: Comprehensive tests for all schema rules

### Reliability
- **Idempotency**: Ensured `call_id` handling prevents duplicates
- **Fallback Logic**: Added fallback for invalid LLM output
- **Retry Strategy**: Improved webhook delivery retry logic

**Result**: Production-ready code from day one, catching issues that would have required extensive manual review.

---

**Last Updated**: 2025-01-27

