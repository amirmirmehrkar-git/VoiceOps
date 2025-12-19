# VoiceOps - Code Implementation Guide

**Complete guide for implementing the codebase**

---

## 📁 Repository Structure

```
VoiceOps/
├── api/                    # Core API code
│   ├── incident.py        # Incident creation & processing
│   ├── scoring.py         # Confidence & severity calculation
│   ├── schema.py          # Schema validation (JSON Schema 2020-12)
│   └── llm.py             # LLM integration
├── tests/                 # Test files
│   └── test_incident_table.py  # Table-driven tests
├── schemas/               # JSON schemas
│   └── incident.v1.json  # Strict schema (additionalProperties=false)
├── prompts/               # LLM prompts
│   ├── incident_prompt.txt
│   ├── incident_schema_summary.txt
│   └── repair_prompt.txt
├── demo/                  # Demo materials
│   ├── demo_scenarios.md
│   ├── demo_scenario_1_outage.json
│   ├── demo_scenario_2_ambiguous.json
│   ├── demo_scenario_3_pii.json
│   └── demo_scenario_4_security.json
├── engineering/           # Technical docs
│   └── vapi_agent_prompt_4questions.txt
├── README.md
└── ARCHITECTURE.md
```

---

## 🔑 Key Implementation Details

### 1. Schema Validation Strategy

**File**: `api/schema.py`

- **Load schema from file**: `schemas/incident.v1.json`
- **Use JSON Schema 2020-12**: `Draft202012Validator`
- **Strict validation**: `additionalProperties=false` enforced
- **Error handling**: Returns list of errors, not just boolean

**Key Functions**:
```python
load_schema() -> Dict
validate_incident(incident: Dict) -> List[str]  # Returns errors
validate_incident_strict(incident: Dict) -> bool  # Raises on error
```

---

### 2. LLM Prompt Strategy

**Files**: `prompts/incident_schema_summary.txt`, `prompts/incident_prompt.txt`

**Approach**:
- **Don't paste full schema** in prompt (too long)
- **Use schema summary** with key constraints only
- **Validate output** against full schema file
- **Repair if invalid** using repair prompt

**Flow**:
1. Build prompt with schema summary
2. Call LLM
3. Validate against full schema
4. If invalid → repair prompt → validate again
5. If still invalid → fallback to defaults

---

### 3. Severity Classification

**File**: `api/scoring.py`

**Rule-based (not AI)**:
```python
if services_down or critical_keywords:
    return "sev1"
elif major_keywords or users > 100:
    return "sev2"
elif minor_keywords:
    return "sev4"
else:
    return "sev3"  # default
```

**Critical Keywords**: down, outage, cannot, 500, emergency, patient at risk, fire

**Explainable**: Judges can see exactly why severity was chosen

---

### 4. PII Redaction

**File**: `api/incident.py`

**Process**:
1. Detect PII in transcript (names, phones, emails, patient IDs)
2. Redact in summary/description → "[REDACTED]"
3. Set flags: `pii.contains_pii=true`, `pii.redaction_applied=true`

**TODO**: Implement actual PII detection (CodeRabbit will help)

---

### 5. Idempotency

**Via `call_id`**:
- Extract `call_id` from VAPI
- Check if incident with same `call_id` exists
- If exists → return existing incident
- If not → create new

**Prevents**: Duplicate incidents from retries

---

## 🧪 Testing Strategy

### Table-Driven Tests

**File**: `tests/test_incident_table.py`

**5 Required Scenarios**:
1. ✅ Clear sev1 outage
2. ✅ Ambiguous → defaults
3. ✅ Contains PII → redaction
4. ✅ security_incident
5. ✅ Missing system/location → fallback

**Plus**:
- Invalid tags (should fail)
- Invalid enum (should fail)

---

## 🐰 CodeRabbit Integration

### PR Workflow

1. **PR #1**: Initial code with schema
   - Title: "Production-grade Incident schema validation & safety baseline"
   - Wait for CodeRabbit review

2. **PR #2**: Apply CodeRabbit suggestions
   - Title: **"Apply CodeRabbit security & reliability recommendations"**
   - Include PR comment from `coderabbit/PR_COMMENT_FOR_CODERABBIT.md`
   - Commit messages mention CodeRabbit
   - Update README

3. **PR #3**: Voice intake flow (optional)
   - Title: "Add voice-first intake flow with deterministic severity mapping"

### CodeRabbit Questions (PR Comment)

See: `coderabbit/PR_COMMENT_FOR_CODERABBIT.md`

**Key Areas**:
- Security & PII
- Reliability & Failure Modes
- Schema & Validation
- Tests
- Code Quality

---

## 📝 Implementation Checklist

### Core API
- [x] `api/schema.py` - Schema validation
- [x] `api/scoring.py` - Severity classification
- [x] `api/incident.py` - Incident creation
- [x] `api/llm.py` - LLM integration

### Prompts
- [x] `prompts/incident_schema_summary.txt` - Schema summary
- [x] `prompts/incident_prompt.txt` - Main prompt
- [x] `prompts/repair_prompt.txt` - Repair prompt
- [x] `engineering/vapi_agent_prompt_4questions.txt` - VAPI agent

### Tests
- [x] `tests/test_incident_table.py` - Table-driven tests

### Demo Materials
- [x] `demo/demo_scenarios.md` - All scenarios
- [x] `demo/demo_scenario_*.json` - Valid JSON examples
- [x] `demo/demo_transcript_*.txt` - Transcript examples

### Documentation
- [x] `README.md` - Updated with CodeRabbit section
- [x] `ARCHITECTURE.md` - Architecture overview
- [x] `coderabbit/PR_TITLES_AND_COMMITS.md` - PR templates

---

## 🚀 Next Steps

1. **Implement LLM API integration** in `api/llm.py`
2. **Implement PII detection** in `api/incident.py`
3. **Add idempotency check** in `api/incident.py`
4. **Run tests** to verify everything works
5. **Create PR #1** and wait for CodeRabbit
6. **Apply CodeRabbit suggestions** in PR #2

---

## 📊 Demo Scenarios Ready

| Scenario | Transcript | JSON | PII | Status |
|----------|-----------|------|-----|--------|
| Outage | ✅ | ✅ | No | Ready |
| Ambiguous | ✅ | ✅ | No | Ready |
| PII | ✅ | ✅ | Yes | Ready |
| Security | ✅ | ✅ | No | Ready |

---

**Last Updated**: 2025-01-27  
**Status**: ✅ **Code structure ready for implementation**

