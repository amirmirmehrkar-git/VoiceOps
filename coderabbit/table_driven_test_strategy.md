# Table-Driven Test Strategy

## Overview

Table-driven tests use data tables to test multiple scenarios with a single test function. This approach is recommended by CodeRabbit for comprehensive, maintainable testing.

## Example: Severity Classification Tests

```typescript
describe('Severity Classification', () => {
  const testCases = [
    {
      name: 'Critical - outage keywords',
      input: 'Service is down, all systems offline',
      expected: { severity: 'CRITICAL', priority: 'P0' }
    },
    {
      name: 'High - security breach',
      input: 'Security breach detected, unauthorized access',
      expected: { severity: 'HIGH', priority: 'P1' }
    },
    {
      name: 'Medium - performance issue',
      input: 'System is slow, some users affected',
      expected: { severity: 'MEDIUM', priority: 'P2' }
    },
    {
      name: 'Low - minor issue',
      input: 'Small UI bug, cosmetic issue',
      expected: { severity: 'LOW', priority: 'P3' }
    }
  ];

  testCases.forEach(({ name, input, expected }) => {
    it(`should classify ${name} correctly`, () => {
      const result = classifySeverity(input);
      expect(result.severity).toBe(expected.severity);
      expect(result.priority).toBe(expected.priority);
    });
  });
});
```

## Example: Schema Validation Tests

```typescript
describe('Incident Schema Validation', () => {
  const validCases = [
    {
      name: 'Complete valid incident',
      incident: {
        incident_id: 'INC-2025-001',
        timestamp: '2025-01-27T14:30:00Z',
        severity: 'HIGH',
        category: 'SECURITY',
        title: 'Test Incident',
        description: 'Test description',
        status: 'OPEN'
      }
    }
  ];

  const invalidCases = [
    {
      name: 'Missing required field',
      incident: {
        incident_id: 'INC-2025-001',
        // Missing timestamp
        severity: 'HIGH'
      },
      expectedError: 'timestamp is required'
    },
    {
      name: 'Invalid severity',
      incident: {
        incident_id: 'INC-2025-001',
        timestamp: '2025-01-27T14:30:00Z',
        severity: 'INVALID',
        category: 'SECURITY',
        title: 'Test',
        description: 'Test',
        status: 'OPEN'
      },
      expectedError: 'severity must be one of: LOW, MEDIUM, HIGH, CRITICAL'
    }
  ];

  validCases.forEach(({ name, incident }) => {
    it(`should validate ${name}`, () => {
      expect(() => validateIncident(incident)).not.toThrow();
    });
  });

  invalidCases.forEach(({ name, incident, expectedError }) => {
    it(`should reject ${name}`, () => {
      expect(() => validateIncident(incident)).toThrow(expectedError);
    });
  });
});
```

## Benefits

1. **Comprehensive Coverage**: Test many scenarios easily
2. **Maintainable**: Add new test cases by adding table rows
3. **Readable**: Test cases are self-documenting
4. **Efficient**: Single test function for multiple scenarios

## CodeRabbit Recommendations

CodeRabbit suggests using table-driven tests for:
- Severity classification rules
- Schema validation
- Category mapping
- Webhook payload generation
- Error handling scenarios

## Implementation

See `/engineering/severity_rules.md` for severity test cases.
See `/engineering/validation_strategy.md` for validation test cases.

