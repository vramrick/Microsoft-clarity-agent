# Notes

## Guiding principles

**Ground everything in user pain, not market pressure.** The competitive announcement was marketing; the real foundation is OCR failure rate (~30%) and near-zero categorization acceptance. Every document should trace back to those numbers.

**API-first, not ML-platform.** The team has no ML experience. The right architecture is LLM API calls by existing backend engineers, not custom model training. Preserve this constraint in future phases.

**Real is better than aspirational.** The strongest moment in the board narrative is "here's what we're already testing" — the goal is to start the POC before the board meeting (~10 weeks out). Don't let the narrative get ahead of the work.

## Key facts to preserve

- OCR failure rate: ~30% of submissions require manual correction
- Categorization: near-zero acceptance rate on current rules-based suggestions
- Volume: ~2–3M submissions/month across customer base
- Timeline: board meeting ~10 weeks out
- Team: 22 engineers, no shipped ML features

## Open items

- Pull OCR vendor cost before budget conversation with CEO
- Validate 8-week POC timeline with engineering lead
- Check data pipeline access for ~500 labeled historical receipts (CS team may have from support tickets)
- Legal review of enterprise customer contracts for data processing restrictions — must happen during POC, not after
