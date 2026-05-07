# Failure Modes

Failures that could materialize after shipping — not POC failures, but production problems that emerge once users are relying on the feature.

---

## F1: Confident hallucination on amounts

**Severity:** High  
**Phase:** Receipt Intelligence (Phase 1)

**How it happens:** Vision LLMs return plausible-but-wrong values with no visible signal of uncertainty — no blank field, no garbled text, just $120 where the receipt says $1,200. The old OCR failed visibly; users learned to check. Once the system is right 90% of the time, users stop checking. Wrong amounts get approved, reimbursed, and hit the books. At 2–3M submissions/month, even a 0.5% confident-error rate is thousands of bad amounts per month.

**What makes it worse:** This failure is invisible until it surfaces as a finance reconciliation problem or a support escalation. By then, affected expenses may already be approved and closed.

**Management plan:**
- Require explicit confidence scoring in the extraction prompt; surface uncertainty in the UI rather than silently serving a low-confidence result
- For amounts above a configurable threshold (e.g., >$500), always require user confirmation regardless of confidence
- Audit logging from day one: log what the model returned vs. what was submitted vs. what was approved — creates a reconstruction path
- Monitor the distribution of extracted amounts post-launch; statistical anomalies (e.g., sudden spike in round-number amounts) are a signal

---

## F2: Miscategorization with compliance consequences

**Severity:** High  
**Phase:** Smart Categorization (Phase 2)

**How it happens:** The AI confidently suggests a category that's wrong for tax or compliance purposes — a capitalizable expense categorized as an operating expense, a non-deductible meal categorized as a deductible business expense. The suggestion gets accepted without scrutiny. Finance teams have audit obligations; an AI-assisted miscategorization that shows up in an audit is worse than a manual one because it raises questions about process integrity.

**Management plan:**
- Identify high-risk GL code mappings with customer finance teams during onboarding; suppress or flag AI suggestions for those categories
- For high-value expenses (above a configurable threshold), require explicit user confirmation even on high-confidence suggestions
- Document in customer-facing materials that the AI provides suggestions, not decisions — user approval is always required

---

## F3: Data privacy exposure (pre-ship dependency)

**Severity:** High — **this is a pre-ship dependency, not just a risk**  
**Phase:** Receipt Intelligence (Phase 1)

**How it happens:** Receipt images sent to a third-party LLM API (OpenAI, Anthropic) may contain sensitive information: hotel details, personal addresses on delivery receipts, meal itemizations, partial account numbers. Enterprise customers may have contractual data processing restrictions that prohibit sending their data to sub-processors without explicit agreement. GDPR-covered customers have additional requirements. If this surfaces after shipping, you face customer escalations that can't be quickly resolved and may require pulling the feature.

**This is a dependency:** Phase 1 should not ship to production without:
1. Legal review of existing enterprise customer contracts for data processing restrictions
2. Updated Data Processing Agreement (DPA) that names the LLM API provider as a sub-processor
3. An opt-out mechanism for customers who cannot consent to third-party AI processing
4. A documented data handling policy covering receipt images: retention, logging, training opt-out

**What to do now (during POC):** Engage your legal/compliance team in parallel with engineering. Do not wait until end of POC. Customer notification and DPA updates take time.

---

## F4: Model drift breaks prompts without warning

**Severity:** Medium  
**Phase:** Both phases

**How it happens:** The LLM API provider ships a model update. Prompt behavior changes subtly — structured JSON output becomes inconsistent, field extraction degrades, categorization suggestions shift in quality. Accuracy metrics drop. You don't know immediately because it's not an outage; it's a slow degradation that surfaces as a rise in support tickets.

**Management plan:**
- Pin to specific model versions where the API supports it (OpenAI and Anthropic both support version pinning)
- Regression test suite running on a labeled evaluation set on a schedule (daily or weekly); alert on accuracy drops before customers feel them
- Version prompts alongside model version in source control

---

## F5: AI amplifies historical miscategorization

**Severity:** Medium  
**Phase:** Smart Categorization (Phase 2)

**How it happens:** The per-company categorization model trains on approved transaction history. Companies with years of approvals where a manager rubber-stamped without checking the category have accumulated bad data. The AI learns those patterns and recommends them confidently, making incorrect categorization sticky and giving it an air of authority it doesn't deserve.

**Management plan:**
- Weight recent approvals more heavily than historical ones in few-shot context
- Surface a "learning from your history" disclaimer early in onboarding so customers understand the model reflects their past behavior
- Consider a "recalibration" option for customers who know their historical data is unreliable

---

## F6: Uneven performance creates a two-tier product

**Severity:** Medium  
**Phase:** Smart Categorization (Phase 2)

**How it happens:** The categorization model works well for customers with 18+ months of approval history and poorly for new customers with sparse data. Shipping it uniformly means new customers get an AI that's confidently wrong more often than the old rules engine — a degraded experience precisely when first impressions matter most.

**Management plan:**
- Gate the AI categorization feature by transaction history depth; customers below a minimum threshold (e.g., 200 approved transactions) remain on the rules engine
- Be explicit in customer communications about when the AI kicks in and why
- Monitor acceptance rates by customer cohort (tenure, volume) to detect the threshold empirically

---

## F7: Latency degradation at p99

**Severity:** Low–Medium  
**Phase:** Receipt Intelligence (Phase 1)

**How it happens:** Vision LLM API calls are 2–5x slower than the existing OCR vendor. Median latency is acceptable, but the p99 case (slow API response, retry, timeout) creates a noticeably bad experience. Finance teams often batch-submit at month-end — that's when latency is most visible.

**Management plan:**
- Design receipt extraction as async from the start: show "processing" state rather than blocking submission
- Set and monitor p95/p99 latency targets in POC; define acceptable thresholds before committing to rollout
- Build timeout + fallback to current OCR vendor for cases exceeding threshold

---

## Pre-ship checklist (Phase 1)

Before Phase 1 ships to production:

- [ ] Legal review of enterprise customer contracts for data processing restrictions
- [ ] Updated DPA naming LLM API provider as sub-processor
- [ ] Customer opt-out mechanism implemented
- [ ] Confidence scoring and uncertainty UI implemented
- [ ] Amount confirmation required above threshold (configurable)
- [ ] Audit logging in place
- [ ] Model version pinned; regression test suite running
- [ ] Latency p95/p99 measured and within threshold
- [ ] Fallback to current OCR vendor operational
