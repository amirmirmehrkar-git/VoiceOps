# 🚀 راهنمای اجرای سرور VoiceOps MVP

## روش 1: اجرای مستقیم (سریع‌ترین)

### گام 1: فعال کردن virtual environment (اگر دارید)

```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### گام 2: نصب dependencies (اگر نصب نشده)

```bash
pip install fastapi uvicorn pydantic python-dotenv jsonschema
```

### گام 3: اجرای سرور

```bash
uvicorn app.main:app --reload --port 8000
```

**خروجی مورد انتظار:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### گام 4: تست سرور

در مرورگر باز کن:
- http://localhost:8000/health
- http://localhost:8000/docs (Swagger UI)

یا با curl:
```bash
curl http://localhost:8000/health
```

---

## روش 2: اجرا با Python مستقیم

```bash
python -m uvicorn app.main:app --reload --port 8000
```

---

## روش 3: اجرا با script (پیشنهادی)

ایجاد فایل `run_server.py`:

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
```

سپس اجرا کن:
```bash
python run_server.py
```

---

## 🔧 تنظیمات پیشرفته

### تغییر پورت

```bash
uvicorn app.main:app --reload --port 3000
```

### اجرا بدون auto-reload (production)

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### اجرا با workers (production)

```bash
uvicorn app.main:app --workers 4 --port 8000
```

---

## ✅ تست Webhook Endpoint

### تست با curl

```bash
curl -X POST http://localhost:8000/webhook/vapi \
  -H "Content-Type: application/json" \
  -d "{\"transcript\":\"Checkout is down, 500 errors. Contact me amir@example.com\"}"
```

### تست با PowerShell

```powershell
$body = @{
    transcript = "Checkout is down, 500 errors. Contact me amir@example.com"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/webhook/vapi" -Method POST -Body $body -ContentType "application/json"
```

---

## 🐛 عیب‌یابی

### خطا: `ModuleNotFoundError: No module named 'app'`

**راه حل:** مطمئن شو که در root directory پروژه هستی:
```bash
cd C:\Amir\VoiceOps
uvicorn app.main:app --reload
```

### خطا: `Address already in use`

**راه حل:** پورت 8000 قبلاً استفاده شده. پورت دیگری انتخاب کن:
```bash
uvicorn app.main:app --reload --port 8001
```

### خطا: `ImportError: cannot import name 'app'`

**راه حل:** مطمئن شو که `app/main.py` وجود دارد و `app = FastAPI(...)` در آن تعریف شده.

---

## 📝 نکات مهم

1. **Auto-reload**: با `--reload` هر تغییر در کد به صورت خودکار reload می‌شود
2. **Swagger UI**: بعد از اجرا، به http://localhost:8000/docs برو برای دیدن API documentation
3. **Health Check**: همیشه `/health` را تست کن قبل از webhook
4. **Logs**: تمام request‌ها در console نمایش داده می‌شوند

---

## 🔗 وصل کردن VAPI (برای production)

برای لوکال development، از ngrok استفاده کن:

```bash
# Terminal 1: سرور را اجرا کن
uvicorn app.main:app --reload --port 8000

# Terminal 2: ngrok را اجرا کن
npx ngrok http 8000
```

در VAPI dashboard:
- Webhook URL = `https://xxxx.ngrok-free.app/webhook/vapi`

