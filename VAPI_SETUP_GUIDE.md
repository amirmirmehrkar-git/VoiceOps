# VAPI Setup Guide for VoiceOps

**API Key**: ✅ Configured  
**VAPI CLI**: ✅ Installed (v0.2.1)

---

## 🔑 API Key Setup

### ✅ Keys Configured

**Private API Key** (Server-side): `ff8c3bb0-6b6f-4f24-82fc-11a48c82d82f`  
**Public API Key** (Client-side): `88bf5220-9b1e-4ca8-8c73-09bbd9c11eed`

### Current Session (PowerShell)
```powershell
$env:VAPI_API_KEY = "ff8c3bb0-6b6f-4f24-82fc-11a48c82d82f"
$env:VAPI_PUBLIC_KEY = "88bf5220-9b1e-4ca8-8c73-09bbd9c11eed"
```

### Permanent Setup (User Environment) ✅ DONE
```powershell
[Environment]::SetEnvironmentVariable("VAPI_API_KEY", "ff8c3bb0-6b6f-4f24-82fc-11a48c82d82f", "User")
[Environment]::SetEnvironmentVariable("VAPI_PUBLIC_KEY", "88bf5220-9b1e-4ca8-8c73-09bbd9c11eed", "User")
```

**Note**: Keys are now permanently set. Restart terminal to use in new sessions.

### Test Connection
```powershell
python scripts/test_vapi_connection.py
```

---

## 🎙️ Create VoiceOps Assistant

### Option 1: Using VAPI Dashboard
1. Go to: https://dashboard.vapi.ai
2. Create new Assistant
3. Use prompt from: `engineering/vapi_agent_prompt_4questions.txt`

### Option 2: Using VAPI CLI
```powershell
# Login (if not already)
vapi login

# Create assistant from config
vapi assistant create --config assistant-config.json
```

### Option 3: Using API (PowerShell)
```powershell
$headers = @{
    'Authorization' = 'Bearer ff8c3bb0-6b6f-4f24-82fc-11a48c82d82f'
    'Content-Type' = 'application/json'
}

$body = @{
    name = "VoiceOps Incident Intake"
    firstMessage = "سلام، من VoiceOps هستم. برای گزارش حادثه، لطفاً به ۴ سؤال من پاسخ دهید."
    model = @{
        provider = "openai"
        model = "gpt-4o"
        messages = @(
            @{
                role = "system"
                content = (Get-Content engineering/vapi_agent_prompt_4questions.txt -Raw)
            }
        )
    }
    voice = @{
        provider = "vapi"
        voiceId = "Elliot"
    }
    transcriber = @{
        provider = "deepgram"
        model = "nova-3"
        language = "fa"
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri 'https://api.vapi.ai/assistant' -Method Post -Headers $headers -Body $body
```

---

## 📋 Assistant Configuration

### Key Settings for VoiceOps:

1. **Name**: "VoiceOps Incident Intake"
2. **First Message**: "سلام، من VoiceOps هستم. برای گزارش حادثه، لطفاً به ۴ سؤال من پاسخ دهید."
3. **System Prompt**: Use `engineering/vapi_agent_prompt_4questions.txt`
4. **Voice**: Elliot (or any professional voice)
5. **Language**: Persian (fa) or English
6. **Model**: gpt-4o (for best JSON output)

---

## 🔗 Webhook Setup

After creating assistant, configure webhook:

1. **Webhook URL**: Your API endpoint (e.g., `https://your-api.com/vapi/webhook`)
2. **Events**: 
   - `end-of-call-report` - Get transcript
   - `function-call` - If using functions
   - `conversation-update` - Track conversation

---

## 🧪 Testing

### Test Call
```powershell
# Make a test call
vapi call create --assistant-id YOUR_ASSISTANT_ID --phone-number YOUR_PHONE
```

### Check Logs
```powershell
# View call logs
vapi call list
```

---

## 📝 Next Steps

1. ✅ VAPI CLI installed
2. ✅ API key configured
3. ⚠️ Create VoiceOps assistant (use prompt from `engineering/vapi_agent_prompt_4questions.txt`)
4. ⚠️ Configure webhook endpoint
5. ⚠️ Test with demo scenarios

---

## 🔗 Resources

- **VAPI Dashboard**: https://dashboard.vapi.ai
- **VAPI Docs**: https://docs.vapi.ai
- **VoiceOps Prompt**: `engineering/vapi_agent_prompt_4questions.txt`

---

**Last Updated**: 2025-01-27

