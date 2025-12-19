# مثال‌های استفاده از VAPI MCP در Cursor

بعد از setup VAPI MCP در Cursor، می‌توانید از این promptها استفاده کنید.

---

## 🎯 مثال‌های Prompt

### 1. ایجاد Assistant

**Prompt:**
```
How do I create a voice assistant with Vapi for VoiceOps incident reporting that asks exactly 4 questions in Persian?
```

**Expected Response:**
```python
from vapi_ai import VapiClient
import os

client = VapiClient(api_key=os.getenv("VAPI_API_KEY"))

# Load prompt
with open("engineering/vapi_agent_prompt_4questions.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

assistant = client.assistants.create({
    "name": "VoiceOps Incident Intake",
    "firstMessage": "سلام، من VoiceOps هستم. برای گزارش حادثه، لطفاً به ۴ سؤال من پاسخ دهید.",
    "model": {
        "provider": "openai",
        "model": "gpt-4o",
        "systemPrompt": system_prompt,
        "temperature": 0.3
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
    "serverUrl": os.getenv("VOICEOPS_WEBHOOK_URL", "http://localhost:8000/api/v1/vapi/webhook")
})
```

---

### 2. Webhook Handling

**Prompt:**
```
Show me a complete FastAPI webhook handler for Vapi that processes end-of-call reports and creates incidents
```

**Expected Response:**
```python
from fastapi import FastAPI, Request, HTTPException
from api.incident import create_incident_from_transcript
from api.schema import validate_incident_strict

app = FastAPI()

@app.post("/api/v1/vapi/webhook")
async def vapi_webhook(request: Request):
    try:
        webhook_data = await request.json()
        event_type = webhook_data.get("type")
        
        if event_type == "end-of-call-report":
            call = webhook_data.get("call", {})
            transcript = call.get("transcript", "")
            call_id = call.get("id")
            
            if not transcript:
                raise HTTPException(status_code=400, detail="No transcript in webhook")
            
            # Create incident
            incident = create_incident_from_transcript(
                transcript=transcript,
                call_id=call_id,
                timezone="Europe/Berlin"
            )
            
            # Validate
            validate_incident_strict(incident)
            
            return {
                "status": "success",
                "incident": incident
            }
        
        elif event_type == "conversation-update":
            # Handle real-time updates if needed
            return {"status": "received"}
        
        return {"status": "ignored", "event_type": event_type}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

### 3. Call Transfer

**Prompt:**
```
How do I transfer a Vapi call to a human agent?
```

**Expected Response:**
```python
# In webhook handler
if event_type == "function-call":
    function_name = webhook_data.get("functionCall", {}).get("name")
    
    if function_name == "transfer_to_human":
        # Transfer call
        return {
            "result": {
                "action": "transfer",
                "phoneNumber": "+1234567890"
            }
        }
```

---

### 4. Speech Updates (Real-time)

**Prompt:**
```
Show me how to handle real-time speech updates from Vapi webhooks
```

**Expected Response:**
```python
@app.post("/api/v1/vapi/webhook")
async def vapi_webhook(request: Request):
    webhook_data = await request.json()
    event_type = webhook_data.get("type")
    
    if event_type == "speech-update":
        transcript = webhook_data.get("transcript", "")
        call_id = webhook_data.get("call", {}).get("id")
        
        # Process real-time transcript
        # Could trigger early incident creation if critical keywords detected
        if any(keyword in transcript.lower() for keyword in ["emergency", "down", "critical"]):
            # Early incident creation
            incident = create_incident_from_transcript(
                transcript=transcript,
                call_id=call_id
            )
            return {"status": "early_incident", "incident": incident}
        
        return {"status": "received"}
```

---

### 5. Function Calls

**Prompt:**
```
Show me how to handle function calls in Vapi webhooks for VoiceOps
```

**Expected Response:**
```python
@app.post("/api/v1/vapi/webhook")
async def vapi_webhook(request: Request):
    webhook_data = await request.json()
    event_type = webhook_data.get("type")
    
    if event_type == "function-call":
        function_call = webhook_data.get("functionCall", {})
        function_name = function_call.get("name")
        parameters = function_call.get("parameters", {})
        
        if function_name == "create_incident":
            # Create incident from function call
            incident = {
                "title": parameters.get("title"),
                "category": parameters.get("category"),
                "severity": parameters.get("severity"),
                # ... other fields
            }
            return {"result": incident}
        
        elif function_name == "check_severity":
            # Check severity based on keywords
            from api.scoring import classify_severity
            severity = classify_severity(parameters, parameters.get("transcript", ""))
            return {"result": {"severity": severity}}
        
        return {"result": None}
```

---

### 6. Error Handling

**Prompt:**
```
Show me best practices for error handling in Vapi webhook handlers
```

**Expected Response:**
```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

@app.post("/api/v1/vapi/webhook")
async def vapi_webhook(request: Request):
    try:
        webhook_data = await request.json()
        
        # Validate webhook structure
        if not webhook_data.get("type"):
            raise HTTPException(status_code=400, detail="Missing event type")
        
        # Process based on event type
        event_type = webhook_data.get("type")
        
        if event_type == "end-of-call-report":
            return await handle_end_of_call(webhook_data)
        elif event_type == "conversation-update":
            return await handle_conversation_update(webhook_data)
        else:
            logger.warning(f"Unknown event type: {event_type}")
            return {"status": "ignored"}
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Webhook processing error: {e}", exc_info=True)
        # Return 200 to prevent Vapi from retrying
        return JSONResponse(
            status_code=200,
            content={"status": "error", "message": "Internal processing error"}
        )
```

---

## 💡 Tips برای استفاده بهتر

### 1. سؤالات دقیق بپرسید
✅ "How do I create a Vapi assistant with Persian language support and 4-question flow?"
❌ "How do I create assistant?"

### 2. درخواست مثال‌های کامل
✅ "Show me a complete FastAPI webhook handler with error handling"
❌ "Show me webhook"

### 3. مشخص کردن Requirements
✅ "Create a webhook handler that processes Vapi calls and creates incidents with PII redaction"
❌ "Create webhook"

---

## 🔗 منابع

- **VAPI Documentation**: https://docs.vapi.ai
- **VAPI MCP Setup**: `VAPI_MCP_CURSOR_SETUP.md`
- **Quick Start**: `QUICK_START.md`

---

**Last Updated**: 2025-01-27

