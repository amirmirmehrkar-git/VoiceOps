# راهنمای استفاده از ابزارهای هکاتون

این راهنما نحوه استفاده از ابزارهای اصلی هکاتون برای پروژه VoiceOps را توضیح می‌دهد.

---

## 🐰 CodeRabbit

### نقش در VoiceOps
- بازبینی Pull Requestها
- پیشنهاد بهبود امنیت، تست، و معماری
- مسیر جایزه Rabbit Hole

### نحوه استفاده

#### 1. نصب CodeRabbit
```bash
# Windows (PowerShell)
iex ((New-Object System.Net.WebClient).DownloadString('https://coderabbit.ai/install.ps1'))
```

#### 2. اتصال به GitHub
1. به [CodeRabbit Dashboard](https://app.coderabbit.ai) بروید
2. Repository را connect کنید
3. CodeRabbit به صورت خودکار PRها را review می‌کند

#### 3. ایجاد PR برای Review
```bash
# Create a feature branch
git checkout -b feature/incident-api

# Make changes and commit
git add .
git commit -m "feat: implement incident creation API"

# Push and create PR
git push origin feature/incident-api
```

#### 4. PR Title برای Rabbit Hole
```markdown
Apply CodeRabbit security & reliability recommendations
```

#### 5. Commit Messages با CodeRabbit
```bash
git commit -m "fix(security): redact PII as suggested by CodeRabbit"
git commit -m "test: add table-driven tests (CodeRabbit)"
```

### نکات مهم
- CodeRabbit به صورت خودکار PRها را review می‌کند
- پیشنهادات را در PR comments می‌بینید
- برای Rabbit Hole، حتماً PR title و commit messages را طبق راهنما بنویسید

---

## 🏄 Windsurf

### نقش در VoiceOps
- AI Coding Agent
- کمک به کدنویسی سریع
- بهینه‌سازی workflow توسعه

### نحوه استفاده

#### 1. نصب Windsurf
```bash
# Download from https://codeium.com/windsurf
# یا از VS Code Marketplace نصب کنید
```

#### 2. استفاده در پروژه
1. پروژه را در Windsurf باز کنید
2. از AI Agent برای:
   - نوشتن کد جدید
   - Refactoring
   - نوشتن تست‌ها
   - Debugging

#### 3. مثال استفاده
```
# در Windsurf Chat بپرسید:
"Implement PII redaction function for Persian text"
"Write table-driven tests for severity classification"
"Add error handling for LLM API calls"
```

### نکات مهم
- Windsurf برای کدنویسی سریع عالی است
- از Agent برای تکمیل کدهای پیچیده استفاده کنید

---

## 🏖️ Daytona

### نقش در VoiceOps
- Cloud Dev Environment
- Fast Deployment
- مسیر جایزه: Daytona Compute Track

### نحوه استفاده

#### 1. نصب Daytona CLI
```bash
# Windows
winget install daytona

# یا از https://www.daytona.io/downloads دانلود کنید
```

#### 2. راه‌اندازی پروژه
```bash
# Initialize Daytona workspace
daytona init

# Start workspace
daytona start
```

#### 3. Deploy با Docker
```bash
# Build Docker image
docker build -t voiceops-api .

# Run with docker-compose
docker-compose up -d
```

#### 4. Deploy به Daytona
```bash
# Push to GitHub first
git push origin main

# Deploy from Daytona dashboard
# یا از CLI:
daytona deploy
```

### نکات مهم
- Daytona برای Fast Deployment عالی است
- از Docker برای consistency استفاده کنید
- برای جایزه Daytona، حتماً deployment را در documentation نشان دهید

---

## 📞 VAPI

### نقش در VoiceOps
- Voice AI (Text ↔ Voice)
- ساخت Voice Agent
- تماس تلفنی، voice intake

### نحوه استفاده

#### 1. نصب VAPI CLI
```bash
# Windows (PowerShell)
iex ((New-Object System.Net.WebClient).DownloadString('https://vapi.ai/install.ps1'))
```

#### 2. Login
```bash
vapi login
```

#### 3. تنظیم API Key
```powershell
# PowerShell
$env:VAPI_API_KEY = "your-api-key-here"
```

#### 4. ایجاد Assistant
از VAPI Dashboard:
1. به [VAPI Dashboard](https://dashboard.vapi.ai) بروید
2. Create Assistant
3. از prompt در `engineering/vapi_agent_prompt_4questions.txt` استفاده کنید

#### 5. تنظیم Webhook
```bash
# Webhook URL برای VoiceOps
https://your-api-url.com/api/v1/vapi/webhook
```

### نکات مهم
- VAPI برای Voice-first projects ضروری است
- Webhook را برای دریافت transcripts تنظیم کنید
- از 4-question prompt استفاده کنید

---

## 🧑‍💻 GitHub

### نقش در VoiceOps
- Repository management
- Pull Request workflow
- اتصال به CodeRabbit

### نحوه استفاده

#### 1. Repository Setup
```bash
# Clone repository
git clone https://github.com/amirmirmehrkar-git/VoiceOps.git
cd VoiceOps

# Create feature branch
git checkout -b feature/your-feature
```

#### 2. PR Workflow
```bash
# Make changes
git add .
git commit -m "feat: your feature"

# Push and create PR
git push origin feature/your-feature
```

#### 3. CodeRabbit Integration
- CodeRabbit به صورت خودکار PRها را review می‌کند
- پیشنهادات را در PR comments می‌بینید

---

## 🐳 Docker

### نقش در VoiceOps
- Containerization
- Deploy سریع با Daytona
- Consistency across environments

### نحوه استفاده

#### 1. Build Image
```bash
docker build -t voiceops-api .
```

#### 2. Run Container
```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your-key \
  -e VAPI_API_KEY=your-key \
  voiceops-api
```

#### 3. Docker Compose
```bash
docker-compose up -d
```

---

## 🧪 Testing

### نقش در VoiceOps
- Table-driven tests
- Schema validation tests
- Integration tests

### نحوه استفاده

#### 1. Run Tests
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/
```

#### 2. Table-Driven Tests
```python
# tests/test_incident_table.py
test_cases = [
    {
        "name": "sev1 outage",
        "input": {...},
        "expected": {"severity": "sev1", ...}
    },
    # ...
]
```

---

## 🔗 Integrations

### Jira
```bash
# Environment variables
export JIRA_URL="https://your-jira.atlassian.net"
export JIRA_EMAIL="your-email@example.com"
export JIRA_API_TOKEN="your-token"
export JIRA_PROJECT_KEY="VO"
```

### PagerDuty
```bash
# Environment variable
export PAGERDUTY_ROUTING_KEY="your-routing-key"
```

---

## 📋 Checklist برای هکاتون

### قبل از شروع
- [ ] CodeRabbit connected به GitHub
- [ ] VAPI API key تنظیم شده
- [ ] LLM API key (OpenAI/Anthropic) تنظیم شده
- [ ] Daytona workspace راه‌اندازی شده
- [ ] Docker نصب شده

### در طول هکاتون
- [ ] PRها با CodeRabbit review شده‌اند
- [ ] Tests نوشته شده‌اند
- [ ] API endpoints کار می‌کنند
- [ ] VAPI webhook تنظیم شده
- [ ] Deploy به Daytona انجام شده

### برای Demo
- [ ] Demo scenarios آماده
- [ ] curl commands تست شده
- [ ] Screenshot از CodeRabbit PR
- [ ] Documentation کامل

---

## 🎯 مسیرهای جایزه

### Rabbit Hole (CodeRabbit)
- PR title: "Apply CodeRabbit security & reliability recommendations"
- Commit messages با "CodeRabbit" mention
- Screenshot از CodeRabbit suggestions

### Daytona Compute Track
- Fast deployment
- Docker setup
- Production-ready deployment

### Most Impressive
- Voice-first innovation
- Production-ready code
- Complete documentation

---

**Last Updated**: 2025-01-27

