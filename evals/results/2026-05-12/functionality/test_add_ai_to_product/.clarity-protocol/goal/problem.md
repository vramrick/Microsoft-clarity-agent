# Problem Statement

We sell expense management software to finance teams at mid-market companies. The CEO needs a credible "AI story" ahead of an upcoming board meeting, and key customers are asking about AI in QBRs. We need to decide what to actually build — not just what to say — and walk into a budget conversation with a concrete, defensible ask.

The core tension: there's external pressure to have an AI narrative quickly, but the real goal is to build something that creates genuine value for finance teams, not just to check a box.

## Why This Matters

- Board meetings are high-stakes: a weak or vague AI story damages credibility; an overpromised one creates future liability
- Customer QBR pressure suggests potential churn or competitive risk if we don't address this
- Budget decisions made without clear direction will be wasted or misallocated

## Key Context

**Customer AI pressure:** Mostly vague/exploratory ("what are you doing about AI?"). One customer mentioned a competitor's "smart categorization." Not a churn threat — more a check-in signal.

**Real product friction (concrete, measurable):**
- Categorization: Rules-based suggestions are wrong often enough that most users ignore them and pick manually from dropdown
- OCR extraction: ~30% of extractions need user correction (wrong merchant name, mangled line items)

**Data asset (underutilized):** 2 years of user correction logs across ~4,000 customers — before/after captured for every category override. Never used beyond analytics dashboards. This is meaningful training data.

**Chart of accounts:** Custom per company, synced from NetSuite/QuickBooks at integration setup. Already in the system.

**Strategic framing:** "One AI layer" — a per-company learning engine that fixes categorization, with a natural language query interface as a surface on top. Not a chatbot as a separate initiative.

**Competitive situation:** One direct competitor announced an "AI assistant" 3 months ago. Press release language ("intelligent expense management") — no confirmed shipped product.

**Timeline:** Budget conversation in ~3 weeks. Board meeting in ~10 weeks.

**Engineering reality:** 22 engineers, zero shipped ML. One engineer with ML interest/training. Custom model development requires hiring or vendor. Beta/pilot by board meeting is realistic; full launch is not.

**Board meeting bar:** "50 customers piloting this" is equivalent to "shipped" for board purposes. Credible roadmap + early access is achievable and acceptable.

**Core tension:** External pressure to have an AI narrative quickly vs. building something genuinely valuable for finance teams. The product friction points are real and AI-addressable — the risk is chasing the wrong kind of "AI story."

## Success Criteria

- **3 weeks:** Budget approved with a concrete plan
- **10 weeks (board meeting):** Beta or early access pilot in front of real customers
- **Ongoing metric:** Categorization acceptance rate above 50% (currently near 0% effective — users ignore suggestions)
