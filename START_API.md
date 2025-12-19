# راه‌اندازی API Server

## روش 1: مستقیم
```bash
python main.py
```

## روش 2: با uvicorn
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## روش 3: با script
```bash
python scripts/start_api.py
```

---

## بعد از راه‌اندازی

### مشاهده خروجی در مرورگر:

1. **Demo Page**: http://localhost:8000/demo
2. **API Docs**: http://localhost:8000/docs
3. **Health Check**: http://localhost:8000/health
4. **Static HTML**: باز کردن `view_output.html` در مرورگر

---

## تست API

```bash
# Test endpoint
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

**نکته**: اگر `ERR_CONNECTION_REFUSED` می‌بینید، API server در حال اجرا نیست. یکی از روش‌های بالا را استفاده کنید.

