# Problem Statement

A 7-person remote engineering team (3 senior, 3 mid, 1 junior) lacks real-time visibility into what each person is working on. The team has standups, Slack, and a Linear board, but none of these provide a quick, current "here's what the team is doing right now" view. This gap has produced three concrete failure modes:

1. **Coordination incidents**: Two engineers working in adjacent areas unaware of each other caused a production incident (2am page) when one's change broke the other's assumptions.
2. **Duplicate work**: Two engineers independently debugged the same performance issue in parallel for half a day.
3. **Leadership visibility gap**: The engineering manager couldn't accurately answer "who's working on what" when asked by their VP, and had to reconstruct it from memory — incompletely.

The team wants a lightweight internal dashboard where anyone can post their current work, visible to the whole team. The primary job is engineer-to-engineer coordination; leadership visibility is a useful side effect, not the goal. The tool should not feel like surveillance.

## Why This Matters

Without this, the team risks repeated coordination failures (production incidents, wasted duplicate effort) and the EM lacks a trustworthy source of truth for leadership conversations. The existing tools — standups, Slack, Linear — are not designed to surface the current state of the team at a glance; they require active reconstruction.

A critical failure mode for the tool itself: if engineers stop updating it, a stale dashboard creates *false confidence* (worse than no dashboard). Staleness must be visible.

## Success Criteria

- No duplicate-work incidents over a 2-month window after adoption
- EM can answer "who's working on what" without reconstructing from memory
- Team is actively updating (updates per person per week is a proxy metric)
- **Failure signal**: team stops posting → tool gets pulled
