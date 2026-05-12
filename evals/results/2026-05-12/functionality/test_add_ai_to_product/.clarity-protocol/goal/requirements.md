# Requirements

These requirements define what the AI learning engine must do to be considered successful. They are scoped to the Phase 1 beta (10-week timeline) with Phase 2 items noted separately.

## Must-have for beta

**1. Per-company categorization model**
The system must generate category suggestions using each company's own correction history, not generic rules. A company that always categorizes "Uber" as "Sales - Client Entertainment" must see that suggestion, even if the global default differs. This is the core differentiator.

**2. Confidence scoring**
The system must know when it's confident and when it isn't. High-confidence suggestions (≥80% match quality) display as a prominent single "Accept" prompt. Low-confidence suggestions display the top 3 options. Users should never be pushed toward a wrong answer.

**3. One-click accept in the submission flow**
The expense submission UI must make accepting the suggestion the path of least resistance — one tap or click, not buried in a dropdown. Override must be equally accessible without friction.

**4. Correction loop**
Every manual override must be captured and fed back into that company's model. This closes the learning loop. If a user corrects the same category 3 times in a row, the model must update before their next submission.

**5. Privacy/anonymization layer**
Before any data is sent to a third-party LLM API, merchant names must be tokenized or hashed and user/amount information must be stripped. What leaves the system is a pattern-matching signal, not customer financial data. This is a prerequisite — not optional.

**6. Measurable acceptance rate tracking**
The system must log suggestion acceptance and override rates per company, per category, and in aggregate. This is how we demonstrate success to the board and to customers ("your acceptance rate went from 4% to 61%").

## Must-have for beta → GA transition

**7. Bulk review interface (finance manager)**
Finance managers must be able to review a batch of expenses with pre-assigned confident suggestions in a single view — bulk accept, spot-check, or step through uncertain items. The per-expense flow is for employees; the batch flow is for managers.

**8. Explanation text**
When a suggestion is shown, display one line of rationale: *"Based on 23 similar expenses in your company."* This builds user trust and reduces the feeling of a black box.

## Phase 2 (post-board, follow-on investment)

**9. Natural language expense query**
Finance managers can query expense data conversationally: *"Show me all client entertainment over $200 in Q1"* or *"Which team had the highest travel spend last month?"* This is built on top of the same company-specific model, not a separate initiative.

**10. OCR accuracy improvement**
Reduce the ~30% manual correction rate on extracted merchant names and line items. Likely a vendor upgrade (e.g., Google Document AI, AWS Textract) rather than a custom model. Scoped separately from the categorization work.

## Non-requirements (explicitly out of scope)

- Automated expense *approval* — categorization is a suggestion, not a decision. Humans approve.
- Cross-company model training — each company's data is isolated. We do not train across customer data.
- Generative AI for expense policy drafting or narrative generation — not what customers asked for.
- Mobile-first redesign — this improves an existing flow, not a new surface.
