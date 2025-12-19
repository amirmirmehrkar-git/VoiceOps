# VoiceOps MVP - Quick Start Guide

## ✅ ساختار ایجاد شده

```
VoiceOps/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app + VAPI webhook
│   ├── models.py        # Pydantic models
│   ├── scoring.py       # Rule-based severity scoring
│   ├── security.py      # PII detection & redaction
│   └── validator.py     # JSON Schema validation
├── schemas/
│   └── incident.v1.mvp.json  # MVP schema
├── demo_incident.json   # Demo incident for PR
└── requirements.txt     # Dependencies
```

## 🚀 نصب و اجرا

### 1. نصب dependencies

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

pip install fastapi uvicorn pydantic python-dotenv jsonschema pytest httpx
```

### 2. اجرای سرور

```bash
uvicorn app.main:app --reload --port 8000
```

### 3. تست Health Check

```bash
curl http://localhost:8000/health
```

### 4. تست VAPI Webhook

```bash
curl -X POST http://localhost:8000/webhook/vapi \
  -H "Content-Type: application/json" \
  -d "{\"transcript\":\"Checkout is down, 500 errors. Contact me amir@example.com\"}"
```

## 📋 ویژگی‌های MVP

- ✅ VAPI webhook endpoint
- ✅ PII detection (email, phone, IP)
- ✅ PII redaction
- ✅ Rule-based severity scoring
- ✅ JSON Schema validation
- ✅ Production-ready error handling

## 🐰 آماده برای CodeRabbit PR

فایل `demo_incident.json` آماده است برای PR اول.

```bash
git checkout -b pr1-mvp-fastapi
git add .
git commit -m "MVP: VAPI webhook -> Incident JSON -> schema validation -> severity scoring"
git push origin pr1-mvp-fastapi
```

## 🔗 وصل کردن VAPI

برای لوکال development، از ngrok استفاده کن:

```bash
npx ngrok http 8000
```

در VAPI dashboard:
- Webhook URL = `https://xxxx.ngrok-free.app/webhook/vapi`

