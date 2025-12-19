# تست اتصال VAPI و CodeRabbit

## ✅ VAPI Connection Test

### Status
- ✅ VAPI CLI نصب شده
- ✅ VAPI MCP در Cursor configure شده
- ✅ VAPI API Key تنظیم شده: `ff8c3bb0-6b6f-4f24-82fc-11a48c82d82f`

### Test Results
```bash
python scripts/test_vapi_connection.py
```

---

## 🐰 CodeRabbit Connection Test

### Step 1: اتصال به GitHub

1. به [CodeRabbit Dashboard](https://app.coderabbit.ai) بروید
2. Sign in با GitHub account
3. Repository را connect کنید: `amirmirmehrkar-git/VoiceOps`

### Step 2: تست با PR اولیه

```bash
# Create test branch
git checkout -b test/coderabbit-connection

# Make a small change
echo "# Test PR for CodeRabbit" >> TEST.md
git add TEST.md
git commit -m "test: verify CodeRabbit connection"

# Push and create PR
git push origin test/coderabbit-connection
```

### Step 3: بررسی CodeRabbit Review

- CodeRabbit باید به صورت خودکار PR را review کند
- پیشنهادات را در PR comments می‌بینید

---

## 📋 Checklist

### VAPI
- [x] VAPI CLI نصب شده
- [x] VAPI MCP configure شده
- [x] API Key تنظیم شده
- [ ] Assistant ایجاد شده
- [ ] Webhook تست شده

### CodeRabbit
- [ ] CodeRabbit Dashboard login
- [ ] Repository connected
- [ ] Test PR created
- [ ] CodeRabbit review received

---

**Last Updated**: 2025-01-27

