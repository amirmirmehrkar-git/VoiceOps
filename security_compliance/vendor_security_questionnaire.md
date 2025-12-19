# VoiceOps Vendor Security Questionnaire - Pre-Filled Answers

## Company Information

**Company Name**: VoiceOps Inc.
**Product/Service**: VoiceOps - Voice-to-Incident Conversion Platform
**Contact**: security@voiceops.com

## Security Program

### Q: Do you have a formal security program?
**A**: Yes. We follow SOC2-lite controls with documented security policies and procedures.

### Q: Who is responsible for security?
**A**: Designated Security Officer. Contact: security@voiceops.com

### Q: Do you have security certifications?
**A**: SOC2-lite currently. Full SOC2 Type II target: Q2 2025.

## Data Security

### Q: How is data encrypted?
**A**: 
- In transit: TLS 1.3
- At rest: AES-256
- Keys: AWS KMS managed

### Q: Where is data stored?
**A**: AWS US-East region. EU data residency available.

### Q: Who has access to customer data?
**A**: Only authorized personnel with business need. All access logged.

## Access Controls

### Q: How is access controlled?
**A**: 
- Multi-factor authentication required
- Role-based access control
- Principle of least privilege
- Regular access reviews

### Q: How are credentials managed?
**A**: 
- Password policy enforced
- MFA required
- No shared accounts
- Credentials rotated regularly

## Incident Response

### Q: What is your incident response process?
**A**: NIST-style process:
1. Detection and analysis
2. Containment
3. Eradication
4. Recovery
5. Post-incident review

### Q: How quickly do you respond to incidents?
**A**: 
- Critical: < 1 hour
- High: < 4 hours
- Medium: < 24 hours

### Q: Will you notify us of incidents?
**A**: Yes, per DPA requirements. Critical incidents within 72 hours.

## Vulnerability Management

### Q: How do you manage vulnerabilities?
**A**: 
- Regular vulnerability scanning
- Patch management process
- Third-party dependency monitoring
- Annual penetration testing

### Q: How quickly are critical vulnerabilities patched?
**A**: Critical: < 24 hours. High: < 7 days. Medium: < 30 days.

## Business Continuity

### Q: What is your uptime SLA?
**A**: 99.5% uptime (excluding scheduled maintenance).

### Q: What is your disaster recovery plan?
**A**: 
- Multi-region failover
- RTO: 4 hours
- RPO: 1 hour
- Regular DR testing

## Compliance

### Q: What compliance frameworks do you follow?
**A**: 
- SOC2-lite controls
- GDPR compliance
- CCPA compliance
- HIPAA-aligned (with BAA)

### Q: Do you have a DPA?
**A**: Yes. Data Processing Addendum available.

## Subprocessors

### Q: Who are your subprocessors?
**A**: 
- VAPI (voice processing)
- AWS (hosting)
- [List others]

### Q: How are subprocessors managed?
**A**: 
- Security reviews required
- DPAs in place
- Regular assessments
- Notification of changes

## Questions?

Contact: security@voiceops.com

