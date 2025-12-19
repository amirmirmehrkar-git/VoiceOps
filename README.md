# VoiceOps

**Voice is the input. Production-grade incidents are the output.**

VoiceOps is an enterprise-ready voice-first incident ingestion system that transforms spoken reports into structured, production-grade incident records.

## 🎯 What VoiceOps Does

VoiceOps enables teams to report incidents via voice (phone, web, mobile) and automatically converts them into structured JSON incidents ready for integration with Jira, PagerDuty, and other incident management tools.

## 🚀 Quick Start

### Demo Flow (90 seconds)

1. **Voice Input**: User calls or speaks incident details
2. **AI Processing**: VAPI agent processes voice → structured JSON
3. **Validation**: Strict schema validation ensures production-ready output
4. **Integration**: Webhook to Jira/PagerDuty with proper severity classification

### Offline Demo

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
├── demo/              # Demo materials and examples
├── engineering/       # Technical documentation
├── coderabbit/        # CodeRabbit integration docs
├── legal/             # Legal documents (export to PDF)
├── security_compliance/ # Security & compliance docs
├── sales/             # Sales materials & pricing
├── post_pilot/        # Post-pilot materials
├── billing/           # Billing templates
├── README.md          # This file
└── ARCHITECTURE.md    # Architecture documentation
```

## 🔐 Security & Compliance

- **SOC2-lite** controls documented
- **HIPAA-aligned** positioning
- **NIST-style** incident response mapping
- Security FAQ and vendor questionnaire available

See `/security_compliance` for details.

## ⚖️ Legal

All legal documents available in `/legal`:
- Pilot Terms (non-binding)
- Data Processing Addendum (DPA)
- Master Service Agreement (MSA)
- Order Form template

**Export to PDF before sending to buyers.**

## 💰 Pricing

- **Pilot**: Free (2-3 weeks)
- **Team**: $X/month
- **Regulated**: Custom pricing

See `/sales/pricing.md` for details.

## 📞 Contact

For pilots, enterprise deals, or questions:
- Email: [your-email]
- Demo: [demo-link]

## 🎯 Universal Tagline

**"Voice is the input. Production-grade incidents are the output."**

---

## 🚦 Status

✅ Hackathon-ready
✅ Pilot-ready
✅ Enterprise-ready
✅ Revenue-ready

