# Churn Diagnosis Research Program

## What We're Doing and Why

Logo churn has risen from 7% to 11% over the last three quarters. The cause is unknown — we have anecdotal hypotheses (competitive pricing pressure, onboarding failures) but no rigorous evidence. Before annual planning, we need a diagnosis the COO can act on: what's driving the increase, and what do we do about it.

This document is the full research program. It's structured so individual sections can be shared with specific audiences: the analytics brief, the CSM brief, and the interview guides are self-contained. The COO narrative skeleton at the end frames where all of this is heading.

---

## Timeline Overview

| Week | Work |
|------|------|
| 1 | Analytics sprint kicks off; CSMs code their churned account notes; survey + interview outreach goes out |
| 2 | Analytics sprint delivers; interviews begin; survey responses collected |
| 3 | Interviews continue (target: 10–12 completed) |
| 4 | Interviews wrap; preliminary synthesis begins |
| 5 | Full synthesis; intervention design; COO narrative drafted |
| 6 | COO presentation |

---

## Section 1: Analytics Partner Brief

*Share this section with your analytics partner to scope the sprint.*

### Context

We have approximately 40 accounts that churned over the last two quarters. We have product usage data (feature adoption, DAU, session depth), support ticket history with sentiment tags, NPS data (low coverage, ~15% response rate), and CRM renewal/cancellation notes. No structured analysis of this population has been done.

We need this sprint completed and findings delivered by end of Week 2.

### Deliverable 1: Churned Account Segmentation

Pull the 40 churned accounts and segment them along:
- ARR tier (e.g., <$10K, $10–50K, >$50K annually — use whatever tiers make sense for our book)
- Company size (employee count or revenue band from CRM)
- Industry vertical
- Tenure at time of churn (time from contract start to churn notice)
- Time-to-churn-notice (how far in advance did they notify us?)

**Output:** A simple table of the 40 accounts with these dimensions filled in, plus a brief narrative: is the churn increase concentrated in a specific segment, or is it broad-based?

### Deliverable 2: Behavioral Fingerprint — Churned vs. Retained

Build a matched comparison cohort of retained accounts (same ARR tiers and rough size profile as the churned group). Then compare pre-churn behavioral signals:

**Feature adoption:** For churned accounts, what was the feature adoption breadth at 30, 60, and 90 days post-onboarding? How does this compare to retained accounts at the same tenure marks?

**DAU/engagement trend:** Plot average DAU (or seat utilization rate, whichever is cleaner) for churned accounts over the 90 days *before* churn notice. Did usage decline, hold flat, or spike? Compare to retained cohort trend over the same trailing window.

**Support patterns:** Ticket volume and sentiment (using existing sentiment tags) in the 60 days before churn notice vs. the same window for retained accounts. Look for elevated volume, negative sentiment trend, or unresolved escalations.

**NPS where available:** For churned accounts with NPS data, what was their last score and trend direction?

**Output:** A summary visualization or table showing the behavioral signature of churned accounts vs. retained, with your interpretation of what patterns are strong vs. weak signals. Flag any segments where the pattern looks different from the overall.

### Deliverable 3: CRM Note Themes

Pull CRM notes from renewal and cancellation conversations for the 40 churned accounts. Code each account by:
- Stated primary reason (use these categories: Pricing/competitor, Product gap, No demonstrated ROI, Onboarding/adoption failure, Org change/budget cut, Other)
- Whether warning signs appeared in QBR or check-in notes before the final renewal conversation (Yes / No / Insufficient notes)
- Confidence in the coding (High = clear stated reason, Low = thin notes)

**Output:** A frequency table of coded reasons, and a flag on what percentage of accounts have insufficient CRM notes to code reliably.

### A Note on Interpretation

Don't resolve contradictions between what customers said (CRM notes) and what the data shows (usage patterns). Surface them. If a customer's stated reason was "pricing" but their usage had been declining for 90 days before the renewal conversation, note that — it's one of the most important findings we can get.

---

## Section 2: CSM Brief

*Share this section with your CSM team.*

### What We're Doing

We're running a structured research program to understand why churn has been increasing. This isn't a fire drill — it's a deliberate, six-week effort to get a real answer so we can show up to annual planning with something credible. I need your help with two specific things.

### Ask 1: Account Note Review (Week 1, ~60–90 min per CSM)

Go through your churned accounts from the last two quarters and do a structured pass on your notes. For each account, answer these questions in a shared doc I'll send you:

1. What was the stated reason for not renewing?
2. Were there warning signs before the renewal conversation? (missed QBRs, dropped engagement, specific complaints)
3. In your judgment, what was the *real* reason — even if it differs from what was stated?
4. Was there anything we could have done differently, and when?

Be honest. This isn't a performance review of your accounts — it's a diagnostic. The more candid you are, the more useful the output.

### Ask 2: Interview Outreach (Week 1)

I'll give you a list of 8–10 of your former accounts to reach out to for a 30-minute listening session. I'll provide the outreach template. Your job is to send it from your name — a warm intro from you will get 2–3x the response rate of anything I send cold.

**What to say:** Use the template I'll provide. The framing is: "We're doing a genuine listening exercise, not a sales call. Your experience would help us serve customers better. No obligation."

**What not to say:** Don't promise anything we can't deliver. Don't apologize on the company's behalf (that's for the Head of CS to do if appropriate). Don't get into product roadmap discussions on the outreach.

**Sensitive accounts:** I'll flag 2–3 accounts that need special handling and will do that outreach myself. You don't need to touch those.

### Timeline for Your Involvement

- **By end of Week 1:** Account note review complete; outreach sent to your assigned accounts
- **Weeks 2–3:** Reply to any scheduling questions; let me know if anyone responds unusually (very positive, very negative)
- **Week 5:** Brief debrief with me on what you're hearing from current at-risk accounts (30 min, I'll schedule)

---

## Section 3: Outreach Templates

### Standard Interview Invitation (CSM sends)

> Subject: A quick question about your experience
>
> Hi [Name],
>
> I hope you're doing well. I wanted to reach out personally — [Company] is doing a listening exercise with former customers to understand how we can do better, and I thought your perspective would be genuinely valuable.
>
> This isn't a sales call. We're not trying to win your business back. We just want to understand your experience, including what didn't work for you.
>
> Would you be open to 30 minutes with [Head of CS] sometime in the next few weeks? Happy to find a time that works.
>
> Thanks for considering it.
> [CSM Name]

### Service-Failure Account (Head of CS sends directly)

> Subject: A personal note
>
> Hi [Name],
>
> I've been doing a personal review of accounts we lost this past year, including yours. I wanted to reach out directly — not to revisit what happened or ask you to relitigate it, but because I think there's something real I can learn from your experience.
>
> I understand completely if you'd rather not, and there's no pressure here. But if you'd be willing to give me 20 minutes, I'd be grateful.
>
> [Your name]

### Survey (to all 40 accounts not yet contacted for interviews)

> Subject: 3 minutes — help us do better
>
> Hi [Name],
>
> As part of a genuine effort to understand where we fell short, I'd love two minutes of your time. If you're not up for a call, this short form covers the essentials.
>
> [Survey link]
>
> Thanks for anything you're willing to share.

**Survey questions:**
1. What was the primary reason you decided not to renew? *(Pricing / Product gaps / Moved to a competitor / Didn't see enough ROI / Budget or org change / Other)*
2. Did you move to another solution? If so, which one? *(free text)*
3. How far in advance had you made the decision not to renew? *(Less than 30 days before renewal / 1–3 months before / More than 3 months before)*
4. What, if anything, could we have done differently? *(free text)*
5. Would you be open to a brief 20-minute call to share more? *(Yes — [scheduling link] / No thanks)*

---

## Section 4: Interview Guide

*For all churned customer interviews except the service-failure account.*

**Format:** 30–45 minutes, video or phone. Head of CS conducts. No slides. Take notes in real time or record with permission.

**Opening (2 min):** Thank them for their time. Confirm: this is a listening exercise, not a sales call. Ask permission to take notes or record.

**Core questions — ask these in order, don't skip ahead:**

1. *"Can you walk me through when your relationship with us first started to feel uncertain?"* — Let them locate the timeline. Don't suggest a starting point.

2. *"What was happening on your end at that time?"* — Probe for business context: org changes, budget pressure, strategic shifts. Sometimes churn has nothing to do with you.

3. *"What alternatives were you considering, or did you move to?"* — If they name the competitor, probe: what was the appeal? Was it price, features, something else?

4. *"What was the moment it tipped — when did the decision feel made?"*

5. *"What would have had to be true for you to stay?"* — This is the most actionable question. Listen carefully.

6. *"Is there anything we could have done differently, and when?"*

**Closing (3 min):** Thank them. Ask if there's anything they wanted to say that you didn't ask about. Don't make promises.

**After the call:** Within 24 hours, write up: (a) timeline of the relationship from their perspective, (b) stated reason, (c) your read on the real reason if different, (d) direct quotes worth keeping, (e) one thing you'd flag for the synthesis.

**For the service-failure account specifically** — see the earlier guidance in this document. Don't open with the incident; open with *"When did your relationship with us first start to feel uncertain?"* and let them find the starting point. Test cause vs. accelerant with: *"Before that happened, how would you have described your team's relationship with the product?"* and *"Had there been any internal conversations about the renewal before the incident?"*

---

## Section 5: Synthesis Framework

*Use this in Weeks 4–5 to structure findings.*

### Cross-validation matrix

For each identified root cause theme, fill in:

| Theme | # interviews mentioning it | Supported by quant data? | ARR represented | Confidence |
|-------|---------------------------|--------------------------|-----------------|------------|
| Competitive pricing | | | | |
| Onboarding/adoption failure | | | | |
| Product gap | | | | |
| No perceived ROI | | | | |
| Org/budget change | | | | |

Confidence is High only if both interviews and behavioral data point the same direction. Medium if one source is strong. Low if it's interview-only with contradictory or absent data.

### The cause/accelerant distinction

For each theme, ask: *If this factor hadn't been present, would the account likely have renewed?* If yes, it's a cause. If the usage data shows disengagement predating the stated reason, it's likely an accelerant on top of something else.

### Prioritization

Rank confirmed root causes by:
- **Frequency** (% of churned accounts this explains)
- **ARR impact** ($ of churned revenue attributable)
- **Fixability** (is there a clear intervention within our control?)

The top 2–3 causes by this ranking are what the COO presentation leads with.

---

## Section 6: COO Narrative Skeleton

*Draft the presentation around this structure. Fill in findings as they emerge.*

**Slide 1 — The situation**
> Churn increased from 7% to 11% over the last three quarters — [X]% increase in logo loss, representing approximately $[Y]M in ARR. Annual planning is the right moment to address this with a real plan.

**Slide 2 — What we did**
> Rather than guess, we ran a structured diagnosis: cohort analysis of all 40 churned accounts over [period], [N] in-depth interviews with former customers, and a survey reaching the full population. Here's what we found.

**Slide 3 — Primary finding**
> [Finding 1 — e.g., "Competitive displacement in mid-market accounts is responsible for approximately X% of churned ARR. Accounts at the $[range] tier are particularly vulnerable to [Competitor], primarily on pricing."]
> *Supporting evidence: [N] interviews confirmed; usage data shows [pattern]; CRM notes coded [Y%] with competitive reference.*

**Slide 4 — Secondary finding**
> [Finding 2 — e.g., "A second driver is onboarding failure: accounts that didn't reach [feature adoption threshold] within 90 days churned at [X]x the rate of those that did. This is fixable."]

**Slide 5 — What surprised us**
> [Finding 3 or a contradiction — e.g., "Pricing was the most common stated reason in cancellation conversations, but usage data shows that the accounts citing price had already disengaged 90+ days earlier. Price was often the excuse; low perceived value was the cause."]

**Slide 6 — What we're recommending**

| Root cause | Intervention | Owner | Estimated lift |
|------------|-------------|-------|----------------|
| [Finding 1] | [Intervention] | [Owner] | [Impact] |
| [Finding 2] | [Intervention] | [Owner] | [Impact] |
| [Finding 3] | [Intervention] | [Owner] | [Impact] |

**Slide 7 — What we're asking for**
> To execute this plan, we need: [specific resources — headcount, tooling, budget]. In return, we're targeting a return to [X%] churn by [date], which represents approximately $[Y]M in retained ARR.

---

*This skeleton becomes your COO deck. Slides 3–5 fill in from synthesis findings in Week 5. Slide 7 requires a conversation with Finance/RevOps on ARR impact before the presentation.*
