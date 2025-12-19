# VoiceOps Security FAQ

## General Security

### Q: How is voice data secured?
**A**: All voice data is encrypted in transit (TLS 1.3) and at rest (AES-256). Transcripts are stored encrypted and access is logged.

### Q: Where is data stored?
**A**: Data is stored in AWS US-East region. EU data residency available for enterprise customers.

### Q: Who has access to my data?
**A**: Only authorized VoiceOps personnel with business need. All access is logged and audited.

## Compliance

### Q: Is VoiceOps SOC2 certified?
**A**: We follow SOC2-lite controls and are working toward full SOC2 Type II certification (target: Q2 2025).

### Q: Is VoiceOps HIPAA compliant?
**A**: VoiceOps can be configured for HIPAA-aligned use cases. BAA available for enterprise customers.

### Q: GDPR compliance?
**A**: Yes. We comply with GDPR requirements including data subject rights, breach notification, and data processing agreements.

## Data Processing

### Q: How long is data retained?
**A**: Active data retained for service duration. Backup data retained 30 days. Deletion available upon request.

### Q: Can I export my data?
**A**: Yes. Full data export available in JSON format. Available within 30 days of request.

### Q: What happens to data after contract termination?
**A**: Data is securely deleted after 30-day retention period. Export available during retention.

## Integrations

### Q: How are webhooks secured?
**A**: Webhooks use HTTPS with signature verification. API keys required for all integrations.

### Q: What data is sent to Jira/PagerDuty?
**A**: Only incident data (title, description, severity, etc.). No voice recordings or transcripts sent.

### Q: Can I use on-premise integrations?
**A**: Yes, for enterprise customers. VPN or private network options available.

## Incident Response

### Q: What is your incident response process?
**A**: We follow NIST-style incident response:
1. Detection
2. Analysis
3. Containment
4. Eradication
5. Recovery
6. Post-incident review

### Q: How quickly do you respond to security incidents?
**A**: Critical: < 1 hour. High: < 4 hours. Medium: < 24 hours.

### Q: Will you notify us of security incidents?
**A**: Yes, per DPA requirements. Critical incidents notified within 72 hours.

## Vendor Security

### Q: Can you complete our vendor security questionnaire?
**A**: Yes. See `vendor_security_questionnaire.md` for pre-filled answers.

### Q: Do you have penetration testing?
**A**: Yes, annual third-party penetration testing. Results available under NDA.

### Q: What is your business continuity plan?
**A**: 99.5% uptime SLA. Multi-region failover. RTO: 4 hours. RPO: 1 hour.
