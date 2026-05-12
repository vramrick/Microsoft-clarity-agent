# Solution

## Approach

A lightweight web dashboard backed by a simple REST API and a Slack integration. Engineers maintain one card each — their current focus, status, component tags, and an optional blocker. The Slack slash command with a pre-filled interactive modal is the primary write path. The web view is the primary read path. A scheduled nudge keeps cards current without requiring discipline.

This approach was chosen over alternatives (a Slack-native bot with no web view, a shared doc, a Notion template) because it gives the team a persistent, structured, scannable surface that doesn't require leaving either Slack or a browser — whichever an engineer is already in.

---

## Data Model

```
engineers
  id               text  (Slack user ID, used as primary key)
  name             text
  avatar_url       text

cards
  engineer_id      text  FK → engineers.id
  current_task     text  (nullable — blank if nothing active)
  status           enum  in_progress | blocked | done
  component_tags   text[] (multi-select from curated list)
  blocker          text  (nullable — free text, only meaningful when status=blocked)
  previous_task    text  (nullable — populated when current_task changes)
  updated_at       timestamp

components
  slug             text  (e.g. "auth", "billing")
  label            text  (display name)
  is_sensitive     bool  (marks areas worth flagging in collision detection)

team_config
  snapshot_token   text  (long random string for VP read-only URL)
  timezone         text  (IANA tz string, e.g. "America/Los_Angeles")
  nudge_time       time  (default 09:00)
```

`previous_task` is updated whenever `current_task` changes — it surfaces as "recently completed" in the VP view without needing full history. No audit log or history table required for v1.

---

## API Surface

```
GET    /api/cards                  All cards, authenticated (web dashboard)
PUT    /api/cards/:engineer_id     Update own card; engineers can only update their own
GET    /api/components             Curated tag list
GET    /api/snapshot/:token        VP read-only view; no auth required
POST   /api/slack/command          Slash command endpoint (Slack → API)
POST   /api/slack/interactive      Modal submission (Slack → API)
GET    /auth/slack                 Initiate Slack OAuth
GET    /auth/callback              Slack OAuth callback
```

Authorization: Slack OAuth for all authenticated routes. Engineers can only write their own card; any engineer can read all cards.

---

## Write Path: Slack Modal

`/status` fires a Block Kit modal pre-filled with the engineer's current card values. Fields: current task (text), status (select), component tags (multi-select), optional blocker (text, enabled when status=blocked). On submit, the modal calls `POST /api/slack/interactive`, which validates and writes to the database.

The web edit view exposes the same fields and calls the same `PUT /api/cards/:id` endpoint. It's the onboarding path and fallback, not the daily driver.

Slack ↔ engineer identity mapping: Slack user ID is the primary key. On first Slack OAuth login to the web app, the engineer record is created or matched. No separate user provisioning needed.

---

## Read Path: Web Dashboard

**Team view** (authenticated): Card grid, sorted by `updated_at` ascending (stalest first). Filter by component tag. Each card shows name + avatar, current task, status (color-coded), component tags, last-updated timestamp, and blocker text if present.

**VP snapshot view** (`/snapshot/:token`): Three sections — In Progress, Blocked, Recently Done (previous_task). No timestamps, no edit controls. Header shows "as of [date, time]." URL is `/snapshot/<long-random-token>`, generated once and stored in `team_config`. Regenerating the token revokes the old link.

---

## Nudge Logic

A cron job runs daily at the configured nudge time (default 9:00am, team timezone), weekdays only.

Fire a Slack DM to any engineer whose `updated_at` is before the start of the previous workday. This catches:
- Cards not updated since yesterday (the normal case)
- Cards not updated over a weekend (Monday nudge catches Friday-or-earlier)

Status doesn't gate the nudge. `blocked` cards get the same 24h treatment — daily confirmation that the block is still active, not a longer grace period. `done` cards that haven't been updated are nudged with "what are you working on?" — the terminal state isn't permanent.

The nudge DM includes a single button: "Update now." Clicking it opens the pre-filled modal inline in Slack, so the entire update happens without leaving the DM thread.

---

## Phase 2: Collision Detection

When an engineer submits a card update, check whether any other engineer's active card shares a `component_tag` marked `is_sensitive=true`. If so, fire a Slack DM:

> "Heads up — you tagged this as `billing` and Marcus is also working in `billing` right now (Optimizing retry logic, in progress). Might be worth a quick sync."

This is a one-time notification per overlap instance, not a recurring one. It fires on write, so it catches the overlap the moment it becomes visible. This directly addresses the 2am incident: the engineer who tags work in a shared area is immediately aware there's someone else nearby.

Collision detection is straightforward to add once the curated tag list is in place — the data model supports it from day one.

---

## Key Design Decisions

**Primary focus only (not "log everything"):** Engineers post one current task. This is an intentional editorial constraint — it prevents the tool from becoming Jira. The norm ("post what matters most right now") is a team convention, not a system enforcement.

**Curated tags, not freeform:** A short team-maintained list of 10–15 component slugs. Prevents "auth" vs "authentication" drift, and makes collision detection tractable. The team lead owns the list.

**Slack OAuth as identity:** No separate user list. The Slack identity already exists and is trusted. Onboarding is "run the slash command" — the account is created on first use.

**No history table in v1:** `previous_task` captures the most recent prior task, which is sufficient for the VP snapshot's "recently completed" view. Full audit history can be added later if needed; it's not required to meet the success criteria.

---

## Failure Modes and Risks (Seed for Failure Analysis)

- **Cards go stale despite nudges** — if nudges become background noise, engineers dismiss them without updating. The tool becomes a misleading dashboard of outdated information, which may be worse than no dashboard.
- **Slack integration breaks silently** — slash command stops working or nudges stop firing, and nobody notices because nothing visibly breaks. The dashboard just goes stale.
- **Tag list doesn't map to real work** — engineers can't find the right tag, use the wrong one, or skip tagging. Collision detection misses real overlaps; the filter becomes useless.
- **"Primary focus" norm doesn't take hold** — engineers post the safe or easy answer, not the real one. The dashboard looks populated but doesn't reflect actual work.
- **VP snapshot creates perverse behavior** — if engineers know the VP is watching, they optimize their card for optics rather than accuracy.
