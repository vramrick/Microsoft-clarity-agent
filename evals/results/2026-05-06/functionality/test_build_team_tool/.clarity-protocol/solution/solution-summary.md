# Solution Summary

## What We're Building

A lightweight team status dashboard: a web app where each engineer maintains one card (current task, status, component tags, optional blocker) and the whole team can see everyone's cards at a glance. The primary write path is a Slack slash command (`/status`) that opens a pre-filled Block Kit modal — so most updates take one interaction without leaving Slack. A background scheduler fires daily weekday nudges for anyone who hasn't updated since the previous workday, with a heartbeat email fallback if Slack stops working.

**Stack:** FastAPI (Python), React + TypeScript, PostgreSQL (existing instance), deployed on AWS as a single Docker container behind Nginx. Slack OAuth is the only identity provider — no separate user list.

## What It Feels Like to Use

An engineer picks up a new task. They type `/status` in Slack, see their current card pre-filled, change the task description and component tags, hit submit. Twenty seconds. If they tagged something as `billing` and a teammate is also active in `billing`, they immediately get a DM: "Heads up — Sarah is also working in billing right now." They check in with Sarah. The 2am incident doesn't happen.

The next morning, the team lead opens the dashboard before standup. Seven cards, sorted stalest-first. An amber badge flags any card over 48 hours old. One person is blocked; the blocker description is right on the card. Standup covers depth rather than basics.

Before a VP sync, the team lead opens `/snapshot/{token}` — three sections, no login required: In Progress, Blocked, Recently Done. The VP gets a real answer without anyone reconstructing it from memory.

## How It Addresses the Problem

The 2am overlap incident is addressed by collision detection: tagging a sensitive component triggers an immediate Slack DM when another engineer is active in the same area. The duplicated investigation problem is addressed by passive visibility — anyone can check the board before starting work. The stale mental model problem is addressed by the snapshot view, which reflects live data without requiring the team lead to query anyone.

## Nonobvious Design Choices

**Monolith, not microservices.** Seven engineers, trivial data volume, one team maintaining it. One FastAPI process handles the REST API, Slack webhook handler, and background scheduler. No message queues, no separate cron service. Simpler to deploy, simpler to debug at 3am.

**APScheduler in-process for nudges, not AWS EventBridge.** Adds a small reliability dependency on the app process staying up, but dramatically reduces operational complexity. Acceptable tradeoff for an internal tool. If the process is down, cards will be visibly stale — the team lead notices without needing a separate alarm.

**Done state as a timed signal, not a terminal state.** Done automatically clears after 24 hours with a "what are you working on?" prompt. The UI shows a visible countdown. This makes using "done" to silence a nudge a conscious, transparent choice rather than a permanent escape — addressing a specific failure mode where done becomes a nudge-silencer rather than a real status.

**Collision deduplication.** The same (engineer_a, engineer_b, tag) combination only fires one alert per day, tracked in a `collision_notifications` table. Without this, two engineers who habitually work in the same areas would develop alert fatigue and ignore the signal when it matters.

**Heartbeat email fallback for Slack integration.** If the nudge job runs but sends 0 messages when stale cards exist, it emails the team lead via SES. Email is the fallback specifically because Slack may be the broken component. This team has direct prior experience with Slack integrations dying silently — this monitor is a first-class feature, not a nice-to-have.

**Curated tag list, co-designed at launch.** The 10–15 component slugs are defined by the team lead but should be validated with engineers before launch. Tags that don't match how engineers think about the codebase will be skipped or misused, disabling both filtering and collision detection. The admin settings page makes the list easy to maintain as the codebase evolves.

**Snapshot token for VP access, not a login.** The VP gets a long random token URL — no account, no expiry, no friction. The team lead can regenerate the token (from admin settings) if it's been shared too widely. This deliberately separates "sharing a snapshot with one person" from "granting someone ongoing access to the tool."
