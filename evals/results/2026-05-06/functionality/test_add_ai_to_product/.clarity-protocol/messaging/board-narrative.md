# Board Narrative: AI Strategy

## The one-paragraph version

Expense management is a workflow product — the value is in frictionless submission, accurate data, and fast approvals. AI makes all three better. We're building it into the core submission flow, starting with the two highest-friction points our customers tell us about: receipt extraction and expense categorization. This isn't a chatbot feature or a roadmap slide — it's a targeted, measurable improvement to something every one of our users does every day.

---

## Narrative arc (for a 5-minute board discussion)

**The problem is specific.** Our customers' employees submit expenses the same way they always have — take a photo of a receipt, fill in some fields, pick a category. About 30% of receipt scans require manual correction because the extraction is wrong. And our category suggestions are wrong often enough that most users just ignore them and pick from a dropdown. That's friction on every single submission, for every user, every day.

**The opportunity is now.** The underlying technology — vision models that can read a receipt the way a human would, language models that can learn a company's specific expense patterns — has crossed a threshold in the last 18 months. The approach we're taking doesn't require hiring ML engineers or building model infrastructure. It's API-based, executable by our existing team.

**What we're doing.** We're running a proof-of-concept right now [or: starting immediately] on receipt intelligence — swapping our current OCR vendor pipeline for a vision model that extracts structured data directly from receipt images. Target: cut manual correction rates from 30% to under 10%. In parallel, we're designing a per-company smart categorization system that learns each customer's chart-of-accounts mapping from their own approval history.

**Why this compounds.** Every approval is a training signal. The system gets better for each customer over time. This starts as an accuracy improvement; it becomes a switching-cost moat. A customer who's been on the platform for two years has a categorization model tuned to their specific expense patterns. That's hard to replicate.

**What we need.** Two engineers focused for 8 weeks, plus a decision on API vendor costs vs. our current OCR contract. We're not asking for a new team or a multi-year platform investment. We're asking for focused execution on something we can measure.

---

## Talking points for customer QBRs

> "We're embedding AI directly into expense submission — the core workflow. Near-term, that means dramatically better receipt extraction and categorization suggestions that actually match your chart of accounts. We're beginning testing this quarter and targeting production rollout [timeframe]. The design point is: AI that works invisibly when it works, not a new interface to learn."
