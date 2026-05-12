# Solution

A lightweight self-hosted web app — **Team Radar** (working name) — that gives a 7-person engineering team a live, scannable view of who's working on what, with adjacency awareness to prevent coordination failures.

## Core Concept

A single-page dashboard where each engineer has one active status entry. The primary view is person-per-row. The primary filter is by codebase area. The primary action is "update my status" — a low-friction form that takes under 60 seconds.

The tool is a place you navigate *to*, not a feed you scroll past. It is not a task manager, not a Slack replacement, not a reporting tool. It answers one question: **what is the team working on right now?**

## Main Dashboard View

**Layout:** Table, one row per engineer. Columns:

| Name | Area | What I'm working on | Status | Blocking on | Last updated |
|------|------|---------------------|--------|-------------|--------------|

- **Area** is a badge drawn from the admin-managed fixed list
- **Status** is a color-coded badge: In Progress (blue) / Blocked (amber) / Done (gray)
- **Blocking on** shows the free-text blocking note if present; empty otherwise
- **Last updated** shows relative time ("2h ago", "yesterday") with staleness tiers:
  - >24h without update → row highlighted (subtle)
  - >3 days "in progress" without update → stronger visual indicator

**Area filter:** Prominent — top of the dashboard, not buried in a settings menu. Clicking an area tag filters to only engineers with that area active. "All areas" resets. This serves both the VP use case ("show me everyone") and the coordination use case ("show me everyone in payments").

**Adjacency callout:** When two or more engineers share the same active area, a small inline badge appears on those rows: "2 in auth ⚠️". This is always visible — no action required — so anyone scanning the board can see overlaps instantly.

## Update Flow

The user's own row is always visible at the top (or highlighted). A persistent "Update status" button opens a compact form:

1. **Area** — dropdown from fixed list (required)
2. **What I'm working on** — free text, ~140 chars (required)
3. **Status** — In Progress / Blocked / Done (required)
4. **Blocking on** — free text (optional; shown if Blocked is selected)
5. **Linear ticket** — URL field (optional)

**On submit:** If another engineer is currently active in the same area, an inline warning appears before confirming: "⚠️ Jamie is also in auth." The user can dismiss and post anyway — this is a heads-up, not a gate.

## Person Drill-Down

Clicking an engineer's row opens a detail view (modal or page):

- Current status entry (full detail)
- Last 3–5 completed items (area, description, when marked done)

This serves the async standup use case — "what did Alice finish recently?" — and provides momentum context that encourages people to mark things done.

## Authentication & Access

GitHub org OAuth. All team members are already authenticated via GitHub; no separate accounts. An "admin" role (initially just the EM) can manage the area tag list and view the same dashboard as everyone else — there is no separate manager view.

## Tech Approach

Small web app. Given the constraints (7 users, simple data model, self-hosted), the right choice is a minimal backend with a simple database:

- **Backend:** Lightweight API (e.g., Python/FastAPI or Node/Express) serving a small REST API
- **Frontend:** React or similar; single page, no complex state management needed
- **Database:** SQLite or Postgres — the data model is a handful of tables (users, updates, areas)
- **Auth:** GitHub OAuth via existing library
- **Deployment:** Single container; can run on any small VPS or internal k8s cluster

The 2–3 engineer-week estimate is consistent with this scope. No novel technical challenges; the complexity is in the UX details and the staleness logic.

## What This Doesn't Do

- No push notifications in v1 (deferred; opt-in overlap alerts can be added if the team requests)
- No separate manager view — EM sees exactly what engineers see
- No time tracking, sprint planning, or performance metrics
- No public access
