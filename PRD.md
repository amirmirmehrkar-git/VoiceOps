# Product Requirements Document (PRD)
## VoiceOps AI - Voice-First Incident Reporting Platform

**Version**: 1.0.0  
**Date**: 2025-01-27  
**Status**: Draft → Ready for Development

---

## 📋 Executive Summary

VoiceOps is a voice-first incident reporting platform that transforms spoken incident reports into structured, production-grade JSON incidents. The platform enables teams in high-pressure environments (hospitals, factories, DevOps teams) to report incidents via voice when typing is not feasible, automatically converting voice input into validated, actionable incident records.

**Core Value Proposition**: "Voice is the input. Production-grade incidents are the output."

---

## 🎯 Problem Statement

### Current Pain Points

1. **Manual Reporting is Slow**
   - Operators/nurses don't have time to fill out forms during incidents
   - Typing fails when time matters most
   - Critical incidents are reported late or incompletely

2. **Inconsistent Data Quality**
   - Free-text reports lack structure
   - Severity classification is inconsistent
   - Missing required information delays response

3. **Integration Challenges**
   - Incident data doesn't fit standard formats
   - Manual data entry into Jira/PagerDuty is error-prone
   - No automated severity classification

4. **PII and Compliance Risks**
   - Personal information may be included in reports
   - No automatic redaction
   - Compliance concerns (HIPAA, SOC2)

### Target Users

- **Primary**: Operators, nurses, technicians in high-pressure environments
- **Secondary**: DevOps teams, security teams, quality inspectors
- **Tertiary**: IT support, customer service escalation teams

---

## 💡 Solution Overview

VoiceOps provides a voice-first incident intake system that:

1. **Accepts Voice Input**: Users call or speak incident details
2. **Structures Data**: AI converts voice → structured JSON
3. **Validates Output**: Strict schema validation ensures quality
4. **Integrates Seamlessly**: Webhooks to Jira, PagerDuty, SIEM systems
5. **Protects Privacy**: Automatic PII redaction and compliance controls

---

## 🎯 Product Goals

### Primary Goals

1. **Reduce Time to Report**: From 5-10 minutes (typing) to 30-60 seconds (voice)
2. **Improve Data Quality**: 100% schema-valid incidents with required fields
3. **Enable Fast Response**: Automatic severity classification (sev1-sev4)
4. **Ensure Compliance**: PII redaction and audit trails

### Success Metrics

- **Adoption**: 80% of incidents reported via voice within 3 months
- **Quality**: 95%+ incidents pass schema validation on first attempt
- **Speed**: Average report time < 60 seconds
- **Accuracy**: 90%+ severity classification accuracy
- **Integration**: 100% successful webhook delivery to downstream systems

---

## 🚀 Core Features

### 1. Voice Intake (MVP)

**Description**: 4-question structured voice intake via VAPI

**Requirements**:
- VAPI integration for voice-to-text
- Exactly 4 questions asked in order:
  1. What happened? (What broke?)
  2. Which system/device? (Where?)
  3. When did it start? (Timeline)
  4. Impact level? (1-4 severity)
- Persian and English language support
- Call duration < 60 seconds

**Acceptance Criteria**:
- [ ] VAPI assistant asks exactly 4 questions
- [ ] Transcript captured successfully
- [ ] Call completes in < 60 seconds
- [ ] Supports Persian and English

---

### 2. AI-Powered Structuring (MVP)

**Description**: LLM converts transcript → structured JSON

**Requirements**:
- OpenAI GPT-4o or Anthropic Claude integration
- Schema-valid JSON output
- Fallback mechanism for invalid output
- Repair prompt for fixing invalid JSON

**Acceptance Criteria**:
- [ ] 90%+ of transcripts convert to valid JSON on first attempt
- [ ] Invalid JSON repaired automatically
- [ ] All required fields populated
- [ ] Safe defaults for unknown values

---

### 3. Schema Validation (MVP)

**Description**: Strict JSON Schema validation

**Requirements**:
- JSON Schema 2020-12 standard
- `additionalProperties: false` enforcement
- Required fields validation
- Enum value validation
- Pattern validation (IDs, tags, dates)

**Acceptance Criteria**:
- [ ] 100% of stored incidents pass schema validation
- [ ] Invalid incidents rejected with clear errors
- [ ] All enum values strictly enforced
- [ ] Pattern validation for IDs and tags

---

### 4. Severity Classification (MVP)

**Description**: Deterministic, rule-based severity scoring

**Requirements**:
- Rule-based (not AI guessing)
- sev1 (critical) → sev4 (minor)
- Auditable decision trail
- Keyword-based classification

**Rules**:
- **sev1**: "down", "outage", "500", "emergency", `services_down=true`
- **sev2**: Severe degradation, high user count (>100)
- **sev3**: Default for ambiguous cases
- **sev4**: Minor, cosmetic issues

**Acceptance Criteria**:
- [ ] Severity rules documented and auditable
- [ ] 90%+ classification accuracy
- [ ] All decisions logged with reasoning

---

### 5. PII Redaction (MVP)

**Description**: Automatic PII detection and redaction

**Requirements**:
- Detect: emails, phone numbers, names
- Redact: Replace with `[REDACTED]`
- Flag: Set `pii.contains_pii=true`
- Log: Audit trail of redaction

**Acceptance Criteria**:
- [ ] 100% of PII detected and redacted
- [ ] Redaction flags set correctly
- [ ] No PII in stored incidents
- [ ] Audit trail maintained

---

### 6. Webhook Integration (MVP)

**Description**: Send incidents to downstream systems

**Requirements**:
- Jira ticket creation
- PagerDuty incident creation
- Generic webhook support
- Retry logic for failed deliveries

**Acceptance Criteria**:
- [ ] Jira tickets created successfully
- [ ] PagerDuty incidents triggered
- [ ] Webhook retries on failure
- [ ] Delivery status tracked

---

### 7. Idempotency (MVP)

**Description**: Prevent duplicate incidents

**Requirements**:
- `call_id` field in schema
- Duplicate detection via `call_id`
- Return existing incident if duplicate

**Acceptance Criteria**:
- [ ] Duplicate calls detected
- [ ] Existing incident returned (not created)
- [ ] No duplicate incidents in system

---

## 📊 Technical Requirements

### Architecture

- **Backend**: FastAPI (Python)
- **Voice**: VAPI integration
- **AI**: OpenAI GPT-4o or Anthropic Claude
- **Validation**: JSON Schema 2020-12
- **Storage**: (Future) PostgreSQL or MongoDB
- **Deployment**: Docker, Daytona-compatible

### API Endpoints

1. `POST /api/v1/incidents` - Create incident from transcript
2. `POST /api/v1/vapi/webhook` - VAPI webhook handler
3. `POST /api/v1/incidents/validate` - Validate incident JSON
4. `GET /api/v1/incidents/{id}` - Get incident by ID
5. `GET /health` - Health check

### Data Schema

- **Schema File**: `schemas/incident.v1.json`
- **Version**: 1.0.0
- **Format**: JSON Schema 2020-12
- **Strictness**: `additionalProperties: false`

### Security Requirements

- **PII Redaction**: Automatic detection and redaction
- **Input Validation**: All inputs validated
- **Error Handling**: No sensitive data in error messages
- **Logging**: Safe logging (no PII in logs)
- **Compliance**: SOC2-lite, HIPAA-aligned

### Performance Requirements

- **Response Time**: < 5 seconds for incident creation
- **Voice Processing**: < 60 seconds per call
- **Webhook Delivery**: < 2 seconds to downstream systems
- **Availability**: 99.9% uptime

---

## 👥 User Stories

### Story 1: Hospital Nurse Reports Equipment Failure

**As a** hospital nurse  
**I want to** report equipment failure via voice call  
**So that** I can report incidents quickly without leaving the patient

**Acceptance**:
- Nurse calls VoiceOps
- Answers 4 questions
- Incident created in < 60 seconds
- Ticket automatically created in hospital system

---

### Story 2: DevOps Engineer Reports Production Outage

**As a** DevOps engineer  
**I want to** report production outage via voice  
**So that** I can trigger PagerDuty escalation immediately

**Acceptance**:
- Engineer calls VoiceOps
- Reports: "Checkout API returning 500s"
- Severity automatically classified as sev1
- PagerDuty incident created automatically

---

### Story 3: Quality Inspector Reports Manufacturing Defect

**As a** quality inspector  
**I want to** report defects via voice while inspecting  
**So that** I don't need to stop and type

**Acceptance**:
- Inspector calls VoiceOps
- Reports defect details
- Incident created with proper categorization
- ERP system updated automatically

---

## 🎨 User Experience

### Voice Flow

1. **User calls** VoiceOps number
2. **Assistant greets**: "سلام، من VoiceOps هستم. برای گزارش حادثه، لطفاً به ۴ سؤال من پاسخ دهید."
3. **Q1**: "چه اتفاقی افتاده یا چه چیزی خراب شده؟"
4. **Q2**: "کدام سیستم یا دستگاه درگیر است و کجا؟"
5. **Q3**: "این مشکل از چه زمانی شروع شده؟"
6. **Q4**: "اثر مشکل چقدر است؟ (1-4)"
7. **Confirmation**: "متشکرم. حادثه ثبت شد."

### Web Interface (Future)

- Dashboard for viewing incidents
- Manual incident creation form
- Integration configuration
- Analytics and reporting

---

## 🔄 Integration Requirements

### Phase 1 (MVP)

- **VAPI**: Voice input
- **Jira**: Ticket creation
- **PagerDuty**: Incident escalation
- **Generic Webhooks**: Custom integrations

### Phase 2 (Future)

- **ServiceNow**: IT service management
- **Slack**: Notifications
- **Email**: Incident notifications
- **SIEM**: Security incident logging

---

## 📈 Success Metrics

### Adoption Metrics

- **Daily Active Users**: Target 50+ users/day
- **Incidents per Day**: Target 100+ incidents/day
- **Voice vs Manual**: 80%+ via voice

### Quality Metrics

- **Schema Validation Rate**: 95%+ on first attempt
- **Severity Accuracy**: 90%+ correct classification
- **PII Detection Rate**: 100% of PII detected

### Performance Metrics

- **Average Call Duration**: < 60 seconds
- **Incident Creation Time**: < 5 seconds
- **Webhook Delivery Success**: 99%+

### Business Metrics

- **Time Saved**: 5-10 minutes per incident
- **Response Time Improvement**: 50% faster incident response
- **Data Quality Improvement**: 100% structured data

---

## 🚦 Release Plan

### Phase 1: MVP (Hackathon)

**Timeline**: 2-3 days

**Features**:
- [x] Voice intake via VAPI
- [x] AI-powered structuring
- [x] Schema validation
- [x] Severity classification
- [x] PII redaction
- [x] Webhook integration
- [x] Idempotency

**Deliverables**:
- Working API
- VAPI assistant
- Demo scenarios
- Documentation

---

### Phase 2: Production Hardening

**Timeline**: 2-4 weeks

**Features**:
- Database storage
- User authentication
- Web dashboard
- Advanced analytics
- Multi-language support

---

### Phase 3: Enterprise Features

**Timeline**: 1-2 months

**Features**:
- SSO integration
- Advanced compliance (HIPAA, SOC2)
- Custom workflows
- API rate limiting
- Multi-tenant support

---

## 🐛 Known Limitations (MVP)

1. **No Database**: Incidents stored in memory (for demo)
2. **Single Language**: Primary support for Persian
3. **No Authentication**: Open API (for demo)
4. **No Dashboard**: API-only (for demo)
5. **Limited Integrations**: Jira and PagerDuty only

---

## 🔒 Security & Compliance

### Security Requirements

- **PII Redaction**: Automatic and mandatory
- **Input Validation**: All inputs validated
- **Error Handling**: No sensitive data leakage
- **Logging**: Safe logging practices
- **API Security**: Rate limiting (future)

### Compliance Alignment

- **SOC2-lite**: Controls documented
- **HIPAA-aligned**: Data minimization
- **GDPR-ready**: PII handling
- **Audit Trail**: All actions logged

---

## 📚 Documentation Requirements

### Technical Documentation

- [x] API documentation (Swagger/OpenAPI)
- [x] Architecture documentation
- [x] Schema documentation
- [x] Integration guides

### User Documentation

- [ ] User guide
- [ ] Voice flow guide
- [ ] Troubleshooting guide
- [ ] FAQ

### Developer Documentation

- [x] Setup guide
- [x] Code structure
- [x] Testing guide
- [x] Deployment guide

---

## 🧪 Testing Requirements

### Unit Tests

- [x] Schema validation tests
- [x] Severity classification tests
- [x] PII redaction tests
- [ ] LLM integration tests

### Integration Tests

- [ ] VAPI webhook tests
- [ ] Jira integration tests
- [ ] PagerDuty integration tests
- [ ] End-to-end flow tests

### Table-Driven Tests

- [x] Multiple scenario tests
- [x] Edge case tests
- [x] Error handling tests

---

## 🎯 Success Criteria

### MVP Success

- [x] Voice intake working
- [x] AI structuring working
- [x] Schema validation working
- [x] Severity classification working
- [x] PII redaction working
- [x] Webhook integration working
- [x] Demo scenarios ready

### Production Readiness

- [ ] Database storage
- [ ] Authentication
- [ ] Error monitoring
- [ ] Performance monitoring
- [ ] Backup and recovery
- [ ] Documentation complete

---

## 📝 Appendices

### A. Schema Reference

See `schemas/incident.v1.json` for complete schema definition.

### B. API Reference

See `http://localhost:8000/docs` for Swagger UI documentation.

### C. Integration Examples

See `engineering/jira_webhook_payload.json` and `engineering/pagerduty_webhook_payload.json`.

### D. Demo Scenarios

See `demo/demo_scenarios.md` for complete demo scenarios.

---

## 🔄 Change Log

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-01-27 | Initial PRD created |

---

## ✅ Approval

**Product Owner**: [TBD]  
**Engineering Lead**: [TBD]  
**Date**: [TBD]

---

**Status**: ✅ Ready for Development  
**Next Steps**: Begin MVP implementation

