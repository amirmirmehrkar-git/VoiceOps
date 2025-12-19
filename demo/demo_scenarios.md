# VoiceOps Demo Scenarios

**Ready-to-use transcripts and expected JSON outputs for demos**

---

## 1️⃣ Scenario: Clear Outage (sev1)

### Transcript (Persian)
```
سلام، از ساعت ۱۸:۰۵ بعد از دیپلوی جدید، checkout-api توی پروداکشن ۵۰۰ می‌دهد. 
مشتری‌ها نمی‌تونن پرداخت کنن. فکر کنم دیتابیس payments timeout می‌ده. 
لطفاً فوری رسیدگی کنید.
```

### Expected JSON Output
```json
{
  "schema_version": "1.0.0",
  "source": {
    "channel": "voice",
    "vendor": "vapi",
    "call_id": "call_demo_outage_001"
  },
  "occurred_at": "2025-12-19T18:05:00+01:00",
  "reported_at": "2025-12-19T18:08:00+01:00",
  "timezone": "Europe/Berlin",
  "title": "Checkout API returning 500 errors in production",
  "summary": "After a new deploy, checkout-api in production is returning HTTP 500 and customers cannot complete payments. Payments database timeouts are suspected and immediate triage is needed.",
  "category": "service_outage",
  "severity": "sev1",
  "status": "new",
  "location": {
    "site": "unknown"
  },
  "systems": [
    {
      "name": "checkout-api",
      "component": "payments",
      "environment": "prod"
    }
  ],
  "impact": {
    "services_down": true,
    "users_affected_estimate": 0
  },
  "evidence": {
    "error_codes": ["HTTP_500", "DB_TIMEOUT"]
  },
  "tags": ["prod", "checkout", "payments"],
  "pii": {
    "contains_pii": false,
    "redaction_applied": false
  },
  "confidence": 0.88
}
```

### Severity Reasoning
- **sev1** because: `services_down=true` + keywords "500", "down", "cannot"

---

## 2️⃣ Scenario: Ambiguous Report (defaults → sev3)

### Transcript (Persian)
```
یه مشکلی هست… بعضی وقتا سیستم کند می‌شه، دقیق نمی‌دونم از کی شروع شده. 
فعلاً فقط چند نفر گفتن صفحه دیر لود می‌شه.
```

### Expected JSON Output
```json
{
  "schema_version": "1.0.0",
  "source": {
    "channel": "voice",
    "vendor": "vapi",
    "call_id": "call_demo_ambiguous_001"
  },
  "occurred_at": "2025-12-19T18:20:00+01:00",
  "reported_at": "2025-12-19T18:20:00+01:00",
  "timezone": "Europe/Berlin",
  "title": "Intermittent slowness reported by some users",
  "summary": "Some users report that pages load slowly at times, but the start time and affected components are unclear. Further triage is required to identify scope and root cause.",
  "category": "performance_degradation",
  "severity": "sev3",
  "status": "new",
  "location": {
    "site": "unknown"
  },
  "systems": [
    {
      "name": "unknown",
      "environment": "unknown"
    }
  ],
  "tags": ["performance", "slow"],
  "pii": {
    "contains_pii": false,
    "redaction_applied": false
  },
  "confidence": 0.62
}
```

### Severity Reasoning
- **sev3** (default) because: unclear scope, no critical keywords, low user impact

---

## 3️⃣ Scenario: Contains PII (Redaction + Flags)

### Transcript (Persian - Contains PII)
```
من علی رضایی هستم، شماره‌ام ۰۹۱۲۳۴۵۶۷۸۹. 
بیمار آقای محمدی توی اتاق ۳۱۲ بعد از قطع شدن مانیتور علائم حیاتی، 
چند دقیقه بدون ثبت ضربان بود. لطفاً سریع پیگیری کنید.
```

### Expected JSON Output
```json
{
  "schema_version": "1.0.0",
  "source": {
    "channel": "voice",
    "vendor": "vapi",
    "call_id": "call_demo_pii_001"
  },
  "occurred_at": "2025-12-19T18:30:00+01:00",
  "reported_at": "2025-12-19T18:31:00+01:00",
  "timezone": "Europe/Berlin",
  "title": "Vital signs monitor interruption with potential patient safety risk",
  "summary": "A vital signs monitoring interruption was reported with potential patient safety impact. Reporter and patient identifiers were removed as [REDACTED]. Immediate triage and safety review are required.",
  "category": "patient_safety",
  "severity": "sev1",
  "status": "new",
  "location": {
    "site": "unknown",
    "room": "312"
  },
  "systems": [
    {
      "name": "vital-signs-monitor",
      "environment": "unknown"
    }
  ],
  "impact": {
    "patient_safety_risk": true,
    "services_down": false,
    "users_affected_estimate": 1
  },
  "tags": ["patient_safety", "monitoring"],
  "pii": {
    "contains_pii": true,
    "redaction_applied": true
  },
  "confidence": 0.8
}
```

### Severity Reasoning
- **sev1** because: `category=patient_safety` + `patient_safety_risk=true` + critical keywords

### PII Handling
- Names redacted: "علی رضایی" → "[REDACTED]"
- Phone redacted: "۰۹۱۲۳۴۵۶۷۸۹" → "[REDACTED]"
- Patient name redacted: "آقای محمدی" → "[REDACTED]"
- Flags set: `pii.contains_pii=true`, `pii.redaction_applied=true`

---

## 4️⃣ Scenario: Security Incident (sev1)

### Transcript (Persian)
```
یک لاگین مشکوک شناسایی شد. کاربر admin از IP غیرمعمول وارد شده. 
احتمال نشت توکن وجود داره. باید فوری بررسی بشه.
```

### Expected JSON Output
```json
{
  "schema_version": "1.0.0",
  "source": {
    "channel": "voice",
    "vendor": "vapi",
    "call_id": "call_demo_security_001"
  },
  "occurred_at": "2025-12-19T18:15:00+01:00",
  "reported_at": "2025-12-19T18:16:00+01:00",
  "timezone": "Europe/Berlin",
  "title": "Suspicious login detected with potential token leak",
  "summary": "Suspicious admin login from unusual IP detected. Potential token leak suspected. Immediate security review and investigation required.",
  "category": "security_incident",
  "severity": "sev1",
  "status": "new",
  "location": {
    "site": "unknown"
  },
  "systems": [
    {
      "name": "authentication-service",
      "environment": "prod"
    }
  ],
  "impact": {
    "users_affected_estimate": 0
  },
  "tags": ["security", "authentication", "suspicious_login"],
  "pii": {
    "contains_pii": false,
    "redaction_applied": false
  },
  "confidence": 0.85
}
```

### Severity Reasoning
- **sev1** because: `category=security_incident` (always sev1)

---

## 📊 Summary

| Scenario | Category | Severity | PII | Confidence |
|----------|----------|----------|-----|-------------|
| Outage | service_outage | sev1 | No | 0.88 |
| Ambiguous | performance_degradation | sev3 | No | 0.62 |
| PII | patient_safety | sev1 | Yes | 0.80 |
| Security | security_incident | sev1 | No | 0.85 |

---

**Last Updated**: 2025-01-27

