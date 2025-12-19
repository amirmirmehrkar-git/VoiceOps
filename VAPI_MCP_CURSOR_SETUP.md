# VAPI MCP Setup برای Cursor - راهنمای کامل

راهنمای کامل برای راه‌اندازی VAPI MCP در Cursor IDE.

---

## 📋 پیش‌نیازها

- Node.js و npm نصب شده
- Cursor IDE
- VAPI API Key

---

## 🔧 Step 1: نصب MCP Server

### نصب Global MCP Server
```bash
npm install -g @vapi-ai/mcp-server
```

### یا نصب Local
```bash
npm install @vapi-ai/mcp-server
```

---

## 📝 Step 2: ایجاد فایل Configuration

فایل `.cursor/mcp.json` در root پروژه ایجاد شده است:

```json
{
  "servers": {
    "vapi-docs": {
      "command": "npx",
      "args": ["@vapi-ai/mcp-server"]
    }
  }
}
```

---

## ✅ Step 3: بررسی Configuration

```bash
vapi mcp status
```

خروجی مورد انتظار:
```
MCP Configuration Status:
✓ Cursor: Configured (.cursor/mcp.json)
✗ Windsurf: Not configured
✗ VSCode: Not configured
Vapi MCP Server: v1.2.3 (latest)
```

---

## 🔄 Step 4: Restart Cursor

**مهم**: بعد از configuration، Cursor را restart کنید تا MCP integration load شود.

---

## 🎯 استفاده از VAPI MCP در Cursor

بعد از setup، می‌توانید از VAPI MCP در Cursor استفاده کنید:

### مثال 1: ایجاد Assistant

**Prompt در Cursor:**
```
How do I create a voice assistant with Vapi for VoiceOps incident reporting?
```

**Cursor پاسخ می‌دهد:**
```python
from vapi_ai import VapiClient
import os

client = VapiClient(api_key=os.getenv("VAPI_API_KEY"))

assistant = client.assistants.create({
    "name": "VoiceOps Incident Intake",
    "firstMessage": "سلام، من VoiceOps هستم. برای گزارش حادثه، لطفاً به ۴ سؤال من پاسخ دهید.",
    "model": {
        "provider": "openai",
        "model": "gpt-4o",
        "systemPrompt": open("engineering/vapi_agent_prompt_4questions.txt").read()
    },
    "voice": {
        "provider": "vapi",
        "voiceId": "Elliot"
    },
    "transcriber": {
        "provider": "deepgram",
        "model": "nova-3",
        "language": "fa"
    },
    "serverUrl": "https://your-api.com/api/v1/vapi/webhook"
})
```

### مثال 2: Webhook Handling

**Prompt در Cursor:**
```
Show me how to handle Vapi webhooks in FastAPI for VoiceOps
```

**Cursor پاسخ می‌دهد:**
```python
from fastapi import FastAPI, Request
from api.vapi_webhook import handle_vapi_webhook

app = FastAPI()

@app.post("/api/v1/vapi/webhook")
async def vapi_webhook(request: Request):
    webhook_data = await request.json()
    event_type = webhook_data.get("type")
    
    if event_type == "end-of-call-report":
        transcript = webhook_data["call"]["transcript"]
        call_id = webhook_data["call"]["id"]
        
        # Process incident
        incident = create_incident_from_transcript(
            transcript=transcript,
            call_id=call_id
        )
        
        return {"status": "success", "incident": incident}
    
    return {"status": "received"}
```

### مثال 3: Call Transfer

**Prompt در Cursor:**
```
How do I transfer calls to a human agent in Vapi?
```

### مثال 4: Function Calls

**Prompt در Cursor:**
```
Show me how to handle function calls in Vapi webhooks
```

---

## 🚀 VAPI CLI Commands

### Initialize Project
```bash
vapi init
```

این دستور:
- SDK را نصب می‌کند
- Components را generate می‌کند
- Webhook handler را ایجاد می‌کند
- Environment template را اضافه می‌کند

### Setup MCP
```bash
vapi mcp setup
```

### Listen to Webhooks (Local Development)
```bash
# Terminal 1: Create tunnel (e.g., with ngrok)
ngrok http 8000

# Terminal 2: Forward webhooks
vapi listen --forward-to localhost:8000/api/v1/vapi/webhook
```

---

## 💡 Best Practices

### 1. سؤالات دقیق بپرسید

✅ **خوب:**
```
"How do I transfer calls to a human agent in Vapi?"
"Show me a complete example of handling speech updates"
"Using Vapi Python SDK, how do I create an assistant with Persian language support?"
```

❌ **بد:**
```
"How do I transfer calls?"
"Show me webhook"
```

### 2. درخواست مثال‌های کامل

```
"Show me a complete example of..."
"Generate a working implementation of..."
"Create a full webhook handler for..."
```

### 3. مشخص کردن SDK Version

```
"Using @vapi-ai/web v2.0, how do I..."
"What's the latest way to create assistants in Vapi?"
```

---

## 🔍 Troubleshooting

### مشکل: MCP در Cursor کار نمی‌کند

**راه‌حل:**
1. بررسی کنید که `.cursor/mcp.json` وجود دارد
2. Cursor را restart کنید
3. بررسی کنید که npm و npx در PATH هستند

```bash
# بررسی npm
npm --version

# بررسی npx
npx --version
```

### مشکل: MCP Server پیدا نمی‌شود

**راه‌حل:**
```bash
# نصب global
npm install -g @vapi-ai/mcp-server

# یا استفاده از npx (نیازی به نصب نیست)
# npx به صورت خودکار package را دانلود می‌کند
```

### مشکل: Webhook دریافت نمی‌شود

**راه‌حل:**
1. از ngrok برای local testing استفاده کنید
2. Webhook URL را در VAPI Dashboard بررسی کنید
3. Logs را در VoiceOps API چک کنید

```bash
# Terminal 1: Run API
python main.py

# Terminal 2: Run ngrok
ngrok http 8000

# در VAPI Dashboard:
# Webhook URL: https://your-ngrok-url.ngrok.io/api/v1/vapi/webhook
```

---

## 📚 منابع بیشتر

- **VAPI Documentation**: https://docs.vapi.ai
- **VAPI Dashboard**: https://dashboard.vapi.ai
- **MCP Documentation**: https://modelcontextprotocol.io

---

## ✅ Checklist

- [ ] Node.js و npm نصب شده
- [ ] `npm install -g @vapi-ai/mcp-server` اجرا شده
- [ ] `.cursor/mcp.json` ایجاد شده
- [ ] `vapi mcp status` موفقیت‌آمیز است
- [ ] Cursor restart شده
- [ ] تست با prompt در Cursor انجام شده

---

**Last Updated**: 2025-01-27

