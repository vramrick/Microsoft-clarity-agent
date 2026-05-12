# Engineering Proposal: AI Receipt & Categorization

## What we're proposing

Two phases of AI work embedded in the core submission flow. Phase 1 is a POC with a clear exit criterion. Phase 2 starts during Phase 1 at the design level. Neither requires ML expertise or new hires.

---

## Phase 1: Receipt Intelligence POC (Weeks 1–8)

**Problem:** ~30% of receipt submissions require manual correction (wrong amount, garbled merchant, missing fields). Current OCR vendor has inconsistent failure modes — not one clean problem type.

**Approach:** Augment or replace the OCR vendor pipeline with a vision LLM API call. The model receives the receipt image and returns structured JSON: amount, merchant, date, line items, currency. We pick an API provider (GPT-4o and Claude both handle this well), design the prompt for structured extraction, build fallback handling, and measure accuracy.

**Why this is software engineering, not ML:** We're not training a model. We're calling an API with a carefully designed prompt and parsing the response. The evaluation framework (comparing extracted fields against a labeled set of historical receipts) is the most technical part, and it's straightforward.

**What we need:**
- 2 backend engineers, focused for 6–8 weeks
- API access to 1–2 vision LLM providers for evaluation
- A labeled evaluation set: ~500 historical receipts with known-correct field values (CS team may have these from support tickets)

**Week-by-week:**
| Weeks | Work |
|-------|------|
| 1–2 | API selection, integration plumbing, structured prompt v1 |
| 3–4 | Evaluation framework, baseline accuracy measurement |
| 5–6 | Prompt iteration, edge cases, fallback logic |
| 7–8 | Controlled rollout (subset of customers), live accuracy metrics |

**Exit criterion:** Manual correction rate below 10% on the evaluation set. If we don't hit that, we've learned something real and can decide whether to continue.

**Cost question to resolve:** What are we currently paying the OCR vendor per month? Vision LLM API costs at 2–3M calls/month need to be modeled against that. Even if there's a cost delta, the accuracy improvement may justify it — but we should go in with the number.

---

## Phase 2: Smart Categorization (Weeks 6–16)

**Problem:** Rules-based category suggester is wrong often enough that users ignore it entirely. Every expense submission ends with a manual dropdown selection.

**Approach:** LLM classifier with per-company few-shot context. We pass the model the expense description, merchant name, and the last N approved categorizations for that company, and ask it to suggest the most likely category from their chart of accounts. We already have the training signal — it's the history of approved transactions.

**Why per-company matters:** Customers have their own chart of accounts mapped to NetSuite/QuickBooks. A generic classifier would be wrong for the same reasons the rules engine is. Per-company context makes this tractable without custom model training.

**Engineering ask:** 1–2 engineers (overlap with Phase 1 team). Design starts Week 6, POC by Week 12, production rollout by Week 16.

**Exit criterion:** >60% user acceptance of suggested category on a pilot cohort.

---

## Risks

| Risk | Mitigation |
|------|------------|
| Vision LLM accuracy doesn't hit target | Run evaluation before committing to vendor; fallback to current OCR if below threshold |
| API costs exceed OCR vendor cost | Model costs explicitly before budget ask; structured as known tradeoff, not surprise |
| Latency: vision LLM calls are slower | Async extraction with user-visible "processing" state; measure P95 latency in POC |
| Prompt reliability at scale | Evaluation framework catches this; structured JSON output with schema validation |

---

## What this is not

This is not a request to build an ML platform, hire ML engineers, or commit to a multi-year AI infrastructure investment. Phase 1 is a focused POC with a binary exit criterion. If it works, we ship it. If it doesn't, we've spent 8 weeks and learned something.

---

## The ask

- 2 engineers reallocated for 8 weeks (Phase 1)
- API costs: [to be determined — pull OCR vendor contract]
- Optional: short-term AI architecture advisor ($30–60K, 6–8 weeks) — not required but reduces rework risk
