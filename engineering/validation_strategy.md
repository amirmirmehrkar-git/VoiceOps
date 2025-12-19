# VoiceOps Validation Strategy

## Strict Schema Validation

### Step 1: JSON Schema Validation
- All incidents MUST pass `incident.v1.json` schema validation
- Invalid JSON is rejected immediately
- Missing required fields trigger error

### Step 2: Business Logic Validation
- Severity must match category (e.g., SECURITY → HIGH/CRITICAL)
- Timestamp must be recent (< 24 hours old)
- Incident ID must be unique
- Affected systems must exist in system catalog

### Step 3: Integration Validation
- Webhook URLs must be valid
- Jira project keys must exist
- PagerDuty service IDs must be valid

## Error Handling

### Validation Failures
1. **Schema Error**: Return error to user, request clarification
2. **Business Logic Error**: Auto-correct with warning log
3. **Integration Error**: Queue for retry, notify admin

### Retry Strategy
- 3 retries with exponential backoff
- Dead letter queue after 3 failures
- Admin notification on permanent failure

## Testing

### Unit Tests
- Schema validation tests
- Severity rule tests
- Category classification tests

### Integration Tests
- End-to-end voice → JSON → webhook
- Jira integration tests
- PagerDuty integration tests

### Table-Driven Tests
See `/coderabbit` for CodeRabbit-driven test strategy.

