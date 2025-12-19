# MVP Complete Guide - VoiceOps

راهنمای کامل برای استفاده از MVP با VAPI.

---

## ✅ MVP Status

**MVP کار می‌کند!**

- ✅ Transcript → JSON conversion
- ✅ Schema validation
- ✅ Severity classification (sev1-sev4)
- ✅ Category classification
- ✅ PII detection
- ✅ API endpoints

---

## 🚀 راه‌اندازی سریع

### 1. نصب Dependencies
```bash
pip install -r requirements.txt
```

### 2. تست MVP (بدون LLM)
```bash
python test_mvp_simple.py
```

**خروجی**: JSON معتبر با severity و category درست

### 3. راه‌اندازی API
```bash
python main.py
```

API در `http://localhost:8000` اجرا می‌شود.

---

## 📞 اتصال VAPI برای Voice Input

### Step 1: ایجاد VAPI Assistant

```bash
python scripts/setup_vapi_assistant.py
```

یا از VAPI Dashboard:
1. به [VAPI Dashboard](https://dashboard.vapi.ai) بروید
2. Create Assistant
3. از prompt در `engineering/vapi_agent_prompt_4questions.txt` استفاده کنید

### Step 2: تنظیم Webhook

#### با ngrok (Local Testing)
```bash
# Terminal 1: Run API
python main.py

# Terminal 2: Run ngrok
ngrok http 8000

# در VAPI Dashboard:
# Webhook URL: https://your-ngrok-url.ngrok.io/api/v1/vapi/webhook
```

#### Production
```
Webhook URL: https://your-api-url.com/api/v1/vapi/webhook
```

### Step 3: تست تماس

1. از VAPI Dashboard یک تماس تست بگیرید
2. به 4 سؤال پاسخ دهید
3. Transcript به webhook شما ارسال می‌شود
4. Incident JSON ایجاد می‌شود

---

## 🧪 تست‌های موجود

### 1. تست ساده (Fallback Mode)
```bash
python test_mvp_simple.py
```

### 2. تست End-to-End
```bash
python scripts/test_end_to_end.py
```

### 3. تست API
```bash
# بعد از راه‌اندازی API:
curl -X POST http://localhost:8000/api/v1/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "از ساعت ۱۸:۰۵ checkout-api توی پروداکشن ۵۰۰ می‌دهد",
    "call_id": "test_001"
  }'
```

### 4. تست Webhook (Simulate VAPI)
```bash
python scripts/test_vapi_call.py
```

---

## 🔑 با LLM API Key (Full Mode)

### تنظیم API Key
```bash
# OpenAI
export OPENAI_API_KEY=your-key

# یا Anthropic
export ANTHROPIC_API_KEY=your-key
```

### مزایا
- ✅ بهتر title/summary extraction
- ✅ بهتر severity/category classification
- ✅ بهتر system/location detection
- ✅ Repair mechanism برای invalid JSON

---

## 📊 Flow کامل

```
1. کاربر تماس می‌گیرد → VAPI Assistant
   ↓
2. VAPI 4 سؤال می‌پرسد
   ↓
3. Transcript به webhook ارسال می‌شود
   POST /api/v1/vapi/webhook
   ↓
4. VoiceOps API پردازش می‌کند:
   - PII redaction
   - LLM structuring (یا fallback)
   - Schema validation
   - Severity classification
   ↓
5. Incident JSON آماده است
   ↓
6. (اختیاری) ارسال به Jira/PagerDuty
```

---

## 🎯 مثال خروجی

### Input (Transcript)
```
از ساعت ۱۸:۰۵ بعد از دیپلوی جدید، checkout-api توی پروداکشن ۵۰۰ می‌دهد. 
مشتری‌ها نمی‌تونن پرداخت کنن.
```

### Output (JSON)
```json
{
  "schema_version": "1.0.0",
  "source": {
    "channel": "voice",
    "vendor": "vapi",
    "call_id": "test_001"
  },
  "title": "Checkout API returning 500 errors in production",
  "category": "service_outage",
  "severity": "sev1",
  "status": "new",
  "systems": [{
    "name": "checkout-api",
    "environment": "prod"
  }],
  "confidence": 0.85
}
```

---

## ✅ Checklist

### MVP Ready
- [x] Dependencies نصب شده
- [x] API endpoints کار می‌کنند
- [x] Schema validation کار می‌کند
- [x] Severity classification کار می‌کند
- [x] Fallback mode کار می‌کند

### VAPI Integration
- [ ] VAPI Assistant ایجاد شده
- [ ] Webhook URL تنظیم شده
- [ ] ngrok برای local testing (اختیاری)
- [ ] تست تماس انجام شده

### Full Mode (اختیاری)
- [ ] LLM API key تنظیم شده
- [ ] تست با LLM انجام شده

---

## 🐛 Troubleshooting

### مشکل: LLM API error
**راه‌حل**: از fallback mode استفاده کنید (بدون API key)

### مشکل: Webhook دریافت نمی‌شود
**راه‌حل**: 
- ngrok را بررسی کنید
- Webhook URL را در VAPI Dashboard چک کنید
- Logs را در API بررسی کنید

### مشکل: Schema validation failed
**راه‌حل**: 
- از `/api/v1/incidents/validate` استفاده کنید
- بررسی کنید که همه required fields موجود هستند

---

## 📚 فایل‌های مهم

- `test_mvp_simple.py` - تست ساده MVP
- `run_mvp.py` - Demo interactive
- `main.py` - API server
- `scripts/setup_vapi_assistant.py` - ایجاد VAPI assistant
- `scripts/test_vapi_call.py` - تست VAPI webhook

---

**Status**: ✅ MVP Working  
**Ready for**: Hackathon, Demo, Pilot

