# VAPI - ساختار دقیق Payload

## 📋 ساختار اصلی VAPI Webhook Payload

بر اساس مستندات رسمی VAPI و کد موجود، VAPI این payload را می‌فرستد:

### 1. Event: `end-of-call` (مهم‌ترین برای ما)

```json
{
  "type": "end-of-call",
  "call": {
    "id": "call_abc123def456",
    "status": "ended",
    "transcript": "Full conversation transcript here...",
    "startedAt": "2025-01-12T18:00:00Z",
    "endedAt": "2025-01-12T18:05:00Z",
    "duration": 300,
    "recordingUrl": "https://storage.vapi.ai/recordings/call_abc123.mp3"
  },
  "assistant": {
    "id": "assistant_xyz789",
    "name": "VoiceOps Incident Reporter"
  },
  "messages": [
    {
      "role": "user",
      "content": "Production API is down"
    },
    {
      "role": "assistant",
      "content": "I understand. Can you tell me more details?"
    }
  ]
}
```

### 2. Event: `call-started`

```json
{
  "type": "call-started",
  "call": {
    "id": "call_abc123def456",
    "status": "ringing",
    "startedAt": "2025-01-12T18:00:00Z"
  },
  "assistant": {
    "id": "assistant_xyz789"
  }
}
```

### 3. Event: `speech-update` (real-time)

```json
{
  "type": "speech-update",
  "call": {
    "id": "call_abc123def456",
    "status": "in-progress"
  },
  "message": {
    "role": "user",
    "content": "Partial transcript so far..."
  }
}
```

## 🔍 فیلدهای مهم برای Incident Processing

### برای `end-of-call` event:

| فیلد | مسیر | نوع | توضیح |
|------|------|-----|-------|
| **transcript** | `call.transcript` | string | **مهم‌ترین** - متن کامل مکالمه |
| **call_id** | `call.id` | string | شناسه یکتا تماس (برای idempotency) |
| **startedAt** | `call.startedAt` | ISO-8601 | زمان شروع تماس |
| **endedAt** | `call.endedAt` | ISO-8601 | زمان پایان تماس |
| **messages** | `messages[]` | array | آرایه پیام‌های مکالمه (اختیاری) |

### نکات مهم:

1. **`transcript`** معمولاً در `call.transcript` است
2. **`messages`** ممکن است موجود باشد (array of message objects)
3. **`call.id`** برای idempotency استفاده می‌شود
4. **`recordingUrl`** ممکن است موجود باشد (برای ذخیره‌سازی)

## 📝 نمونه‌های واقعی

### نمونه 1: ساده (فقط transcript)

```json
{
  "type": "end-of-call",
  "call": {
    "id": "call_123456",
    "transcript": "Checkout is down, 500 errors. Contact me amir@example.com"
  }
}
```

### نمونه 2: کامل (با messages)

```json
{
  "type": "end-of-call",
  "call": {
    "id": "call_789012",
    "status": "ended",
    "transcript": "User: Production API is completely down. All services offline. Started at 6 PM. About 1200 users affected. This is critical.\nAssistant: I understand. I'll create an incident report for you.",
    "startedAt": "2025-01-12T18:00:00Z",
    "endedAt": "2025-01-12T18:05:00Z",
    "duration": 300
  },
  "assistant": {
    "id": "asst_voiceops_001",
    "name": "VoiceOps Incident Reporter"
  },
  "messages": [
    {
      "role": "user",
      "content": "Production API is completely down"
    },
    {
      "role": "assistant",
      "content": "I understand. Can you tell me when this started?"
    },
    {
      "role": "user",
      "content": "Started at 6 PM. About 1200 users affected. This is critical."
    }
  ]
}
```

### نمونه 3: با PII (برای تست redaction)

```json
{
  "type": "end-of-call",
  "call": {
    "id": "call_pii_test",
    "transcript": "Patient John Doe, phone 555-1234, email john@example.com reported an issue in room 205. IP address is 192.168.1.1"
  }
}
```

## 🔧 Endpoint فعلی ما

Endpoint در `app/main.py` این ساختار را پشتیبانی می‌کند:

```python
# Extract transcript (flexible - supports multiple locations)
transcript = (
    (payload.call.transcript if payload.call else None) or  # Primary location
    payload.transcript or                                  # Root level fallback
    ""                                                     # Default
).strip()

# Extract call_id
call_id = (
    (payload.call.id if payload.call else None) or
    (payload.call.call_id if payload.call else None) or
    None
)
```

## ✅ تست با نمونه واقعی

### تست 1: ساختار ساده

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

### تست 2: ساختار کامل

```bash
curl -X POST http://localhost:8000/webhook/vapi \
  -H "Content-Type: application/json" \
  -d '{
    "type": "end-of-call",
    "call": {
      "id": "call_test_456",
      "status": "ended",
      "transcript": "Production API is completely down. All services offline. Started at 6 PM. About 1200 users affected. This is critical.",
      "startedAt": "2025-01-12T18:00:00Z",
      "endedAt": "2025-01-12T18:05:00Z"
    },
    "assistant": {
      "id": "asst_voiceops_001"
    }
  }'
```

## 🎯 خلاصه

**VAPI دقیقاً این payload را می‌فرستد:**

```json
{
  "type": "end-of-call",
  "call": {
    "id": "call_xxx",
    "transcript": "متن کامل transcript اینجا..."
  }
}
```

**Endpoint ما:**
- ✅ `call.transcript` را می‌خواند (primary)
- ✅ `transcript` در root level را هم پشتیبانی می‌کند (fallback)
- ✅ `call.id` را برای idempotency استفاده می‌کند

**همه چیز آماده است!** 🚀

