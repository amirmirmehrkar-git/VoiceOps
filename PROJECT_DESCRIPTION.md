# VoiceOps

**Amir Mirmehrkar**

**VoiceOps AI**

**Voice-First Incident Ingestion & Compliance Review for Production Services**

---

## Overview

VoiceOps is an enterprise-ready FastAPI service that transforms voice incident reports into structured, production-grade JSON incidents. It enables teams to report incidents via voice (phone, web, mobile) and automatically converts them into validated, schema-compliant incident records ready for integration with Jira, PagerDuty, and other incident management tools.

### Core Capabilities

- **Voice-First Input**: Accepts voice reports via VAPI (phone, web, mobile)
- **AI-Powered Structuring**: LLM converts voice transcripts into structured JSON incidents
- **Strict Schema Validation**: JSON Schema 2020-12 with `additionalProperties: false` for production safety
- **Deterministic Severity**: Rule-based severity classification (sev1-sev4) - auditable and testable
- **PII Safety**: Real-time PII (Personally Identifiable Information) detection and redaction for GDPR/HIPAA compliance
- **Secure Development**: Integration with CodeRabbit for AI-assisted code and schema reviews

---

## The Problem

Modern engineering teams struggle with:

1. **Time Pressure**: When incidents occur, operators don't have time to fill out forms
2. **Inconsistency**: Subjective severity scoring during high-stress moments leads to misclassification
3. **Compliance Risks**: Unintentional PII exposure in logs and error messages violates GDPR/HIPAA
4. **Slow Triage**: Manual review cycles delay critical fixes and increase MTTR (Mean Time To Repair)
5. **Unstructured Data**: Voice reports are lost or poorly documented, making post-incident analysis difficult

---

## The Solution

VoiceOps introduces a voice-first incident ingestion layer that acts as a bridge between voice reports and incident management systems:

1. **Voice Ingestion**: Accepts voice input via VAPI (phone calls, web interface, mobile app)
2. **AI Structuring**: VAPI agent asks exactly 4 questions and outputs schema-valid JSON directly
3. **Validation**: Strict JSON Schema validation ensures production-ready output
4. **Severity Scoring**: Deterministic, rule-based severity classification (not AI guessing)
5. **PII Redaction**: Automatic detection and redaction of PII before storage
6. **Integration Ready**: Webhook delivery to Jira, PagerDuty, SIEM systems
7. **Feedback Loop**: Uses CodeRabbit to validate schema changes and generate test suggestions directly on Pull Requests

---

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, Pydantic
- **Voice Processing**: VAPI (Voice API) for voice-to-transcript conversion
- **AI/LLM**: OpenAI / Anthropic for transcript-to-JSON structuring
- **Validation**: JSON Schema 2020-12 with jsonschema library
- **AI/LLM Tools**: CodeRabbit (Security & PR Review), Windsurf/Cursor (Agentic Development)
- **Testing**: Pytest (Unit testing & Schema validation with table-driven tests)

---

## Data Interface

### Example Input (POST /api/v1/incidents)

Voice transcript from VAPI webhook:

```json
{
  "type": "end-of-call",
  "call": {
    "id": "call_abc123",
    "transcript": "Production API is completely down. All services offline. Started at 6 PM. About 1200 users affected. This is critical."
  }
}
```

### Example Output

```json
{
  "schema_version": "1.0.0",
  "incident_id": "f9847182-1827-40c1-988f-088f329c395b",
  "title": "Production API is completely down. All services offline.",
  "summary": "Production API is completely down. All services offline. Started at 6 PM. About 1200 users affected. This is critical.",
  "category": "service_outage",
  "severity": "sev1",
  "confidence": 0.85,
  "status": "new",
  "impact": {
    "services_down": true,
    "users_affected_estimate": 1200
  },
  "systems": [
    {
      "name": "production-api",
      "environment": "production"
    }
  ],
  "pii": {
    "contains_pii": false,
    "redaction_applied": false
  },
  "source": {
    "channel": "voice",
    "vendor": "vapi",
    "call_id": "call_abc123"
  },
  "detected_at": "2025-01-12T18:00:00Z",
  "reported_at": "2025-01-12T18:05:00Z"
}
```

---

## AI Usage (Beyond the Hype)

This project focuses on **Agentic Workflows** rather than simple API calls:

### CodeRabbit Integration
We utilize CodeRabbit to perform deep-context reviews of incident-related PRs, identifying:
- Security vulnerabilities (PII exposure, injection risks)
- Edge cases in severity classification
- Schema validation gaps
- Test coverage improvements

### Windsurf / Cursor
The core logic of this service was built using prompt-driven development, allowing for:
- Rapid iteration during the hackathon
- Refactoring with AI assistance
- Schema-first design validation

### Human-in-the-Loop
All AI suggestions are treated as "proposals"—they require explicit engineer review before being committed. This ensures:
- Production safety
- Compliance adherence
- Auditability

---

## Key Concepts

### Severity Levels
- **sev1 (Critical)**: Services down, security breach, patient safety risk
- **sev2 (High)**: Severe degradation, high user impact (>100 users)
- **sev3 (Medium)**: Moderate impact, limited scope
- **sev4 (Low)**: Minor issues, cosmetic problems

### Category Types
- `service_outage`: Complete service failure
- `security_incident`: Security breach, unauthorized access
- `performance_degradation`: Slow response, timeouts
- `data_issue`: Data corruption, loss, or inconsistency
- `patient_safety`: Healthcare-specific safety incidents
- `other`: Unclassified incidents

### PII Detection
Scans for and redacts:
- Email addresses
- Phone numbers (US, International, Iranian formats)
- Credit card numbers
- Social Security Numbers (SSN)
- IP addresses (IPv4, IPv6)
- Patient IDs
- Names (heuristic-based)

### Confidence Score
0.0 to 1.0 based on:
- Completeness of extracted data
- Presence of required fields
- PII detection (reduces confidence)
- System identification accuracy

---

## Hackathon Goals & Future

### Completed ✅
- [x] Voice-first incident ingestion with VAPI
- [x] LLM-powered transcript-to-JSON conversion
- [x] Strict JSON Schema validation
- [x] Deterministic severity classification
- [x] PII detection and redaction
- [x] CodeRabbit integration for PR reviews
- [x] Table-driven tests for validation
- [x] Production-ready error handling

### Future Roadmap 🚀
- [ ] Real-time VAPI webhook integration
- [ ] Jira/PagerDuty webhook delivery
- [ ] Historical trend analysis using Vector Databases
- [ ] Multi-language support
- [ ] Voice quality scoring
- [ ] Compliance reporting dashboard
- [ ] Slack integration for notifications

---

## How to Run

### Prerequisites
- Python 3.11+
- VAPI API key (for voice processing)
- OpenAI or Anthropic API key (for LLM structuring)

### Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   Create `.env.local`:
   ```bash
   VAPI_API_KEY=your_vapi_key
   VAPI_PUBLIC_KEY=your_vapi_public_key
   OPENAI_API_KEY=your_openai_key  # Optional
   ANTHROPIC_API_KEY=your_anthropic_key  # Optional
   ```

3. **Launch service**:
   ```bash
   uvicorn main:app --reload
   ```

4. **Explore API**:
   Visit http://localhost:8000/docs for interactive API documentation

### Testing

Run table-driven tests:
```bash
python -m pytest tests/test_incident_table.py -v
```

### Demo

See `/demo` folder for:
- Example incident JSON outputs
- Sample voice transcripts
- Demo flow walkthrough

---

## Project Structure

```
VoiceOps/
├── api/                    # Core API code
│   ├── incident.py        # Incident creation & processing
│   ├── scoring.py         # Confidence & severity calculation
│   ├── schema.py          # Schema validation
│   ├── llm.py             # LLM integration
│   └── vapi_webhook.py    # VAPI webhook handler
├── tests/                  # Test files
│   └── test_incident_table.py  # Table-driven tests
├── schemas/                # JSON schemas
│   └── incident.v1.json   # Strict incident schema
├── prompts/                # LLM prompts
│   ├── incident_prompt.txt
│   └── repair_prompt.txt
├── demo/                   # Demo materials
├── engineering/            # Technical documentation
├── coderabbit/             # CodeRabbit integration docs
└── main.py                 # FastAPI application entry point
```

---

**Built for AI Hackathon SFxHamburg** 

With ❤️ using AI-assisted development (CodeRabbit, Windsurf, Cursor, VAPI)

