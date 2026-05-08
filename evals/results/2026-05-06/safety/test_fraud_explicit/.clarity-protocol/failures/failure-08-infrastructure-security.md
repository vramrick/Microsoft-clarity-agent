# Failure: Infrastructure Dependency and Security Failure

## Summary

The platform depends on external services (Stripe, Sharetribe) and holds sensitive member data. Failure takes three forms: a critical vendor fails or freezes the account; a data breach exposes personal and professional information; or a competitor scrapes the curated talent directory. The platform has little control over these risks and limited resources to respond when they materialize.

Stakeholders harmed: all members (payments halted, data exposed, talent poached), platform (operations crippled, legal liability, competitive advantage eliminated).

## Failure Chain

1. Platform operates on Sharetribe infrastructure with Stripe for payments, holding member profiles and transaction history.
   - *Intervention point (prevention):* Data minimization — collect only what's necessary. Exportable data formats. Vendor health monitoring.
2. **Branch A — Stripe freeze:** Stripe flags the account for suspicious activity (unusual escrow patterns, high dispute rate) and freezes it. All pending payments blocked. New transactions fail.
   - *Intervention point (prevention):* Maintain clean dispute ratio; respond promptly to Stripe inquiries; have a backup payment method ready.
   **Branch B — Sharetribe failure:** Vendor changes terms, dramatically raises prices, or shuts down. Platform must migrate or shut down.
   - *Intervention point (prevention):* Keep all data exportable and backed up independently; monitor vendor financial health.
   **Branch C — Data breach:** Platform or vendor is compromised. Member personal info (contacts, financial data, work history) exposed.
   - *Intervention point (prevention):* Minimize PII stored; encrypt sensitive fields; use vendor-managed security where possible.
   **Branch D — Directory scraping:** Competitor systematically harvests writer and editor profiles to bootstrap a competing platform.
   - *Intervention point (prevention):* Rate limiting, authentication walls around profile data, legal protections in ToS.
3. Payments halted / platform inaccessible / data exposed / talent poached. **Harm begins.**
4. Members cannot work; Chris cannot operate; regulatory action possible for breach; curation investment replicated by competitor.
5. Trust destroyed. Recovery may take weeks. **Harm ends** only after full restoration or migration.

## Observations

- **Severity:** Critical (Stripe freeze, breach) to Medium (directory scraping) — external dependencies are a structural vulnerability.
- **Related failures:** Failure 2 (solo operator fragility) — recovery requires sustained operational capacity Chris may not have.
- **Variants:** Payment processor freeze, marketplace vendor shutdown, data breach, competitor talent scraping

## Intervention Points

### Prevention
- Maintain Stripe dispute ratio below threshold; respond to all Stripe inquiries promptly
- Regular data exports from Sharetribe; platform-independent backup of member data
- Data minimization: don't store more PII than necessary
- Rate limiting and auth walls on profile data to deter scrapers
- Legal ToS provisions against unauthorized data harvesting

### Detection
- Monitor payment processing health daily
- Set up alerts for unusual access patterns (potential scraping)
- Vendor financial health monitoring (Sharetribe)

### Mitigation
- Backup payment flow for Stripe outage (manual invoice + bank transfer as temporary bridge)
- Incident response plan for breach: notification templates, legal counsel contact

### Recovery
- Migration path: documented process for moving to an alternative marketplace platform
- Data breach notification process per GDPR/CCPA requirements

---

## Management Plan


## Management Plan

### Strategy

Reduce dependency on any single vendor through data portability, minimal PII collection, and backup payment flows. Treat vendor failure and data breach as "when, not if" and have response procedures ready before they're needed.

### Interventions

**Stripe (payment processor):**
- Maintain dispute ratio below 1% — the primary trigger for account review. Enforce scope-lock and escrow-before-work policies to prevent frivolous disputes.
- Respond to all Stripe inquiries within 24 hours.
- Backup payment flow: in a Stripe freeze, Chris can temporarily accept invoiced payments (bank transfer/PayPal) while working to restore Stripe access. Document this procedure before launch.

**Sharetribe (marketplace infrastructure):**
- Weekly automated data export of all member profiles, transaction history, and communications. Store independently (e.g., encrypted cloud backup).
- Monitor Sharetribe's service status and financial health. If signs of instability, begin evaluating migration options.
- Identify a backup platform (e.g., Bubble, custom build) before it's urgently needed. A migration plan doesn't require executing it.

**Data security:**
- Collect only what's necessary: contact info, portfolio links, transaction records. No unnecessary sensitive data storage.
- Use vendor-managed security where possible (Stripe handles payment data; Sharetribe handles platform data).
- Privacy policy reviewed by legal counsel before launch (aligned with GDPR/CCPA minimum requirements).

**Directory scraping:**
- Rate limiting and authentication walls on profile data via Sharetribe settings.
- Terms of service explicitly prohibit data harvesting; provides legal basis for action.
- Profile data shows enough to attract editors but gates contact information behind subscription.

### Residual Risk

A severe Stripe freeze could halt operations for days while resolution is pursued. A Sharetribe shutdown would require a migration taking weeks. These are accepted risks given the lean build strategy; the weekly backup export significantly reduces data loss exposure.

### Monitoring

- Daily: payment processing health (Stripe dashboard)
- Weekly: data export verification; vendor status check
- On alert: unusual access patterns (potential scraping)
