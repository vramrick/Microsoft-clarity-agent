# Solution

## Approach: Trust-First Curated Marketplace, Built Lean

The platform is organized around a single principle: **trust**. Every feature either builds trust between writers and editors, or protects the platform's ability to enforce it. This shapes every design decision, from how people get in, to how money moves, to how reputation accumulates.

The Year 1 build is deliberately lean — using off-the-shelf tools and no-code/low-code platforms where possible, outsourcing commodity infrastructure (payments, analytics), and reserving custom development for the pieces that are genuinely differentiating. The platform validates its model with ~150 members before investing in bespoke engineering.

## Core Solution Layers

### 1. Curated Access (Gated Entry)
Not open signup. All writers and editors apply, are reviewed against documented criteria, and are accepted or rejected. Accepted members begin with a probationary standing — they gain full ranking and visibility through demonstrated performance.

**Implementation:** Application forms (Typeform or similar) feeding into an operations dashboard (Airtable or Notion) that Chris uses to manage review, acceptance, and onboarding.

### 2. Discovery and Matching (The Marketplace)
Writer profiles display: portfolio samples, bio, topic specializations, ratings from past work, and platform rank. Editors browse and filter by topic, genre, experience, and rating. Editors post project briefs; writers pitch directly or respond.

**Implementation:** Off-the-shelf marketplace platform (Sharetribe or equivalent) handles profiles, search, listings, and messaging. Chosen for its native support for subscription + transaction fee models without heavy custom development.

### 3. Transaction Infrastructure (Trust in Money)
Escrow-style payment flow: editor funds a project upfront → work is delivered and accepted → platform releases payment to writer minus transaction fee. This deters off-platform side-deals, protects writers from non-payment, and gives the platform a lever in disputes.

**Implementation:** Stripe Connect handles payment holding, escrow release, and subscription billing. Sharetribe integrates natively; this can be extended with custom logic if needed.

### 4. Quality and Reputation Engine (Trust Over Time)
After project completion, editors rate writers. Ratings aggregate into a platform ranking score that determines profile prominence and tier access. Top-ranked writers get featured placement and access to premium subscription-tier editors. Persistent poor performers are flagged; violations of standards result in removal.

**Implementation:** Basic rating collection built into the marketplace platform. Ranking logic starts simple (weighted average) and evolves. Chris manually reviews flagged cases in Year 1.

### 5. Operations Tooling (Chris's Control Room)
Chris needs a manageable solo workflow for: vetting applications, monitoring quality, resolving disputes, and tracking platform health. This doesn't need to be custom software — a well-organized Airtable base with views for each workflow serves this at Year 1 scale.

**Implementation:** Airtable (or Notion) for vetting queue, active disputes, member status, and basic metrics. Escalate to custom dashboard when volume demands it.

## Key Design Decisions

### Decision: Off-the-shelf marketplace platform for MVP
**Rationale:** Chris is not a developer. Building a custom marketplace from scratch (even with hired developers) is expensive, slow, and risky for a pre-validation concept. Sharetribe and equivalent platforms provide profiles, search, messaging, and payments out of the box, and are designed for exactly this use case.
**Tradeoff:** Less flexibility for custom features (ranking algorithm, fraud detection tooling) in the short term. Plan: launch on the platform, validate with real users, build custom where the constraints bite.

### Decision: Escrow payment model
**Rationale:** Protects writers from non-payment, discourages off-platform deals, and gives the platform standing in disputes. The added friction of upfront escrow is worth it — it signals to both sides that the platform is serious.
**Alternative considered:** Direct payment with retroactive fee invoicing. Rejected because it doesn't protect writers and creates fee collection problems.

### Decision: Application-based entry, manual review at launch
**Rationale:** The curation is the product. Automated screening can assist, but Chris's judgment and personal relationships are the quality signal at launch. Tools augment; they don't replace.
**Risk:** This doesn't scale beyond ~200–300 members without process changes. Addressed by treating Year 1 as the validation phase, not the scale phase.

### Decision: Separation of contracts and content
**Rationale:** Hosting content and managing contracts creates legal liability and operational complexity far beyond the platform's capacity. Providing templates respects user needs without taking on responsibility.

## Failure Modes Observed During Brainstorming

- **Writer poaching / off-platform deals:** Escrow friction helps; but editors and writers who build strong relationships may be tempted to cut the platform out. Needs contractual protections and monitoring signals (e.g., projects started but never funded through the platform).
- **Application gaming:** Writers submitting polished but inauthentic portfolios. Manual review helps; portfolio verification tools needed as volume grows.
- **Rating inflation:** Editors give uniformly high ratings to avoid conflict. Ranking becomes meaningless. Needs calibration mechanisms (e.g., comparative ranking, editor-specific baselines).
- **Solo operator burnout:** Chris is a single point of failure for vetting, disputes, and standards enforcement. If platform growth outpaces his capacity, quality degrades. Hard ceiling needs to be acknowledged and planning triggered before hitting it.
- **Platform dependency risk:** Building on Sharetribe or similar creates vendor lock-in. If the vendor changes pricing, terms, or shuts down, migration is costly. Mitigate by keeping data exportable and monitoring vendor health.

## Open Questions

- Transaction fee rate (Q3 from open questions) — competitive research needed before setting rates
- Legal compliance strategy (Q4) — especially Stripe's requirements, contractor classification, and data privacy
- When and how to trigger hiring (Chris's capacity ceiling)
