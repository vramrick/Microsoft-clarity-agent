# Problem Statement

A 7-person engineering team lacks real-time visibility into who is working on what. The absence of a low-friction, persistent coordination layer causes three distinct failure modes: engineers accidentally work in overlapping areas without knowing it (leading to broken assumptions at integration time), engineers independently investigate the same problem (wasted effort that only surfaces at standup), and engineering leadership can't give accurate status answers to stakeholders without resorting to a stale mental model.

Jira exists but goes stale immediately — nobody updates it until sprint review. Slack is too ephemeral for coordination; things disappear. What's missing is something in between: structured enough to scan at a glance, lightweight enough that people actually keep it current.

## Why This Matters

The 2am incident is the clearest illustration of the cost: two engineers working in adjacent areas without knowing it, one's change breaking the other's untested assumption. The duplicated perf investigation and the incomplete VP answer both point to the same root cause — there's no shared, current picture of what the team is doing. The team lead's mental model is perpetually a week stale, and that has real consequences.

## Scope

**In scope:**
- Engineer-to-engineer coordination visibility (who's working on what, in what state)
- Flagging work that touches shared or sensitive areas (auth layer, billing pipeline, shared state across services)
- Team lead situational awareness, especially for management syncs
- Read-only snapshot access for the VP when requested

**Out of scope:**
- Sprint planning or ticket management (not a Jira replacement)
- Time tracking
- Replacing standup (this supplements it, giving standup a persistent foundation)
- Real-time executive monitoring (VP access is on-demand, not a live feed)

## Success Criteria

- No repeat of the 2am incident caused by invisible overlap — engineers working in shared/risky areas are visible to the team
- The team lead can open the dashboard before a VP sync and give an accurate, complete answer without relying on memory
- Engineers maintain their status without being nagged — updates happen naturally as part of picking up and completing work
- Standup becomes richer because the basics are already known, not more laborious
