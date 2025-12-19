# VAPI Webhook Payload Structure

## ساختار دقیق Payload VAPI

بر اساس کد موجود و مستندات VAPI، payload structure این شکلی است:

### ساختار اصلی (end-of-call event)

```json
{
  "type": "end-of-call",
  "call": {
    "id": "call_abc123",
    "transcript": "Full transcript text here..."
  }
}
```

### فیلدهای مهم

- **`type`** (required): نوع event
  - `"end-of-call"`: تماس تمام شده، transcript آماده است
  - `"call-started"`: تماس شروع شده
  - `"speech-update"`: به‌روزرسانی real-time transcript

- **`call.id`** (optional): شناسه یکتا تماس
- **`call.transcript`** (optional): متن کامل transcript

### حالت‌های ممکن

VAPI ممکن است transcript را در یکی از این مکان‌ها بفرستد:

1. **در `call.transcript`** (رایج‌ترین):
```json
{
  "type": "end-of-call",
  "call": {
    "id": "call_123",
    "transcript": "Production is down..."
  }
}
```

2. **در root level** (گاهی):
```json
{
  "type": "end-of-call",
  "transcript": "Production is down...",
  "call": {
    "id": "call_123"
  }
}
```

## Endpoint تنظیم شده

Endpoint در `app/main.py` هر دو حالت را پشتیبانی می‌کند:

```python
# Extract transcript (flexible)
transcript = (
    (payload.call.transcript if payload.call else None) or
    payload.transcript or
    ""
).strip()

# Extract call_id
call_id = (
    (payload.call.id if payload.call else None) or
    (payload.call.call_id if payload.call else None) or
    None
)
```

## تست Endpoint

### تست با curl

```bash
curl -X POST http://localhost:8000/webhook/vapi \
  -H "Content-Type: application/json" \
  -d '{
    "type": "end-of-call",
    "call": {
      "id": "call_test_123",
      "transcript": "Checkout is down, 500 errors. Contact me amir@example.com"
    }
  }'
```

### تست با PowerShell

```powershell
$body = @{
    type = "end-of-call"
    call = @{
        id = "call_test_123"
        transcript = "Checkout is down, 500 errors. Contact me amir@example.com"
    }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/webhook/vapi" `
    -Method POST `
    -Body $body `
    -ContentType "application/json"
```

## Response

Endpoint یک incident JSON برمی‌گرداند:

```json
{
  "ok": true,
  "incident": {
    "incident_id": "inc_abc123",
    "title": "Checkout is down (500 errors) - [REDACTED_EMAIL]",
    "summary": "Checkout is down, 500 errors. Contact me [REDACTED_EMAIL]",
    "category": "operational_outage",
    "severity": "sev1",
    "confidence": 0.75,
    "pii": {
      "contains_pii": true,
      "pii_types": ["email"],
      "redacted": true
    },
    "notes": {
      "severity_reasoning": "Rule-based scoring for category=operational_outage.",
      "category_reasoning": "Heuristic keyword routing based on transcript."
    }
  }
}
```

