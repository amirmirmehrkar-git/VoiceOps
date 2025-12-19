# VoiceOps HIPAA Alignment

## Positioning

VoiceOps can be configured for HIPAA-aligned use cases in healthcare incident management.

## Key Considerations

### ✅ What We Do
- Encrypt all data (transit and at rest)
- Implement access controls
- Maintain audit logs
- Sign Business Associate Agreements (BAA)

### ⚠️ What We Don't Do
- We do NOT store Protected Health Information (PHI) by default
- We do NOT process medical records
- We do NOT provide medical advice

## Use Cases

### Appropriate Use
- IT incident reporting in healthcare
- System outage reporting
- Security incident reporting
- Non-PHI operational incidents

### Not Appropriate Use
- Patient data processing
- Medical record management
- Clinical decision support
- Direct patient care

## Technical Safeguards

- **Access Control**: Role-based access, MFA
- **Audit Controls**: Comprehensive logging
- **Integrity**: Data validation, checksums
- **Transmission Security**: TLS 1.3 encryption

## Administrative Safeguards

- **Security Officer**: Designated
- **Workforce Training**: Security awareness
- **Incident Response**: Documented procedures
- **Business Associate Agreements**: Available

## Physical Safeguards

- **Facility Controls**: AWS data centers (HIPAA-eligible)
- **Workstation Security**: Encrypted devices
- **Media Controls**: Encrypted storage

## BAA Availability

Business Associate Agreement (BAA) available for enterprise customers using VoiceOps in healthcare contexts.

## Compliance Disclaimer

VoiceOps is a technology platform. Healthcare customers are responsible for:
- Ensuring appropriate use
- Maintaining HIPAA compliance
- Obtaining necessary authorizations
- Proper data handling

**We recommend consulting with legal/compliance before using in healthcare contexts.**

