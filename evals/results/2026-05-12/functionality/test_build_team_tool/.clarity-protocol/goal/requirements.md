# Requirements

Requirements are ordered by priority. All items marked **must** are non-negotiable; **should** items are strong defaults; **may** items are explicitly deferred.

## Functional Requirements

**F1 — Status updates (must)**
Engineers can post a status update containing: a codebase area tag (from a defined list: payments, auth, infra, etc.), a free-text task description, and a status value (in progress / blocked / done).

**F2 — Blocking flags (must)**
An update can include an optional blocking note — free text naming what/who the engineer is waiting on. This is distinct from status so it's immediately visible to teammates.

**F3 — Team dashboard view (must)**
A single view shows the current status of all team members — one entry per person, most recent update. This is the primary view; it must be scannable at a glance.

**F4 — Staleness indicators (must)**
Each entry shows when it was last updated. Entries older than ~24 hours (or a configurable threshold) are visually flagged as potentially stale. A stale dashboard creates false confidence; this must be immediately visible.

**F5 — Area grouping / adjacency visibility (must)**
The dashboard can be sorted or filtered by codebase area, so engineers can quickly see "who else is in payments right now." This is the core feature that would have caught both the production incident and the duplicate debugging.

**F6 — Linear ticket link (should)**
Updates may optionally include a link to a Linear ticket. Not required; adds useful context without being mandatory.

**F8 — Admin-managed area tag list (must)**
Codebase area tags are drawn from a fixed, admin-curated list (seeded with ~10–15 areas at launch). Engineers pick from the list; they cannot create new tags. The EM/admin can add tags. This prevents fragmentation that would break adjacency detection.


Optional, opt-in notifications when two or more engineers post updates in the same codebase area simultaneously. Not in v1; to be added if the team requests it.

## Non-Functional Requirements

**N1 — Low friction (must)**
Posting an update must take under 60 seconds. If it's slower than that, compliance will drop. The tool lives or dies on update frequency.

**N2 — Not surveillance (must)**
The tool is designed for peer coordination, not managerial monitoring. The EM's visibility is a side effect of the same data engineers post for each other — there is no separate "manager view" with additional data. Update history should not be prominently surfaced as a performance record.

**N3 — Internal-only access (must)**
The dashboard is accessible only to the engineering team. No public access; auth required.

**N4 — Team size: small (constraint)**
Designed for ~7 engineers. Does not need to scale beyond ~20. This frees the design from heavy infrastructure.

**N5 — Staleness rules (must)**
Two staleness tiers, both visual-only (no auto-expiry):
- **Stale**: no update posted in >24 hours on a workday
- **Stagnant**: status has been "in progress" for >3 days without any update

**N6 — Authentication: GitHub org OAuth (must)**
Access gated via GitHub org membership. All team members already have GitHub accounts; no separate credential management needed.

**N7 — Self-hosted web app (constraint)**
Deployed on team infrastructure. Not a Slack app or third-party SaaS — intentionally a separate destination engineers navigate to, not another feed to scroll past.



- Sprint planning, task management, or ticket tracking (Linear already does this)
- Time tracking
- Performance review or metrics tied to individuals
- External stakeholder access
