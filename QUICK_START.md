# VoiceOps - Quick Start Guide

راهنمای سریع برای راه‌اندازی VoiceOps در هکاتون.

---

## 🚀 راه‌اندازی سریع (5 دقیقه)

### 1. Clone Repository
```bash
git clone https://github.com/amirmirmehrkar-git/VoiceOps.git
cd VoiceOps
```

### 2. نصب Dependencies
```bash
pip install -r requirements.txt
```

### 3. تنظیم Environment Variables
```bash
# کپی .env.example به .env
cp .env.example .env

# ویرایش .env و اضافه کردن API keys
# حداقل نیاز: OPENAI_API_KEY یا ANTHROPIC_API_KEY
```

### 4. راه‌اندازی API
```bash
# Run locally
python main.py

# یا با uvicorn
uvicorn main:app --reload
```

### 5. تست API
```bash
# Health check
curl http://localhost:8000/health

# Create incident
curl -X POST http://localhost:8000/api/v1/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "از ساعت ۱۸:۰۵ checkout-api توی پروداکشن ۵۰۰ می‌دهد",
    "call_id": "test_001"
  }'
```

---

## 🐳 با Docker

### Build & Run
```bash
# Build image
docker build -t voiceops-api .

# Run container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-key \
  voiceops-api
```

### با Docker Compose
```bash
docker-compose up -d
```

---

## 📞 تنظیم VAPI

### 1. نصب VAPI CLI
```powershell
iex ((New-Object System.Net.WebClient).DownloadString('https://vapi.ai/install.ps1'))
```

### 2. Login
```bash
vapi login
```

### 3. Setup MCP در Cursor (اختیاری)

**روش جدید (پیشنهادی):**
```bash
# نصب MCP server
npm install -g @vapi-ai/mcp-server

# فایل .cursor/mcp.json خودکار ایجاد شده است
# Cursor را restart کنید
```

**روش قدیمی:**
```bash
vapi mcp setup cursor
```

**برای راهنمای کامل**: `VAPI_MCP_CURSOR_SETUP.md`

### 4. تنظیم API Key
```powershell
$env:VAPI_API_KEY = "your-vapi-api-key"
```

### 5. ایجاد Assistant

**روش 1: با Script (پیشنهادی)**
```bash
python scripts/setup_vapi_assistant.py
```

**روش 2: از VAPI Dashboard**
1. به [VAPI Dashboard](https://dashboard.vapi.ai) بروید
2. Create Assistant
3. از prompt در `engineering/vapi_agent_prompt_4questions.txt` استفاده کنید
4. Webhook URL: `https://your-api-url.com/api/v1/vapi/webhook`

### 6. تست تماس
```bash
# Test با transcript
python scripts/test_vapi_call.py
```

---

## 🧪 تست

### Run Tests
```bash
pytest tests/
```

### Test با Demo Scenarios
```bash
# استفاده از demo scenarios
python -m pytest tests/test_incident_table.py -v
```

---

## 🔗 Integrations

### Jira
```bash
export JIRA_URL="https://your-jira.atlassian.net"
export JIRA_EMAIL="your-email@example.com"
export JIRA_API_TOKEN="your-token"
```

### PagerDuty
```bash
export PAGERDUTY_ROUTING_KEY="your-routing-key"
```

---

## 📚 Documentation

- **Hackathon Tools Guide**: `HACKATHON_TOOLS_GUIDE.md`
- **Architecture**: `ARCHITECTURE.md`
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)

---

## 🎯 برای هکاتون

### Checklist
- [ ] API running
- [ ] VAPI webhook configured
- [ ] Tests passing
- [ ] Docker build successful
- [ ] Demo scenarios ready

### Demo Commands
```bash
# Test incident creation
curl -X POST http://localhost:8000/api/v1/incidents \
  -H "Content-Type: application/json" \
  -d @demo/demo_scenario_1_outage.json

# Validate incident
curl -X POST http://localhost:8000/api/v1/incidents/validate \
  -H "Content-Type: application/json" \
  -d @demo/demo_scenario_1_outage.json
```

---

**Need Help?** Check `HACKATHON_TOOLS_GUIDE.md` for detailed instructions.

