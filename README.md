# VoiceOps

**Development prototype for voice-to-incident extraction.**

VoiceOps is a development prototype for converting voice transcripts into structured incident records. The LLM provider and downstream integrations are not implemented in the current main branch.

## 🎯 What VoiceOps Does

VoiceOps enables teams to report incidents via voice (phone, web, mobile) and automatically converts them into structured JSON incidents ready for integration with Jira, PagerDuty, and other incident management tools.

## 🚀 Quick Start



1. **Voice Input**: User calls or speaks incident details
2. **AI Processing**: VAPI agent processes voice → structured JSON
3. **Validation**: Strict schema validation ensures production-ready output
4. **Integration**: Webhook to Jira/PagerDuty with proper severity classification



See `/demo` folder for:
- `demo_incident.json` - Example output
- `demo_transcript_security.txt` - Security incident example
- `demo_transcript_outage.txt` - Outage incident example
- `demo_flow.md` - Complete demo walkthrough

## 🏗️ Architecture

- **Frontend**: Voice interface (web/mobile)
- **AI Agent**: VAPI-powered voice-to-JSON conversion
- **Validation**: JSON Schema validation (see `/schemas`)
- **Integration**: Webhook delivery to Jira/PagerDuty
- **Severity Logic**: Deterministic, auditable severity rules

See `/engineering` for detailed architecture.

## 🐰 CodeRabbit Integration

This project was developed with CodeRabbit AI code review, ensuring:
- Production-ready code quality
- Security best practices
- Comprehensive test coverage
- Clean PR titles and commit messages

### How CodeRabbit Improved This Code

CodeRabbit AI code review helped ensure production-ready code quality:

#### Security Improvements
- **PII Redaction**: CodeRabbit identified missing PII handling in `api/incident.py`
- **Input Validation**: Enhanced validation in `api/schema.py` to prevent injection
- **Error Handling**: Improved error messages to avoid information leakage
- **Logging Safety**: Identified risks of logging sensitive data

#### Code Quality
- **Type Safety**: Added type hints throughout
- **Error Handling**: Proper exception handling with clear messages
- **Code Organization**: Suggested better module structure (schema/parsing/scoring separation)

#### Testing
- **Table-Driven Tests**: CodeRabbit recommended table-driven test strategy
- **Edge Cases**: Identified missing test cases for boundary conditions
- **Schema Validation**: Comprehensive tests for all schema rules (enums, constraints, patterns)

#### Reliability
- **Idempotency**: Ensured `call_id` handling prevents duplicates
- **Fallback Logic**: Added fallback for invalid LLM output with repair prompts
- **Retry Strategy**: Improved webhook delivery retry logic
- **Failure Modes**: Identified VAPI/LLM failure points and suggested retries/backoff

#### Schema & Validation
- **Strict Enforcement**: Verified `additionalProperties=false` enforcement
- **Constraint Validation**: Tests for min/max lengths, patterns, ISO datetime
- **Enum Validation**: Comprehensive enum value checking

**Result**: Production-ready code from day one, catching issues that would have required extensive manual review.

See `/coderabbit` for:
- Review checklist
- Example PR titles
- Rabbit Hole narrative
- PR comment template for CodeRabbit

## 📁 Project Structure

```
VoiceOps/
├── api/               # Core API code
│   ├── incident.py    # Incident creation & processing
│   ├── scoring.py     # Confidence & severity calculation
│   ├── schema.py      # Schema validation
│   └── llm.py         # LLM integration
├── tests/             # Test files
├── schemas/           # JSON schemas for validation
│   └── incident.v1.json
├── prompts/           # LLM prompts
│   ├── incident_prompt.txt
│   ├── incident_schema_summary.txt
│   └── repair_prompt.txt
├── demo/              # ----
├── engineering/       # Technical documentation
├── coderabbit/        # CodeRabbit integration docs
├── legal/             # ----
├── security_compliance/ # Security & compliance docs
├── sales/             # --
├── post_pilot/        # Post-pilot materials
├── billing/           # -----
├── README.md          # This file
└── ARCHITECTURE.md    # Architecture documentation
```




## Reproducible local checks and current boundaries

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Use Python 3.12. CI runs the same tests. The incident API fails closed when no LLM provider is configured.
Only synthetic local demos should pass `allow_fallback=True` explicitly. The fallback is a rule-based demo,
not a substitute for a configured provider or verified incident triage.
UTC timestamps retain the requested IANA timezone label. Unknown impact defaults to sev3; security incidents
are escalated. Explicitly negated urgency does not override independent outage evidence.

PII filtering covers basic email, phone and labelled patient-name patterns before the provider call.
It is incomplete: do not use real patient data or claim HIPAA/GDPR/SOC2 compliance from these tests.
A production integration requires reviewed privacy controls, retention, access control, provider configuration,
authentication and integration tests. Existing marketing/compliance documents describe goals, not certification.
No project reuse license has been selected.
