# MVP Quick Start - VoiceOps

راهنمای سریع برای راه‌اندازی و تست MVP.

---

## 🚀 راه‌اندازی سریع (3 دقیقه)

### 1. نصب Dependencies
```bash
pip install -r requirements.txt
```

### 2. تنظیم API Keys
```bash
# حداقل یکی از این‌ها:
export OPENAI_API_KEY=your-key
# یا
export ANTHROPIC_API_KEY=your-key
```

### 3. تست MVP
```bash
# تست کامل با demo scenarios
python run_mvp.py

# یا تست end-to-end
python scripts/test_end_to_end.py
```

### 4. راه‌اندازی API
```bash
# روش 1: با script
python scripts/start_api.py

# روش 2: مستقیم
python main.py

# روش 3: با uvicorn
uvicorn main:app --reload
```

---

## 🧪 تست‌های موجود

### 1. Demo Interactive
```bash
python run_mvp.py
```
- انتخاب scenario
- نمایش JSON خروجی
- Validation

### 2. End-to-End Tests
```bash
python scripts/test_end_to_end.py
```
- تست همه scenarios
- Validation خودکار
- گزارش نتایج

### 3. API Test
```bash
# بعد از راه‌اندازی API:
curl -X POST http://localhost:8000/api/v1/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "از ساعت ۱۸:۰۵ checkout-api توی پروداکشن ۵۰۰ می‌دهد",
    "call_id": "test_001"
  }'
```

---

## 📞 اتصال VAPI (اختیاری)

### 1. ایجاد Assistant
```bash
python scripts/setup_vapi_assistant.py
```

### 2. تست Webhook
```bash
# با ngrok برای local testing
ngrok http 8000

# در VAPI Dashboard webhook را تنظیم کنید:
# https://your-ngrok-url.ngrok.io/api/v1/vapi/webhook
```

---

## ✅ Checklist

- [ ] Dependencies نصب شده
- [ ] API key تنظیم شده (OpenAI یا Anthropic)
- [ ] `python run_mvp.py` کار می‌کند
- [ ] API server راه‌اندازی شده
- [ ] تست end-to-end موفق

---

## 🐛 Troubleshooting

### مشکل: LLM API error
- بررسی کنید API key درست است
- بررسی کنید quota دارید
- از fallback mode استفاده کنید (بدون LLM)

### مشکل: Schema validation failed
- بررسی کنید که همه required fields موجود هستند
- از `POST /api/v1/incidents/validate` استفاده کنید

### مشکل: Import errors
- مطمئن شوید که در root directory هستید
- `pip install -r requirements.txt` را اجرا کنید

---

**Ready to go!** 🚀

