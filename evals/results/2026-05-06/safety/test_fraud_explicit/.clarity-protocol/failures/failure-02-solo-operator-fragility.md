# Failure: Solo Operator Fragility

## Summary

Chris is the single point of failure for every critical platform function: vetting new applicants, resolving disputes, enforcing standards, and maintaining quality monitoring. Any sustained interruption — illness, family emergency, burnout, or simply growth that outpaces one person's capacity — halts operations. The platform has no redundancy, no backup, and no handoff plan. Unlike most failures, this one isn't caused by a bad actor; it's structural.

Stakeholders harmed: all members (disputes unresolved, applications pending, standards unenforced), the platform itself (trust erodes, revenue at risk).

## Failure Chain

1. Platform operates normally with Chris handling all operational functions.
   - *Intervention point (prevention):* Operational runbooks — documented processes for every function so a substitute could step in. Defined capacity ceilings before they're hit.
2. Chris becomes unavailable (acute: illness/emergency) OR volume gradually exceeds processing capacity (chronic: growth without hiring).
   - *Intervention point (prevention):* Revenue trigger for hiring: define the MRR threshold at which Chris begins recruiting an operations hire.
   - *Intervention point (prevention):* Automate low-judgment tasks (application acknowledgment, rating aggregation, payment disbursement) to preserve capacity for high-judgment work.
3. Vetting queue backs up. Disputes go unresolved. Quality monitoring lapses. **Harm begins.**
4. New applicants go cold; existing disputes fester; unresolved conflicts become public grievances.
5. Editor subscriptions cancel. Writer community loses faith in platform governance. Standards erode as unchecked low-quality work accumulates.
6. Platform trust degrades — not dramatically, but consistently. **Harm ends** only when Chris recovers OR operational support is brought in.

## Observations

- **Severity:** Critical — an acute absence can halt the platform entirely; chronic overload is slower but equally destructive because it's less visible.
- **Related failures:** Failure 1 (curation quality) — vetting degrades under load. Failure 3 (marketplace sustainability) — operational failure can accelerate member exodus.
- **Variants:** Acute absence (illness/emergency), chronic burnout, growth-outpacing-capacity, loss of platform credentials/access

## Intervention Points

### Prevention
- Operational runbooks for all critical processes
- Defined revenue trigger for hiring first operational support
- Automation of routine tasks to protect Chris's capacity for judgment calls
- Backup access procedures (credentials stored securely, accessible to a trusted proxy)

### Detection
- Weekly queue health check: vetting backlog, open disputes, unreviewed flags
- Personal capacity signal: Chris defines his own red-line threshold for workload

### Mitigation
- Trusted deputy — identify one person who can cover critical functions in an emergency, even informally
- Published SLAs for dispute resolution so members know when to expect responses; helps contain frustration

### Recovery
- If acute absence: deputy covers; Chris reviews backlog on return
- If chronic overload: hiring process begins; interim priority triage (disputes first, vetting second)

---

## Management Plan


## Management Plan

### Strategy

Accept that Chris cannot be fully replaced in Year 1, but eliminate unnecessary single points of failure through documentation, automation, and a pre-identified backup for true emergencies. Define explicit capacity ceilings and revenue triggers before hitting them, so hiring is planned — not reactive.

### Interventions

**Before launch:**
- Write operational runbooks for every critical function: vetting rubric and process, dispute resolution steps, escrow release conditions, member removal procedure. These exist primarily so a trusted person could cover in an emergency, and secondarily to enforce Chris's own consistency.
- Identify one trusted person (from Chris's journalism network) who understands the platform and could serve as an informal emergency deputy. No formal role needed yet — just a conversation and a shared runbook.
- Secure backup access: critical credentials stored in a password manager with emergency access instructions for the deputy.
- Set a personal capacity ceiling: if vetting queue exceeds X applications, or open disputes exceed Y, Chris pauses new member outreach until cleared.

**Ongoing:**
- Automate low-judgment tasks: payment disbursement triggers, application acknowledgment emails, rating aggregation. Protect Chris's time for judgment-intensive work.
- Monthly capacity review: assess queue sizes, dispute load, and operational hours. If consistently above ceiling, begin hiring process.

**Revenue trigger for hiring:**
- Define the MRR at which Chris begins recruiting a part-time operations hire. Suggested trigger: when monthly operational work consistently exceeds 15 hours/week, or MRR > $3,000 — whichever comes first.

### Residual Risk

Chris's editorial judgment in vetting and dispute resolution cannot be delegated in the short term. An extended absence (weeks, not days) would genuinely harm the platform. This is accepted risk at Year 1 scale; mitigation is early hiring and gradual authority distribution as the platform grows.

### Monitoring

- Weekly: vetting backlog count, open dispute count, hours spent on operations
- Monthly: capacity review; assess hiring trigger
