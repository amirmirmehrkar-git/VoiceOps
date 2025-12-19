# Verification: VAPI & CodeRabbit Setup

## 🎯 هدف
تست و اطمینان از کارکرد VAPI و CodeRabbit قبل از شروع پروژه.

---

## ✅ VAPI Setup Verification

### 1. VAPI CLI
```bash
vapi --version
```
**Expected**: Version number

### 2. VAPI MCP Status
```bash
vapi mcp status
```
**Expected**: ✅ Configured with Vapi MCP server

### 3. VAPI API Connection
```bash
python scripts/test_vapi_connection.py
```
**Expected**: ✅ API connection successful

### 4. VAPI API Key
```powershell
echo $env:VAPI_API_KEY
```
**Expected**: `ff8c3bb0-6b6f-4f24-82fc-11a48c82d82f`

---

## 🐰 CodeRabbit Setup Verification

### 1. CodeRabbit Dashboard
- [ ] به [CodeRabbit Dashboard](https://app.coderabbit.ai) رفته‌اید
- [ ] با GitHub login کرده‌اید
- [ ] Repository `amirmirmehrkar-git/VoiceOps` را connect کرده‌اید

### 2. Test PR
```bash
# Create test branch
git checkout -b test/coderabbit-verification

# Make minimal change
echo "Test for CodeRabbit" > TEST_CODERABBIT.md
git add TEST_CODERABBIT.md
git commit -m "test: verify CodeRabbit connection"

# Push
git push origin test/coderabbit-verification
```

### 3. Create PR on GitHub
- Title: `Test: Verify CodeRabbit Connection`
- Description: `Testing CodeRabbit integration for VoiceOps project`
- Wait for CodeRabbit review

### 4. Verify CodeRabbit Review
- [ ] CodeRabbit comment در PR ظاهر شد
- [ ] پیشنهادات ارائه شد
- [ ] می‌توانید suggestions را apply کنید

---

## 📝 Next Steps After Verification

### اگر همه چیز کار می‌کند:
1. ✅ VAPI آماده برای استفاده
2. ✅ CodeRabbit آماده برای PR reviews
3. ✅ می‌توانید شروع به کار روی پروژه کنید

### اگر مشکلی وجود دارد:
1. VAPI: بررسی `VAPI_SETUP_GUIDE.md`
2. CodeRabbit: بررسی `HACKATHON_TOOLS_GUIDE.md`

---

**Status**: در حال تست...

