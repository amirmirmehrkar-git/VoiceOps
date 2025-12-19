# Demo Repository Checklist (Judge- & Pilot-Ready)

Use this checklist before pushing your final repo.

## 📁 Repo Structure

```
/schemas
  incident.v1.json

/src
  intake.py
  severity.py
  validate.py

/tests
  test_incident_table.py

/README.md
```

### ✅ Structure Checklist
- [ ] `/schemas/incident.v1.json` exists
- [ ] `/src/intake.py` exists
- [ ] `/src/severity.py` exists
- [ ] `/src/validate.py` exists
- [ ] `/tests/test_incident_table.py` exists
- [ ] `/README.md` exists and is complete

---

## 🔒 Must-Haves (Judges Look for These)

### ✅ Strict JSON Schema
- [ ] Schema has `additionalProperties: false`
- [ ] All required fields defined
- [ ] Enum values strictly enforced
- [ ] Pattern validation for IDs

**File**: `/schemas/incident.v1.json`

### ✅ Schema Validation
- [ ] Validation enforced before storage
- [ ] Invalid data rejected with clear errors
- [ ] Validation happens in `validate.py`

**File**: `/src/validate.py`

### ✅ Deterministic Severity Rules
- [ ] Severity rules are deterministic (sev1–sev4)
- [ ] Rules are auditable and documented
- [ ] No AI/LLM decides severity - rules do

**File**: `/src/severity.py`, `/engineering/severity_rules.md`

### ✅ PII Redaction Logic
- [ ] PII redaction implemented
- [ ] Redaction happens at intake
- [ ] Test cases for PII redaction

**File**: `/src/intake.py`

### ✅ Idempotency via call_id
- [ ] `call_id` field in schema
- [ ] Duplicate calls handled via `call_id`
- [ ] Idempotency logic tested

**File**: `/src/intake.py`

### ✅ Fallback for Invalid LLM Output
- [ ] Fallback mechanism implemented
- [ ] Invalid JSON handled gracefully
- [ ] Error recovery tested

**File**: `/src/intake.py`, `/src/validate.py`

---

## 🐰 CodeRabbit Proof

### ✅ PR Title
- [ ] At least one PR titled: **"Apply CodeRabbit security & reliability recommendations"**
- [ ] CodeRabbit comment visible in PR
- [ ] PR shows CodeRabbit suggestions applied

**Reference**: See `/coderabbit/example_pr_titles.md`

### ✅ Commit Messages
- [ ] One commit that explicitly references CodeRabbit:

```
fix(security): redact PII as suggested by CodeRabbit
```

```
test: add table-driven tests (CodeRabbit)
```

**Reference**: See `/coderabbit/example_pr_titles.md`

---

## 🧪 Tests (Minimal but Strong)

### ✅ Table-Driven Test Coverage

**File**: `/tests/test_incident_table.py`

Must cover:
- [ ] **sev1 outage** - Critical severity classification
- [ ] **ambiguous defaults** - Default values when ambiguous
- [ ] **PII redaction** - PII detection and redaction
- [ ] **security_incident** - Security category handling
- [ ] **missing system/location** - Handling missing fields
- [ ] **One failing test** for invalid tags / invalid enum

**Reference**: See `/coderabbit/table_driven_test_strategy.md`

### Test Structure Example:
```python
test_cases = [
    {
        "name": "sev1 outage",
        "input": {...},
        "expected": {"severity": "CRITICAL", ...}
    },
    {
        "name": "PII redaction",
        "input": {"description": "User email: john@example.com"},
        "expected": {"description": "User email: [REDACTED]"}
    },
    # ... more test cases
]
```

---

## 🎬 Demo Backup

### ✅ Offline Demo Materials
- [ ] `demo_incident.json` (schema-valid) exists
- [ ] `curl` command ready for API testing
- [ ] Screenshot of CodeRabbit PR (offline backup)
- [ ] Demo transcripts available (`demo_transcript_security.txt`, `demo_transcript_outage.txt`)

**Location**: `/demo/` folder

### ✅ curl Command Example
```bash
curl -X POST https://api.voiceops.com/v1/incidents \
  -H "Content-Type: application/json" \
  -d @demo/demo_incident.json
```

---

## 📋 Final Pre-Push Checklist

### Code Quality
- [ ] All tests pass
- [ ] No linter errors
- [ ] Code formatted
- [ ] Comments added where needed

### Documentation
- [ ] README.md complete
- [ ] CodeRabbit section in README
- [ ] Architecture documented
- [ ] API examples provided

### Security
- [ ] No secrets in code
- [ ] PII redaction tested
- [ ] Input validation tested
- [ ] Error handling secure

### Demo Ready
- [ ] Demo flow tested
- [ ] Backup materials ready
- [ ] Screenshots prepared
- [ ] curl commands tested

---

## ✅ Status

**Ready for**: 
- ✅ Hackathon judges
- ✅ Pilot deployments
- ✅ Enterprise demos

**Last Updated**: 2025-01-27

