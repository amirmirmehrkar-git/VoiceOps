# LLM Prompt for Incident JSON Generation

**Purpose**: Convert unstructured incident reports (voice transcripts) into valid JSON that matches the incident schema.

---

## System Prompt

```
You are an incident-structuring engine. Convert unstructured incident reports into a STRICT JSON object that must validate against the provided JSON Schema.

Rules:

- Output MUST be valid JSON only (no markdown, no commentary).

- Follow the schema exactly: required fields must be present; no extra fields.

- If a value is unknown, still fill required fields using safe defaults:
  - category: "other"
  - severity: "sev3"
  - status: "new"
  - location.site: "unknown"
  - systems: [{"name":"unknown","environment":"unknown"}]
  - confidence: between 0.5 and 0.9 depending on clarity

- Do NOT include personal data. If the transcript contains names, phone numbers, patient identifiers, emails, addresses, set pii.contains_pii=true and redact them in summary/description.

- Title: 8–120 chars. Summary: 20–500 chars.

- occurred_at and reported_at must be ISO-8601 date-time strings. If occurred_at is unclear, set occurred_at = reported_at.

- Tags must be machine-friendly: lowercase letters/numbers/underscore/hyphen only.

- For "source.vendor" use "vapi" and "source.channel" use "voice" unless given otherwise.
```

---

## User Prompt Template

```
JSON Schema (for reference): <PASTE THE SCHEMA HERE OR PROVIDE IT AS A FILE>

Context:
- timezone: Europe/Berlin
- reported_at: {{NOW_ISO}}
- call_id: {{VAPI_CALL_ID}}

Transcript (verbatim):
{{TRANSCRIPT_TEXT}}

Task:
Return ONE JSON object that validates the schema.
```

---

## Example Usage

### Input (Transcript):
```
"We have a critical issue. The checkout API is down. Started around 6 PM. All payments are failing. About 1200 users affected. This is production."
```

### Expected Output:
```json
{
  "schema_version": "1.0.0",
  "source": {
    "channel": "voice",
    "vendor": "vapi",
    "call_id": "call_abc123"
  },
  "occurred_at": "2025-12-19T18:00:00+01:00",
  "reported_at": "2025-12-19T18:08:12+01:00",
  "timezone": "Europe/Berlin",
  "title": "Checkout API down - payments failing",
  "summary": "Checkout API is down since 6 PM. All payments failing. Approximately 1200 users affected in production environment.",
  "category": "service_outage",
  "severity": "sev1",
  "status": "new",
  "location": {
    "site": "unknown"
  },
  "systems": [
    {
      "name": "checkout-api",
      "environment": "prod"
    }
  ],
  "impact": {
    "users_affected_estimate": 1200,
    "services_down": true
  },
  "tags": ["checkout", "api", "payments", "prod"],
  "pii": {
    "contains_pii": false,
    "redaction_applied": false
  },
  "confidence": 0.85
}
```

---

## Validation Checklist

Before accepting LLM output:

- [ ] Valid JSON (parseable)
- [ ] All required fields present
- [ ] No extra fields (schema has `additionalProperties: false`)
- [ ] Enum values match schema
- [ ] String lengths within limits
- [ ] ISO-8601 timestamps valid
- [ ] Tags match pattern `^[a-z0-9_\\-]{2,32}$`
- [ ] Confidence between 0 and 1
- [ ] PII handling applied if needed

---

## Error Handling

If LLM output is invalid:

1. **Try again** with more explicit instructions
2. **Use fallback defaults** for missing required fields
3. **Log the error** for debugging
4. **Return error response** to caller

---

## Integration with VAPI

When using with VAPI:

1. Receive transcript from VAPI webhook
2. Extract `call_id` from VAPI metadata
3. Use current timestamp for `reported_at`
4. Pass transcript to LLM with this prompt
5. Validate output against schema
6. Store or forward validated incident

---

**Last Updated**: 2025-01-27

