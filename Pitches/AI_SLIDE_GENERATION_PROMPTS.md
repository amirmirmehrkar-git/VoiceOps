# 🎯 VoiceOps - AI Slide Generation Prompts

**Ready-to-use prompts for creating pitch decks with AI tools**

**Compatible with**: Copilot, Gamma, Tome, Canva AI, Beautiful.ai, PowerPoint AI, ChatGPT → PPT

---

## 📋 Quick Start Guide

### Step 1: Main Deck
Use **PROMPT 1** to create your 6-slide main pitch deck.

### Step 2: Backup Slides
Use **PROMPT 3-7** separately to create backup slides.

### Step 3: Emergency Pitch
Use **PROMPT 2** if you need a quick 25-second pitch.

---

## 🧠 PROMPT 1 — Main Pitch Deck (6 Slides)

**Goal**: Main deck for hackathon judging / demo

**Copy this prompt**:

```
Create a clean, professional 6-slide pitch deck for a B2B SaaS product called "VoiceOps".

Audience: technical judges, DevOps, healthcare and security professionals.
Tone: clear, minimal, production-focused. No buzzwords.

Slides:

1. Title
   - Product name: VoiceOps
   - Tagline: "Voice-first incident ingestion. Production-ready by design."

2. Problem
   - Incident reporting fails under pressure
   - Forms are skipped, severity is wrong, response is slow
   - One strong sentence: "Typing fails when time matters most."

3. Solution
   - Voice-based incident intake
   - Exactly 4 structured questions
   - Deterministic severity (sev1–sev4)
   - No raw transcripts stored

4. How It Works
   - Voice input → structured JSON
   - Strict schema validation
   - Ready for Jira / PagerDuty / SIEM

5. Why It's Production-Ready
   - Schema-first design
   - PII redaction
   - Deterministic rules (not AI guessing)
   - Built with security and reliability in mind

6. Vision
   - Incident ingestion as infrastructure
   - One core system → multiple industries
```

---

## 🚨 PROMPT 2 — 25-Second Emergency Pitch (1 Slide)

**Goal**: When time is short or judge is in a hurry

**Copy this prompt**:

```
Create a single-slide emergency pitch for a product called VoiceOps.

Content:
- One sentence problem
- One sentence solution
- One sentence differentiation

Constraints:
- Max 40 words total
- Large readable font
- Suitable for a 25-second spoken pitch

Tone: confident, technical, credible.
```

---

## 🧰 PROMPT 3 — Backup Slides: Architecture & Engineering

**Goal**: Backup slides for technical judges / Daytona

**Copy this prompt**:

```
Create 3 backup slides explaining the technical architecture of VoiceOps.

Audience: senior engineers, infrastructure judges.

Slides:

1. Architecture Overview
   - Voice intake (VAPI)
   - Structured output
   - Validation layer
   - Integrations

2. Severity Logic
   - Deterministic rules
   - Conservative escalation
   - No AI decision-making

3. Failure Handling
   - Invalid AI output fallback
   - Idempotency via call_id
   - Retry and backoff strategy

Style:
- Simple diagrams
- Bullet points
- No marketing language
```

---

## 🐰 PROMPT 4 — Backup Slides: CodeRabbit (Rabbit Hole)

**Goal**: Specifically for Rabbit Hole prize

**Copy this prompt**:

```
Create 2 backup slides showing how CodeRabbit was used in this project.

Audience: CodeRabbit judges and technical reviewers.

Slides:

1. How CodeRabbit Helped
   - Security review
   - Schema validation improvements
   - Test coverage suggestions

2. Concrete Impact
   - PII risks identified
   - Validation enforced
   - Table-driven tests added

Include:
- Emphasis on production-readiness
- Focus on real code changes, not just usage
```

---

## 🔐 PROMPT 5 — Backup Slides: Security & Compliance

**Goal**: Security questions / healthcare / enterprise

**Copy this prompt**:

```
Create 3 backup slides focused on security and compliance for VoiceOps.

Audience: healthcare, security, enterprise judges.

Slides:

1. Data Minimization
   - Only 4 intake questions
   - No raw transcript storage
   - PII redaction at intake

2. Compliance Mindset
   - SOC2-aligned controls
   - HIPAA-style data minimization
   - Audit-friendly incident records

3. Trust Statement
   - AI structures data, does not decide
   - Deterministic and auditable behavior

Tone:
- Calm
- Trustworthy
- Enterprise-ready
```

---

## 💰 PROMPT 6 — Backup Slides: Business & Pricing

**Goal**: If judge asks "Who buys this?"

**Copy this prompt**:

```
Create 2 backup slides explaining the business model of VoiceOps.

Slides:

1. Ideal Customer Profile
   - Teams that own incidents
   - DevOps, healthcare ops, security teams
   - High-pressure environments

2. Pricing
   - Per-team SaaS pricing
   - Pilot → paid conversion
   - Comparable to PagerDuty add-ons

Style:
- Very simple
- No aggressive sales language
```

---

## 🎯 PROMPT 7 — "Questions from Judges" Slide

**Goal**: End of deck or backup

**Copy this prompt**:

```
Create a final backup slide titled "Questions We Expect".

Include short answers to:
- Is AI deciding severity?
- How do you handle PII?
- Why voice instead of forms?
- How is this production-ready?

Answers must be one sentence each.
```

---

## 🎨 Golden Closing Line

**Use this on your final slide**:

> "We fix the first incident report — everything downstream depends on it."

---

## 📝 Usage Instructions

### Method 1: Step-by-Step (Recommended)

1. **Start with PROMPT 1**
   - Create main 6-slide deck
   - Review and adjust

2. **Add Backup Slides**
   - Run PROMPT 3 → Architecture slides
   - Run PROMPT 4 → CodeRabbit slides
   - Run PROMPT 5 → Security slides
   - Run PROMPT 6 → Business slides
   - Run PROMPT 7 → Q&A slide

3. **Organize**
   - Main deck: Slides 1-6
   - Backup slides: After main deck (can be hidden)
   - Emergency pitch: Keep separate or as slide 0

### Method 2: All-in-One

Copy all prompts into one request (for tools that support multi-slide generation).

---

## 🛠️ Tool-Specific Tips

### For Gamma / Tome:
- Use one prompt at a time
- Let AI generate visuals automatically
- Review and refine

### For PowerPoint AI / Copilot:
- Paste prompt in "Design Ideas" or "Create with AI"
- Adjust layout manually if needed

### For ChatGPT → PPT:
- Use detailed prompts
- Request specific slide layouts
- Export to PowerPoint format

### For Canva AI / Beautiful.ai:
- Use shorter prompts
- Focus on content, not structure
- Let tool handle design

---

## ✅ Checklist

Before presenting:

- [ ] Main deck (6 slides) created
- [ ] Backup slides ready (Architecture, CodeRabbit, Security, Business, Q&A)
- [ ] Emergency pitch slide prepared
- [ ] Golden closing line added
- [ ] All slides reviewed for accuracy
- [ ] Backup slides marked as "hidden" (optional)
- [ ] Tested on screen/projector

---

## 🎯 Key Messages to Emphasize

### Always Include:
1. **"Voice is the input. Production-grade incidents are the output."**
2. **"We fix the first incident report — everything downstream depends on it."**
3. **Deterministic severity (not AI guessing)**
4. **Production-ready from day one**

### Avoid:
- ❌ Buzzwords
- ❌ Over-promising
- ❌ Complex diagrams
- ❌ Marketing fluff

---

## 📊 Slide Count Summary

| Deck Type | Slides | Purpose |
|-----------|--------|---------|
| Main Deck | 6 | Primary presentation |
| Architecture | 3 | Technical backup |
| CodeRabbit | 2 | Rabbit Hole prize |
| Security | 3 | Compliance backup |
| Business | 2 | Pricing backup |
| Q&A | 1 | Judge questions |
| Emergency | 1 | Quick pitch |
| **TOTAL** | **18** | Complete deck |

---

## 🚀 Quick Reference

**Main Deck**: PROMPT 1 (6 slides)  
**Emergency**: PROMPT 2 (1 slide)  
**Backup**: PROMPT 3-7 (11 slides)  
**Total**: 18 slides

**Golden Line**: "We fix the first incident report — everything downstream depends on it."

---

**Last Updated**: 2025-01-27  
**Status**: ✅ Ready to use with any AI slide generation tool

