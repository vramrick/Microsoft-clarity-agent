# Churn Research Program

## Approach

A four-workstream parallel research program designed to test three leading churn hypotheses and produce a defensible churn plan for annual planning within 6 weeks. Workstreams are designed to corroborate or contradict each other — findings that appear in both quantitative data and qualitative interviews carry more weight than either alone.

## Hypotheses Under Test

| Hypothesis | Decision if confirmed | Rigor required |
|---|---|---|
| Onboarding friction (no dedicated implementation → lower activation → churn) | Headcount ask: implementation specialist, or reallocation of who gets the resource | Rate differential with a number |
| Value realization gap (core workflow features never adopted → no perceived ROI → churn) | Playbook and coverage model changes | Clean enough to act on |
| Competitive pricing displacement | Escalation to CEO/sales — not CS's decision to make | Enough to raise credibly |

## Workstreams

### WS1: Cohort & Usage Analysis
*Owner: Analytics partner | Weeks 1–3*

Deliverable: A table showing churn rate by implementation-resource status, feature adoption curves for churned vs. retained cohorts, and a segmentation cut by size band and vertical.

Spec:
- Pull all 40 churned accounts + a matched retained cohort (same size band, same acquisition vintage, same vertical where possible)
- Primary split: accounts that received dedicated implementation resource vs. those that didn't. Calculate churn rates for each group.
- Feature adoption: for churned accounts, which core workflow features had <X% of users active at 60 and 90 days? Compare to retained cohort.
- Time-to-churn distribution: does churn concentrate at first renewal? Second? Does this differ by implementation resource status?
- Segmentation: is churn rate meaningfully different by size band (50–200 vs. 200+) or vertical (logistics/field services vs. others)?

Watch for: onboarding and value realization may show as a single causal chain (no implementation → no feature adoption → churn). If so, treat them as one finding, not two.

### WS2: CRM Note Tagging
*Owner: Head of CS (or analytics partner) | Week 1*

Deliverable: A structured dataset across all 40 churned accounts with consistent tags. Takes ~2–3 hours total; do not ask CSMs to tag their own accounts.

Tagging schema (per account):
- Primary stated reason for churn (free text, max 1 sentence)
- Competitive mention: Y / N / unclear
- Onboarding issue flagged: Y / N / unclear
- Champion departure: Y / N
- Value complaint (didn't get ROI, didn't use product): Y / N / unclear
- CSM-noted relationship quality at renewal: strong / neutral / weak / unknown
- Time to churn from contract start: <12mo / 12–24mo / 24mo+

Output: frequency counts per tag, cross-tabbed against size band and vertical. This is the fastest triangulation source — done in week 1, before interviews.

### WS3: Exit Interviews
*Owner: Head of CS | Weeks 2–4*

Deliverable: 10–12 structured interviews with churned accounts (3–6 months post-churn, clean exits prioritized). See Interview Guide section below.

### WS4: Exit Survey
*Owner: Head of CS (send) / CSMs (relationship warm-up if needed) | Week 2–3*

Deliverable: Quantitative responses from accounts that won't do interviews. Use to validate interview themes, not as primary evidence.

Survey structure (6 questions, email-based, <5 minutes):
1. What was the primary reason you decided not to renew? [multi-select: price/cost, not enough value/ROI, product gaps, switched to a competitor, internal budget cut, other]
2. At the time of your renewal decision, had your team regularly adopted [core workflow feature]? [Yes / Partially / No]
3. How would you describe your onboarding experience? [Excellent / Good / Neutral / Difficult / We didn't really have onboarding support]
4. Did you evaluate any alternatives before deciding not to renew? [Yes, chose a competitor / Yes, chose to build internally / Yes, chose to do without / No alternatives evaluated]
5. If we had done one thing differently, what would have had the most impact on your decision? [open text]
6. Would you be open to a 20-minute conversation with me personally? [Yes / No]

## 6-Week Timeline

| Week | WS1 (Analytics) | WS2 (CRM Tagging) | WS3 (Interviews) | WS4 (Survey) |
|---|---|---|---|---|
| 1 | Data pull, cohort scoping | Complete tagging pass | Outreach to 15–20 accounts | — |
| 2 | First-pass cohort analysis | — | First interviews (recent churns) | Survey live |
| 3 | Feature adoption analysis | — | Interviews continue | Survey closes |
| 4 | Segmentation cuts | — | Final interviews | Compile responses |
| 5 | **Synthesis across all workstreams** | | | |
| 6 | **Deck development** | | | |

## Synthesis Framework (Week 5)

For each hypothesis, assess:
- What does the quantitative data say? (WS1 + WS2 frequency counts)
- What do the interviews say? (WS3 themes)
- Do they agree? If not, why might they diverge?
- Confidence level: high (two sources agree) / medium (one source clear, other ambiguous) / low (conflicting or insufficient data)

A finding with high confidence gets a recommendation. Medium confidence gets a "likely" finding with a caveat. Low confidence gets named as an open question for ongoing monitoring, not a plan item.

## Interview Guide

See Interview Guide section for full structure.

## Interview Guide

### Opening (2 min)
*"Thanks for making time. I want to be upfront: this is a research call, not a sales call — I'm genuinely not trying to win you back. I'm trying to understand what happened so we can get better. The conversation stays with me. If it would be useful, I'm happy to share a summary of what I hear across all these conversations when I'm done."*

### Context-setting (3 min)
*"Before we get into the decision itself — can you remind me where things stood for your team when the renewal came up? What were you trying to accomplish with [product], and how was it going?"*

### The decision (10 min)
*"Walk me through how the renewal decision actually played out — who was involved, what were the main conversations?"*

Listen, don't interrupt. After they finish: *"What were the two or three factors that mattered most?"* Probe on what they named — not your hypotheses.

### Experience probes (10 min)
Only after they've told you what mattered unprompted:
- Onboarding/value: *"Take me back to the first 90 days — what did your team actually accomplish during that period?"* / *"When did you feel like you were getting real value? Did that moment come?"*
- Value realization: *"Which parts of the product did your team use regularly? Were there things you bought expecting to use but didn't?"*
- Competitive: *"Did you end up going with an alternative, or did you just step away from this category?"*

### Time machine question (3 min)
*"If you could go back and change one thing about how we worked together — something on our side — what would it be?"*

### Close (2 min)
*"Is there anything you expected me to ask that I didn't?"* Then stop. No offer, no pitch.

### Field notes (within 1 hour of call)

Code each call:

| Factor | Primary | Secondary | Minor | Absent |
|---|---|---|---|---|
| Pricing/competitive | | | | |
| Onboarding friction | | | | |
| Value realization | | | | |
| Champion departure | | | | |
| Budget/unrelated | | | | |

Plus: *"The real answer in one sentence"* and *"What surprised me."*

### Anti-bias protocol
Before call 1, write down what disconfirmation looks like for each hypothesis. After interviews 5–6, share anonymized notes with one CSM for a blind coding check.

## Synthesis Framework

See Synthesis section below for how to turn four workstreams into a coherent narrative.
