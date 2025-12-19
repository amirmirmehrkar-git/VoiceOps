# Example PR Titles & Commit Messages

## PR Titles (CodeRabbit Style)

### Feature PRs
- `feat: Add voice-to-JSON incident conversion`
- `feat: Implement severity classification rules`
- `feat: Add Jira webhook integration`
- `feat: Support PagerDuty incident creation`

### Fix PRs
- `fix: Correct severity mapping for security incidents`
- `fix: Handle missing timestamp in voice input`
- `fix: Retry logic for failed webhook deliveries`

### Refactor PRs
- `refactor: Extract severity rules to separate module`
- `refactor: Improve schema validation error messages`
- `refactor: Optimize webhook delivery queue`

### Security PRs
- `security: Add input sanitization for voice transcripts`
- `security: Encrypt transcript storage`
- `security: Implement rate limiting for API`

### Test PRs
- `test: Add table-driven tests for severity rules`
- `test: Integration tests for Jira webhook`
- `test: E2E test for voice-to-incident flow`

## Commit Messages

### Good Examples
```
feat: Add voice-to-JSON conversion with VAPI

- Integrate VAPI agent for voice processing
- Implement JSON schema validation
- Add error handling for invalid inputs
- Update documentation

Closes #123
```

```
fix: Correct severity classification for outages

Previously, outages were classified as HIGH instead of CRITICAL.
Now correctly maps "down" and "outage" keywords to CRITICAL.

Fixes #456
```

### Bad Examples (Avoid)
- "Fixed bug"
- "Updated code"
- "Changes"
- "WIP"

## CodeRabbit Recommendations

CodeRabbit suggests:
- Use conventional commits format
- Include issue numbers
- Write descriptive commit messages
- Keep commits focused and atomic

