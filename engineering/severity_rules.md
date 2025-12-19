# VoiceOps Severity Rules

## Deterministic & Auditable Severity Classification

### CRITICAL (P0)
**Keywords:**
- "critical", "urgent", "emergency"
- "down", "broken", "not working"
- "all", "everyone", "complete failure"

**Examples:**
- "Payment system is down"
- "Critical security breach"
- "All services offline"

**Response Time:** Immediate (< 5 minutes)

---

### HIGH (P1)
**Keywords:**
- "high priority", "important"
- "significant impact"
- "many users affected"

**Examples:**
- "High priority security issue"
- "Significant performance degradation"
- "Many customers affected"

**Response Time:** < 15 minutes

---

### MEDIUM (P2)
**Keywords:**
- "medium", "moderate"
- "some users", "partial"
- "degraded performance"

**Examples:**
- "Moderate performance issue"
- "Some users experiencing problems"
- "Partial service degradation"

**Response Time:** < 1 hour

---

### LOW (P3)
**Keywords:**
- "low", "minor", "small"
- "cosmetic", "non-critical"
- "future enhancement"

**Examples:**
- "Minor UI issue"
- "Low priority bug"
- "Small performance improvement needed"

**Response Time:** < 4 hours

---

## Category Classification

### SECURITY
- Keywords: "security", "breach", "hack", "unauthorized", "vulnerability"
- Auto-escalate to HIGH or CRITICAL

### OUTAGE
- Keywords: "down", "outage", "offline", "not working", "broken"
- Auto-escalate to CRITICAL or HIGH

### PERFORMANCE
- Keywords: "slow", "performance", "lag", "timeout", "degraded"
- Usually MEDIUM or HIGH

### DATA
- Keywords: "data", "corruption", "loss", "backup", "restore"
- Usually HIGH or CRITICAL

---

## Audit Trail

All severity decisions are logged with:
- Source keywords detected
- Confidence score
- Override reason (if manual)
- Timestamp

This ensures full auditability for SOC2 compliance.

