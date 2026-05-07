# Churn Research Program Brief

**Purpose:** Diagnose why gross logo churn increased from ~7% to ~11% over the last three quarters and produce a defensible churn plan for annual planning.  
**Timeline:** 6 weeks  
**Output:** Evidence-backed findings + 10–15 slide deck for COO, with potential board roll-up  
**Owner:** Head of Customer Success

---

## The Three Hypotheses

We are testing three specific explanations for the churn increase. The research is designed to confirm, disconfirm, or return an inconclusive verdict on each.

**H1 — Onboarding friction**  
Accounts that didn't receive dedicated implementation support activated more slowly, adopted core workflow features at lower rates, and churned at higher rates as a result.

*Confirmed if:* Cohort data shows a meaningful churn rate differential between accounts with and without dedicated implementation support, corroborated by interview themes.  
*Disconfirmed if:* Fewer than 3 of 12 interview subjects mention onboarding unprompted, AND the cohort churn rate differential is less than 1.5x. If both conditions are true, this is not the primary driver.

**H2 — Value realization gap**  
Some accounts never adopted the core workflow features, never perceived ROI, and therefore didn't have a defensible reason to renew.

*Confirmed if:* Churned accounts show materially lower core feature adoption at 60 and 90 days compared to the retained cohort.  
*Disconfirmed if:* Churned and retained accounts show similar feature adoption curves. If so, the problem is not product engagement — look harder at pricing and competitive displacement.

**H3 — Competitive pricing displacement**  
A competitor who entered ~18 months ago at a lower price point is winning renewals on price, particularly in the 50–200 employee segment.

*Confirmed if:* Competitive mentions appear in >30% of CRM tags and >4 of 12 interviews, and interview subjects describe price as a primary or secondary factor.  
*Disconfirmed if:* Competitive mentions are sparse across both sources, and/or interview subjects describe the competitor as an evaluation they didn't choose.

**Note on H1 and H2:** These may turn out to be a single causal chain — accounts that didn't onboard well also didn't realize value. If the data shows this, treat it as one finding, not two. It strengthens the case.

**Note on hope and bias:** The single-mechanism story (H1 → H2 as one chain) is the easiest to act on. That's also a reason to hold the falsification criteria seriously. Let the evidence table in week 5 determine the story, not the story determine the evidence.

---

## Workstreams

### WS1: Cohort & Usage Analysis
**Owner:** Analytics partner  
**Weeks:** 1–3 (complete by end of week 3)

Before pulling data, confirm: do we have enough retained accounts in the 50–200 employee band to build a valid comparison group? This is a 30-minute scoping conversation, not a research project.

**Pull list:**
- All 40 churned accounts (last 2 quarters)
- Matched retained cohort: same size band, similar acquisition vintage, same verticals where possible

**Analysis:**
1. Split churned accounts by implementation resource status (dedicated vs. self-serve). Calculate churn rate for each group. We need a number, not a trend — the COO will ask for it.
2. Feature adoption curves: for churned accounts, what % of users were active on core workflow features at 30, 60, and 90 days? Compare to retained cohort.
3. Time-to-churn: does churn concentrate at first renewal? Second? Does this differ by implementation status?
4. Segmentation: is churn rate meaningfully different by size band (50–200 vs. 200+) or vertical (logistics/field services vs. others)? Even a "no detectable pattern" answer is useful.

---

### WS2: CRM Note Tagging
**Owner:** Head of CS (or analytics partner) — do NOT ask CSMs to tag their own accounts  
**Week:** 1 (complete by end of week 1)

Tag all 40 churned accounts against this schema. One person applies the schema to ensure consistency.

| Field | Options |
|---|---|
| Primary stated reason | Free text, max 1 sentence |
| Competitive mention | Y / N / unclear |
| Onboarding issue flagged | Y / N / unclear |
| Champion departure | Y / N |
| Value complaint (no ROI, didn't use product) | Y / N / unclear |
| Relationship quality at renewal | strong / neutral / weak / unknown |
| Time to churn from contract start | <12mo / 12–24mo / 24mo+ |

Output: frequency counts per tag, cross-tabbed against size band and vertical. This is the fastest triangulation source and feeds interview preparation.

---

### WS3: Exit Interviews
**Owner:** Head of CS  
**Weeks:** 2–4 (outreach in week 1)

**Target:** 10–12 interviews from the ~15–20 reachable accounts. Prioritize accounts that churned 3–6 months ago — fresher recall, more candid. Skip accounts that left contentiously.

**Outreach email:**

> Subject: Quick ask — 20 minutes to share what you saw
>
> Hi [Name],
>
> I'm doing a structured research project on why some of our customers have decided not to renew, and I'd love 20 minutes of your honest perspective.
>
> This isn't a sales conversation — I'm genuinely not trying to win you back. I'm trying to understand what we got wrong so we can fix it. Your name won't appear in anything I publish internally.
>
> If you're open to it, I'm happy to share a summary of what I hear across these conversations when I'm done — sometimes that's useful context if you're evaluating vendors in this space.
>
> Would you have 20 minutes in the next two weeks? [Calendly link]
>
> Thanks either way —
> [Name]

Add one specific personal sentence at the top for any account where you have a real memory or detail from the CRM notes.

**Interview structure (30 minutes):**

*Opening (2 min):* "This is a research call, not a sales call. I'm not trying to win you back. Your name won't appear in anything I publish internally. Happy to share a summary of findings when I'm done, if that's useful."

*Context-setting (3 min):* "Before we get into the decision — remind me where things stood for your team when the renewal came up. What were you trying to accomplish, and how was it going?"

*The decision (10 min):* "Walk me through how the renewal decision played out — who was involved, what were the main conversations?" Listen without interrupting. Then: "What were the two or three factors that mattered most?" Probe on what they name — not your hypotheses.

*Experience probes (10 min) — only after they've told you what mattered unprompted:*
- Onboarding: "Take me back to the first 90 days — what did your team actually accomplish during that period?" / "When did you feel like you were getting real value? Did that moment come?"
- Value realization: "Which parts of the product did your team use regularly? Were there things you bought expecting to use but didn't?"
- Competitive: "Did you end up going with an alternative, or step away from this category?" If they named a competitor: "What made that feel like the better fit?" Don't ask about price directly — let them bring it up.

*Time machine question (3 min):* "If you could change one thing about how we worked together — something on our side — what would it be?" This is the highest-signal question. Don't skip it.

*Close (2 min):* "Is there anything you expected me to ask that I didn't?" Then stop. No pitch, no offer.

**Field notes — complete within 1 hour of each call:**

| Factor | Primary | Secondary | Minor | Absent |
|---|---|---|---|---|
| Pricing / competitive | | | | |
| Onboarding friction | | | | |
| Value realization | | | | |
| Champion departure | | | | |
| Budget / unrelated | | | | |

Also write: *"The real answer in one sentence"* and *"What surprised me."*

**Anti-bias protocol:**
- Before call 1: write down what disconfirmation looks like for each hypothesis (see above). Do this before outreach goes out.
- After interviews 5–6: share anonymized notes with one CSM who didn't own those accounts. Ask them to fill out the coding sheet independently. Where your codes diverge is where bias may be operating.

---

### WS4: Exit Survey
**Owner:** Head of CS  
**Weeks:** 2–3 (live by week 2, closed by end of week 3)

For reachable accounts that won't do a 20-minute call. Validates interview themes — not primary evidence.

6 questions, email-based, under 5 minutes:

1. What was the primary reason you decided not to renew? *(multi-select: price/cost, not enough value/ROI, product gaps, switched to a competitor, internal budget cut, other)*
2. At the time of your renewal decision, had your team regularly adopted [core workflow feature]? *(Yes / Partially / No)*
3. How would you describe your onboarding experience? *(Excellent / Good / Neutral / Difficult / We didn't really have onboarding support)*
4. Did you evaluate alternatives before deciding not to renew? *(Yes, chose a competitor / Yes, chose to build internally / Yes, chose to do without / No alternatives evaluated)*
5. If we had done one thing differently, what would have had the most impact? *(open text)*
6. Would you be open to a 20-minute conversation? *(Yes / No)*

---

## 6-Week Timeline

| Week | WS1 Analytics | WS2 CRM Tags | WS3 Interviews | WS4 Survey |
|---|---|---|---|---|
| 1 | Scoping conversation; data pull begins | Complete tagging pass | Interview outreach sent | — |
| 2 | First-pass cohort analysis | — | First interviews (recent churns) | Survey live |
| 3 | Feature adoption analysis | — | Interviews continue | Survey closes |
| 4 | Segmentation cuts; final analysis | — | Final interviews | Compile responses |
| 5 | **Synthesis week** — evidence table, then the sentence, then deck spine | | | |
| 6 | **Deck development and review** | | | |

---

## Synthesis Framework (Week 5)

**Don't touch the deck until the evidence table is complete.**

### Step 1: Build the evidence table

For each hypothesis, fill in what each workstream says, then assign a verdict and confidence level.

| | WS1 Cohort | WS2 CRM tags | WS3 Interviews | WS4 Survey | Verdict | Confidence |
|---|---|---|---|---|---|---|
| H1 Onboarding friction | | | | | confirmed / partial / disconfirmed | high / med / low |
| H2 Value realization | | | | | | |
| H3 Competitive pricing | | | | | | |

**Confidence rule:** High = two independent sources agree. Medium = one source clear, others ambiguous. Low = sources conflict or data is thin.

**Weighting rule when sources conflict:** Quantitative cohort data > interview themes > CRM tag frequency > survey. If interviews say "pricing" but usage data shows low feature adoption, believe the data. "Price" is the socially acceptable exit narrative. Usage data can't rationalize.

### Step 2: Find the sentence

The deck has one spine — a single sentence the whole argument is built around. Three possible story structures:

- **Single mechanism** (strongest): All evidence points to one causal chain. *"Mid-market accounts without dedicated implementation never reach core feature adoption, don't perceive ROI at renewal, and churn at 2x the rate of supported accounts."*
- **Segmented** (solid): Different causes for different customer groups. The plan has two tracks.
- **Multiple independent causes** (weakest): Force a hierarchy — lead with the cause that explains the most churn by volume. Don't present three equal findings with no priority.

### Step 3: Deck structure

1. **The situation** — Churn went from 7% to 11%. What that means in ARR. We didn't have a rigorous explanation.
2. **The method** — What we did to find out. Brief — 1 slide. Establishes credibility of what follows.
3. **The finding** — [The sentence.] The number.
4. **The mechanism** — *Why* it happens. The causal chain. This is the most important slide and the one most decks skip. *"Accounts without dedicated implementation complete onboarding at X% the rate of supported accounts, reach core feature activation 60–90 days later, and show half the engagement at 6 months."*
5. **The plan** — What we're changing. What we're asking for. Each ask maps explicitly to a finding.
6. **What we don't know** — What we looked for and didn't find, or where confidence is medium rather than high. Include this slide. A COO who asks a question you've already named in this slide trusts the rest of the deck more, not less.

**Slide title discipline:** Every title should be a conclusion, not a description.
- ❌ "Interview Themes"
- ✅ "Churned accounts consistently describe an onboarding experience without a clear value moment"

If you can't write a conclusion title, the finding isn't ready to be in the deck.

---

## How to Use This Brief

**With your analytics partner:** Share WS1 spec. Start with the scoping conversation on the matched cohort. She'll push back and improve the technical approach — that's the point. Make sure she knows the output we need is a churn rate differential with an actual number, not a correlation.

**With your CSMs:** Share the context (churn increase, research program, 6-week timeline) and their role: supporting interview outreach for accounts they have warm relationships with. Do not ask them to do the CRM tagging on their own accounts. Frame the program as account diagnosis, not CSM performance review.

**For yourself:** Fill out the falsification criteria for each hypothesis before outreach goes out. This is the piece most likely to get skipped under time pressure. It takes 15 minutes and will save you from finding the story you hoped for.
