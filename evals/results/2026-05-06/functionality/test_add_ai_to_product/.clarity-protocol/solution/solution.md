# Solution

## Approach

Build AI into the core expense submission workflow — the thing every user does every day — starting with the two highest-friction points: receipt extraction and expense categorization. Use LLM APIs (not custom-trained models), so the work is software engineering, not ML research. Existing engineers can execute this.

This is not an "AI platform" play. It's two targeted improvements that fix real problems, are measurable, and compound over time.

---

## Phase 1: Receipt Intelligence (Weeks 1–8, POC)

**What:** Replace or augment the current OCR vendor with a vision LLM API call (e.g., GPT-4o, Claude). A structured prompt extracts amount, merchant name, date, line items, and currency from receipt images, returning structured JSON.

**Why this works:** Modern vision LLMs handle messy, rotated, partially obscured receipts far better than traditional OCR services. The extraction is context-aware — it understands that "$" before a number is an amount, not a merchant name.

**Engineering ask:** 2 backend engineers, 6–8 weeks.
- Weeks 1–2: API selection, integration plumbing, structured prompt design
- Weeks 3–4: Evaluation framework — measure accuracy against a labeled set of historical receipts with known-correct values
- Weeks 5–6: Iterate on prompt, handle edge cases, build fallback logic
- Weeks 7–8: Controlled rollout (subset of customers or receipt types), measure live accuracy

**Target:** Reduce manual correction rate from ~30% to <10%.

**Cost consideration:** Current OCR vendor cost vs. vision LLM API cost at 2–3M submissions/month needs direct comparison. Actual number to pull before budget conversation. Even if API cost is higher, the accuracy improvement may justify it — but this should be explicit in the ask, not assumed.

---

## Phase 2: Smart Categorization (Weeks 6–16)

**What:** Replace the rules-based category suggester with an LLM classifier that uses each company's own approved transaction history as few-shot context. Every time a user approves a categorization, the model gets a better signal for that company.

**Why this works:** The product already has the training data — it's the history of approved expense categorizations per customer. This is a hidden asset. Per-company personalization is actually an advantage: we're not trying to build a generic classifier, we're learning each customer's specific chart-of-accounts mapping.

**Engineering ask:** 1–2 backend engineers (can overlap with Phase 1 team). Start design in Week 6, POC by Week 12, rollout by Week 16.

**Target:** >60% user acceptance of suggested category (vs. near-zero today with the current rules engine).

---

## The compounding story

Each approval or correction is a training signal. The system gets better for each customer over time. By Year 2, this becomes a meaningful switching-cost moat — the AI has learned your company's specific expense patterns, chart of accounts, and edge cases. Migrating away means starting over.

---

## Budget ask structure

1. **Engineering time:** 2 engineers reallocated for 6–8 weeks (Phase 1). Internal cost, no new headcount.
2. **API costs:** To be modeled — compare vision LLM per-call cost vs. current OCR vendor contract. Likely $X–Y/month at current volume. [Pull actual number before budget meeting.]
3. **Optional advisor:** $30–60K for a 6–8 week AI architecture engagement. Accelerates getting the evaluation framework and API selection right. Not required, but reduces risk of costly rework.

---

## What this is not

- Not an "AI copilot" or chatbot layer
- Not a multi-year ML platform build
- Not dependent on hiring ML engineers
- Not vaporware — both phases have measurable exit criteria and can be running within 10 weeks

---

## Open question

What is the current OCR vendor cost per month? This is the single number needed to complete the budget ask.
