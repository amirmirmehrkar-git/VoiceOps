# VoiceOps Demo Flow (90 seconds)

## 🎬 Live Demo Script

### Opening (5s)
"VoiceOps transforms voice reports into production-ready incidents. Watch this."

### Step 1: Voice Input (15s)
- User calls or speaks: "We have a security breach. Unauthorized access detected at 2:30 PM. Affecting user database. High priority."
- **Show**: Voice waveform / transcription appearing in real-time

### Step 2: AI Processing (20s)
- **Show**: VAPI agent processing
- **Show**: Structured JSON being generated
- **Highlight**: Schema validation passing

### Step 3: Output Display (20s)
- **Show**: Final JSON incident
- **Highlight**: 
  - Severity: HIGH
  - Category: SECURITY
  - All required fields populated
  - Timestamp accurate

### Step 4: Integration (20s)
- **Show**: Webhook delivery to Jira
- **Show**: Ticket created automatically
- **Show**: PagerDuty alert triggered

### Closing (10s)
"That's VoiceOps. Voice in. Production incidents out. Ready for pilots."

## 📦 Offline Backup Demo

If live demo fails:

1. **Show** `demo_incident.json` - Pre-generated output
2. **Show** `demo_transcript_security.txt` - Input transcript
3. **Walk through** schema validation
4. **Show** Jira webhook payload

## 🎯 Key Points to Emphasize

- ✅ **Speed**: 90 seconds from voice to ticket
- ✅ **Accuracy**: Schema-validated, no manual editing
- ✅ **Integration**: Works with existing tools
- ✅ **Enterprise-ready**: SOC2, HIPAA considerations

## 🐛 Troubleshooting

- **If VAPI fails**: Use offline JSON
- **If webhook fails**: Show payload structure
- **If audio fails**: Use transcript file

