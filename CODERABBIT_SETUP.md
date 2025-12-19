# راهنمای اتصال CodeRabbit به VoiceOps

## 📋 مراحل اتصال

### Step 1: اطمینان از اتصال Repository

1. به [CodeRabbit Dashboard](https://app.coderabbit.ai) بروید
2. Repository `VoiceOps` را انتخاب کنید
3. اگر repository را نمی‌بینید:
   - به Settings → Repositories بروید
   - "Connect Repository" را بزنید
   - GitHub را authorize کنید
   - Repository `amirmirmehrkar-git/VoiceOps` را انتخاب کنید

### Step 2: ایجاد PR برای Review

CodeRabbit نیاز به یک PR باز دارد تا بتواند review کند.

```bash
# 1. Create a new branch
git checkout -b feature/initial-mvp

# 2. Add your changes
git add .

# 3. Commit with proper message
git commit -m "feat: implement MVP with voice intake and JSON output"

# 4. Push to GitHub
git push origin feature/initial-mvp
```

### Step 3: ایجاد PR در GitHub

1. به GitHub repository بروید: https://github.com/amirmirmehrkar-git/VoiceOps
2. "Compare & pull request" را بزنید
3. PR Title: `Production-grade Incident schema validation & safety baseline`
4. PR Description:
```markdown
## Changes
- Add strict Incident JSON Schema (additionalProperties=false)
- Implement voice intake → JSON conversion
- Add schema validation
- Add severity classification (sev1-sev4)
- Add PII redaction logic
- Add webhook handlers for VAPI, Jira, PagerDuty

## Testing
- MVP tested and working
- Schema validation passing
- End-to-end tests passing
```

### Step 4: منتظر CodeRabbit Review

- CodeRabbit به صورت خودکار PR را review می‌کند (معمولاً 1-2 دقیقه)
- پیشنهادات را در PR comments می‌بینید
- می‌توانید suggestions را apply کنید

---

## 🐰 برای Rabbit Hole Prize

### PR #2 (بعد از دریافت CodeRabbit suggestions)

**PR Title:**
```
Apply CodeRabbit security & reliability recommendations
```

**PR Description:**
```markdown
This PR applies suggestions from CodeRabbit review:

- PII redaction improvements
- Schema validation enhancements
- Test coverage improvements
- Security fixes

Changes implemented based on CodeRabbit review feedback.
```

**Commit Messages:**
```bash
fix(security): redact PII as suggested by CodeRabbit
test: add table-driven tests (CodeRabbit)
feat(reliability): handle invalid LLM output (CodeRabbit)
```

---

## ✅ Checklist

- [ ] CodeRabbit Dashboard login
- [ ] Repository connected
- [ ] Branch created
- [ ] Changes committed
- [ ] PR created on GitHub
- [ ] CodeRabbit review received
- [ ] Suggestions reviewed

---

## 🔗 لینک‌های مفید

- **CodeRabbit Dashboard**: https://app.coderabbit.ai
- **GitHub Repository**: https://github.com/amirmirmehrkar-git/VoiceOps
- **PR Template**: `coderabbit/PR_COMMENT_FOR_CODERABBIT.md`

---

**Status**: Ready to create PR

