# VAPI MCP Setup برای Cursor

راهنمای کامل برای راه‌اندازی VAPI MCP در Cursor و دریافت ورودی Voice.

**⚠️ توجه**: این فایل برای setup قدیمی است. برای setup جدید با MCP server، به `VAPI_MCP_CURSOR_SETUP.md` مراجعه کنید.

---

## 🔧 نصب VAPI MCP در Cursor

### 1. نصب VAPI CLI
```powershell
# Windows PowerShell
iex ((New-Object System.Net.WebClient).DownloadString('https://vapi.ai/install.ps1'))
```

### 2. Login به VAPI
```bash
vapi login
```

### 3. Setup MCP در Cursor
```bash
vapi mcp setup cursor
```

این دستور:
- VAPI MCP server را در Cursor اضافه می‌کند
- API keys را configure می‌کند
- Cursor را برای استفاده از VAPI آماده می‌کند

---

## 📞 دریافت ورودی Voice

### روش 1: از طریق VAPI Dashboard

1. **ایجاد Assistant در VAPI Dashboard**
   - به [VAPI Dashboard](https://dashboard.vapi.ai) بروید
   - Create Assistant
   - از prompt در `engineering/vapi_agent_prompt_4questions.txt` استفاده کنید

2. **تنظیم Webhook**
   - Webhook URL: `https://your-api-url.com/api/v1/vapi/webhook`
   - Events: `end-of-call-report`

3. **تماس تست**
   - از VAPI Dashboard یک تماس تست بگیرید
   - Transcript به webhook شما ارسال می‌شود

### روش 2: از طریق VAPI API

```python
# استفاده از VAPI API برای ایجاد تماس
import requests

VAPI_API_KEY = "your-vapi-api-key"
ASSISTANT_ID = "your-assistant-id"

# Create a call
response = requests.post(
    "https://api.vapi.ai/call",
    headers={
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "assistantId": ASSISTANT_ID,
        "phoneNumberId": "your-phone-number-id"
    }
)
```

### روش 3: از طریق VAPI CLI

```bash
# Create a call
vapi call create \
  --assistant-id YOUR_ASSISTANT_ID \
  --phone-number YOUR_PHONE_NUMBER
```

---

## 🔗 اتصال VAPI به VoiceOps API

### 1. تنظیم Webhook در VAPI

```python
# در VAPI Dashboard یا API
webhook_config = {
    "url": "https://your-voiceops-api.com/api/v1/vapi/webhook",
    "events": ["end-of-call-report", "conversation-update"]
}
```

### 2. Webhook Handler در VoiceOps

Webhook handler در `api/vapi_webhook.py` آماده است:

```python
@app.post("/api/v1/vapi/webhook")
async def vapi_webhook(request: Request):
    webhook_data = await request.json()
    result = handle_vapi_webhook(webhook_data)
    return result
```

### 3. تست Webhook

```bash
# Test webhook locally با ngrok
ngrok http 8000

# سپس در VAPI Dashboard webhook URL را تنظیم کنید:
# https://your-ngrok-url.ngrok.io/api/v1/vapi/webhook
```

---

## 🎤 استفاده از VAPI MCP در Cursor

بعد از setup، می‌توانید از VAPI MCP در Cursor استفاده کنید:

### دستورات MCP

1. **ایجاد Assistant**
   ```
   Create a VAPI assistant for VoiceOps incident reporting
   ```

2. **ایجاد تماس**
   ```
   Make a test call to the VAPI assistant
   ```

3. **دریافت Transcript**
   ```
   Get the transcript from the last VAPI call
   ```

---

## 📝 مثال کامل: از Voice تا Incident

### Step 1: تماس Voice
کاربر با VAPI Assistant تماس می‌گیرد و می‌گوید:
```
"از ساعت ۱۸:۰۵ checkout-api توی پروداکشن ۵۰۰ می‌دهد"
```

### Step 2: VAPI Webhook
VAPI webhook به VoiceOps API ارسال می‌شود:
```json
{
  "type": "end-of-call-report",
  "call": {
    "id": "call_123",
    "transcript": "از ساعت ۱۸:۰۵ checkout-api توی پروداکشن ۵۰۰ می‌دهد"
  }
}
```

### Step 3: پردازش در VoiceOps
```python
# api/vapi_webhook.py
def handle_end_of_call(webhook_data):
    transcript = webhook_data["call"]["transcript"]
    call_id = webhook_data["call"]["id"]
    
    # Create incident
    incident = create_incident_from_transcript(
        transcript=transcript,
        call_id=call_id
    )
    
    return incident
```

### Step 4: خروجی Incident JSON
```json
{
  "schema_version": "1.0.0",
  "source": {
    "channel": "voice",
    "vendor": "vapi",
    "call_id": "call_123"
  },
  "title": "Checkout API returning 500 errors in production",
  "severity": "sev1",
  "category": "service_outage",
  ...
}
```

---

## 🧪 تست Local با ngrok

### 1. نصب ngrok
```bash
# Download from https://ngrok.com/download
# یا
winget install ngrok
```

### 2. راه‌اندازی ngrok
```bash
# Terminal 1: Run VoiceOps API
python main.py

# Terminal 2: Run ngrok
ngrok http 8000
```

### 3. تنظیم Webhook در VAPI
```
Webhook URL: https://your-ngrok-url.ngrok.io/api/v1/vapi/webhook
```

### 4. تست تماس
- از VAPI Dashboard یک تماس تست بگیرید
- Transcript به local API شما ارسال می‌شود

---

## 🔑 Environment Variables

```bash
# .env
VAPI_API_KEY=your-vapi-api-key
VAPI_PUBLIC_KEY=your-vapi-public-key
VAPI_WEBHOOK_SECRET=your-webhook-secret  # Optional
```

---

## 📋 Checklist

- [ ] VAPI CLI نصب شده
- [ ] `vapi login` انجام شده
- [ ] `vapi mcp setup cursor` اجرا شده
- [ ] Assistant در VAPI Dashboard ایجاد شده
- [ ] Webhook URL تنظیم شده
- [ ] VoiceOps API running
- [ ] ngrok برای local testing (اختیاری)
- [ ] تست تماس انجام شده

---

## 🐛 Troubleshooting

### مشکل: VAPI MCP در Cursor کار نمی‌کند
```bash
# بررسی کنید که VAPI CLI نصب است
vapi --version

# دوباره setup کنید
vapi mcp setup cursor
```

### مشکل: Webhook دریافت نمی‌شود
- بررسی کنید که ngrok running است
- Webhook URL را در VAPI Dashboard دوباره چک کنید
- Logs را در VoiceOps API بررسی کنید

### مشکل: Transcript خالی است
- بررسی کنید که Assistant به درستی configure شده
- از VAPI Dashboard logs را بررسی کنید

---

**Last Updated**: 2025-01-27

