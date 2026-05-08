# Requirements

Any solution must:

## Functional Requirements

1. Engineers can post and update what they're working on, with a status (in progress / blocked / done).
2. Engineers can flag work as touching a shared or sensitive area (e.g., auth layer, billing pipeline, cross-service shared state). The set of "sensitive areas" is team-defined, not system-enforced.
3. The full team's current status is visible at a glance — scannable in ~30 seconds.
4. The dashboard provides a read-only shareable view suitable for showing to the VP on demand (not a live feed).
5. Engineers receive a nudge if they haven't updated their status in 24 hours.

## Non-Functional Requirements

### Performance
- No specific latency requirements; the team is small (7 people) and the data volume is trivial.

### Reliability
- Should be available when needed (before VP syncs, at standup). Data should persist — nothing ephemeral.

### Usability
- Update friction must be lower than the current workaround (a shared doc or Slack). If it's not significantly easier to use, it won't be maintained.
- The interface should be scannable — optimized for reading, not just writing.

### Security
- Access should be limited to the team by default; the VP read-only view is on-demand and intentionally shared, not always-on.

## Constraints

- **Team size**: 7 engineers. The tool doesn't need to scale beyond a small team.
- **Existing tools**: Must not require Jira integration or replace sprint planning — engineers already have workflows around those.
- **Adoption**: The team lead cannot enforce mandatory updates with authority alone; the tool must make updating feel natural enough that engineers do it voluntarily (or with a light nudge).
