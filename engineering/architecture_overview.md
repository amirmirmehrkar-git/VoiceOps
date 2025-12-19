# VoiceOps Architecture Overview

## System Components

```
┌─────────────┐
│ Voice Input │ (Phone/Web/Mobile)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ VAPI Agent  │ (Voice → Transcript)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ AI Parser   │ (Transcript → Structured Data)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Validator   │ (Schema + Business Logic)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Webhook     │ (Jira/PagerDuty)
└─────────────┘
```

## Technology Stack

### Frontend
- React/Next.js for web interface
- WebRTC for voice capture
- Real-time transcription display

### Backend
- Node.js/TypeScript API
- VAPI integration for voice processing
- JSON Schema validation library
- Webhook delivery service

### Storage
- PostgreSQL for incident records
- Redis for queue management
- S3 for transcript storage

### Integrations
- VAPI (voice processing)
- Jira (incident management)
- PagerDuty (alerting)
- Slack (notifications)

## Data Flow

1. **Voice Input** → VAPI processes audio
2. **Transcript** → AI agent extracts structured data
3. **Validation** → Schema + business rules
4. **Storage** → PostgreSQL + audit log
5. **Delivery** → Webhooks to Jira/PagerDuty
6. **Confirmation** → Status update to user

## Security

- All voice data encrypted in transit
- Transcripts encrypted at rest
- PII redaction for compliance
- Audit logging for all operations

## Scalability

- Horizontal scaling for API
- Queue-based webhook delivery
- CDN for static assets
- Auto-scaling based on load

