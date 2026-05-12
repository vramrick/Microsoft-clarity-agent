# Team Radar — Engineering Brief

## Problem

Our team lacks a shared, real-time view of who's working on what. This has caused concrete failures: a production incident where two engineers made conflicting changes in adjacent areas, half a day of duplicated debugging on the same perf issue, and an inability to answer "who's working on what" for leadership without reconstructing it from memory.

Standups, Slack, and Linear don't solve this — they require active reconstruction. We need one place that answers the question at a glance.

## What We're Building

A lightweight internal web dashboard — **Team Radar** — where each engineer posts a daily status update and can see the whole team's current state. Primary job is engineer-to-engineer coordination; leadership visibility is a side effect.

**Core features (v1):**
- Dashboard: one row per engineer, showing current task, codebase area, status, and blocking note
- Area filter: prominent; lets you see "everyone in payments" instantly
- Adjacency callout: dashboard highlights when two people are in the same area; on-post warning if you pick an area a colleague is already in
- Staleness indicators: entries >24h old flag as stale; "in progress" entries >3 days flag as stagnant — visual only, no auto-expiry
- Person drill-down: last 3–5 completed items per engineer (async standup context)
- Update form: area picker (fixed admin-managed list), free text, status, optional blocking note, optional Linear link — under 60 seconds to post

**Explicitly out of scope:** task management, time tracking, performance metrics, manager-only views, push notifications (deferred).

## Stack

- **Backend:** Node.js / TypeScript (Express)
- **Frontend:** React (single page)
- **Database:** Postgres on RDS
- **Auth:** GitHub org OAuth — no new credentials
- **Deployment:** ECS (single task), behind ALB. Fits the existing ECS/RDS pattern.

## Data Model

Three tables:

```sql
users         — github_id, name, avatar_url, role (member | admin)
areas         — slug, label, display_order  (admin-managed fixed list, ~10–15 at launch)
status_entries — user_id, area_id, description, status, blocking_note, linear_url,
                 created_at, updated_at
```

**Key rule:** Each new task = new row. Edits to an existing entry update in-place. "Current" status per user = most recent row. History is free. Staleness computed from `updated_at` at query time — no background jobs.

## API (8 endpoints)

```
GET  /api/dashboard          All users + current entry + adjacencies (main view)
GET  /api/users/:id          User's current entry + last 5 completed (drill-down)
POST /api/status             Create new status entry (authed user)
PATCH /api/status/current    Edit current entry in-place (authed user)
GET  /api/areas              All areas
POST /api/areas              Admin: add area
GET  /api/auth/github        Start OAuth
GET  /api/auth/callback      OAuth callback → session → redirect
```

`GET /api/dashboard` returns an `adjacencies` array computed server-side — the frontend reads it directly to render overlap badges and on-post warnings; no client-side overlap detection needed.

## Known Limitation

Staleness uses calendar time in v1. An entry will show stale Monday morning if the engineer didn't update Friday afternoon. This is **informational, not an alarm** — treat it as "worth checking in," not a problem. Workdays-aware logic can be added if the team finds it noisy.

## Estimate

2–3 engineer-weeks, consistent with the scope. No novel technical challenges.
