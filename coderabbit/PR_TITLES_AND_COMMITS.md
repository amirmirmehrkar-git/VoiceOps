# PR Titles & Commit Messages (Rabbit Hole Ready)

**Ready-to-use PR titles and commit messages for CodeRabbit integration**

---

## 🔹 PR #1 — Show CodeRabbit is in the Game

### PR Title
```
Production-grade Incident schema validation & safety baseline
```

### PR Description (Short)
```
- Add strict Incident JSON Schema (additionalProperties=false)
- Enforce validation before persistence
- Prepare hooks for PII handling and retries
```

### Commit Messages Inside PR
```
feat(schema): add strict incident.v1.json with required fields

feat(api): enforce schema validation before storing incidents

chore(logging): add safe logging boundaries (no raw transcripts)
```

---

## 🔹 PR #2 — Rabbit Hole Moment (Very Important)

### PR Title
```
Apply CodeRabbit security & reliability recommendations
```

### PR Description
```
This PR applies suggestions from CodeRabbit review:

- PII redaction and flags
- Invalid LLM output fallback
- Table-driven tests for severity and schema constraints

Changes implemented based on CodeRabbit review feedback.
```

### Golden Commit Messages
```
test(incident): add table-driven tests for severity & defaults (CodeRabbit)

fix(security): redact PII from summaries as suggested by CodeRabbit

feat(reliability): handle invalid LLM output with repair fallback
```

### ⚠️ Important
**Must write in PR description**:
> "Changes implemented based on CodeRabbit review feedback."

---

## 🔹 PR #3 — Optional (If Time Permits)

### PR Title
```
Add voice-first intake flow with deterministic severity mapping
```

### Commit
```
feat(voice): add 4-question VAPI intake flow with severity mapping
```

---

## 📋 Complete PR Workflow

### Step 1: Initial PR
1. Create PR #1 with schema and basic validation
2. Wait for CodeRabbit review
3. Document initial feedback

### Step 2: Rabbit Hole PR
1. Create PR #2 with title: **"Apply CodeRabbit security & reliability recommendations"**
2. Paste PR comment from `PR_COMMENT_FOR_CODERABBIT.md`
3. Apply CodeRabbit suggestions
4. Use commit messages that mention CodeRabbit
5. Update README with "How CodeRabbit Improved This Code"

### Step 3: Follow-up PRs
1. Continue applying CodeRabbit suggestions
2. Reference CodeRabbit in commit messages
3. Show iterative improvement

---

## 🎯 Key Commit Message Patterns

### For CodeRabbit-Related Changes
```
fix(security): redact PII as suggested by CodeRabbit
test: add table-driven tests (CodeRabbit)
feat(reliability): handle invalid LLM output (CodeRabbit)
refactor(schema): enforce additionalProperties=false (CodeRabbit)
```

### For Regular Features
```
feat(api): add incident creation from transcript
feat(schema): add strict JSON Schema validation
feat(scoring): add deterministic severity classification
```

### For Fixes
```
fix(validation): handle missing required fields
fix(security): prevent PII leakage in logs
fix(reliability): add retry logic for webhook delivery
```

---

## ✅ Checklist for Rabbit Hole PR

- [ ] PR title mentions CodeRabbit or "security & reliability recommendations"
- [ ] PR description includes "Changes implemented based on CodeRabbit review feedback"
- [ ] At least one commit message mentions CodeRabbit
- [ ] CodeRabbit comment is included in PR
- [ ] README updated with "How CodeRabbit Improved This Code" section
- [ ] Tests added based on CodeRabbit suggestions
- [ ] Security improvements documented

---

**Last Updated**: 2025-01-27

