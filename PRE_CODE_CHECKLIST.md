# ✅ Pre-Code Checklist - VoiceOps

**Status**: Ready for code implementation

---

## 📋 Checklist Before Writing Code

### ✅ Documentation Complete
- [x] Demo Repository Checklist updated (`demo/demo_repo_checklist.md`)
- [x] Pilot Terms updated (`legal/pilot_terms.md`)
- [x] Case Study Template updated (`post_pilot/case_study_template.md`)
- [x] Schema updated with `additionalProperties: false` and `call_id`

### 📁 Required File Structure

```
VoiceOps/
├── schemas/
│   └── incident.v1.json ✅ (updated with additionalProperties: false, call_id)
├── src/                    ⚠️ NEEDS CREATION
│   ├── intake.py          ⚠️ NEEDS CREATION
│   ├── severity.py        ⚠️ NEEDS CREATION
│   └── validate.py        ⚠️ NEEDS CREATION
├── tests/                  ⚠️ NEEDS CREATION
│   └── test_incident_table.py ⚠️ NEEDS CREATION
└── README.md              ✅ (exists)
```

---

## 🔒 Must-Have Features to Implement

### 1. `/src/intake.py`
**Required features**:
- [ ] Voice input processing
- [ ] PII redaction logic
- [ ] Idempotency via `call_id`
- [ ] Fallback for invalid LLM output
- [ ] Integration with VAPI

### 2. `/src/severity.py`
**Required features**:
- [ ] Deterministic severity rules (sev1–sev4)
- [ ] No AI/LLM decides severity - rules do
- [ ] Auditable severity classification
- [ ] Priority mapping (P0, P1, P2, P3)

### 3. `/src/validate.py`
**Required features**:
- [ ] Strict JSON Schema validation
- [ ] Validation before storage
- [ ] Clear error messages
- [ ] Reject invalid data

### 4. `/tests/test_incident_table.py`
**Required test cases**:
- [ ] sev1 outage (Critical severity)
- [ ] ambiguous defaults
- [ ] PII redaction
- [ ] security_incident
- [ ] missing system/location
- [ ] One failing test for invalid tags
- [ ] One failing test for invalid enum

---

## 🐰 CodeRabbit Integration

### PR Requirements
- [ ] Create PR titled: **"Apply CodeRabbit security & reliability recommendations"**
- [ ] Include CodeRabbit comments in PR
- [ ] Show CodeRabbit suggestions applied

### Commit Requirements
- [ ] Commit: `fix(security): redact PII as suggested by CodeRabbit`
- [ ] Commit: `test: add table-driven tests (CodeRabbit)`

---

## 🎬 Demo Backup Materials

### Already Available ✅
- [x] `demo/demo_incident.json` (schema-valid)
- [x] `demo/demo_transcript_security.txt`
- [x] `demo/demo_transcript_outage.txt`
- [x] `demo/demo_flow.md`

### Need to Create ⚠️
- [ ] `curl` command ready for API testing
- [ ] Screenshot of CodeRabbit PR (offline backup)

---

## 📝 Next Steps

1. **Create `/src/` folder** and implement:
   - `intake.py` - Voice intake with PII redaction
   - `severity.py` - Deterministic severity rules
   - `validate.py` - Schema validation

2. **Create `/tests/` folder** and implement:
   - `test_incident_table.py` - Table-driven tests

3. **Set up CodeRabbit**:
   - Create PR with CodeRabbit integration
   - Apply CodeRabbit recommendations
   - Take screenshot for demo backup

4. **Test everything**:
   - Run all tests
   - Verify schema validation
   - Test PII redaction
   - Test idempotency

---

## ✅ Ready to Code

All documentation is complete. You can now proceed with code implementation.

**Last Updated**: 2025-01-27

