# Failure: Blocker Under-Reporting

## Summary

Engineers are reluctant to mark their status as "blocked" because they fear it signals incompetence or reflects poorly on them in a context where the team lead (and possibly others) can see it. They stay in "in progress" while effectively stuck. The team lead's picture of the team's real state is systematically optimistic on blockers — the most actionable signal in the dashboard is suppressed by a cultural dynamic that predates the tool.

This failure is distinct from Failure 3 (signal quality) and Failure 4 (visibility chilling): the cause is not tooling friction or management surveillance, but an existing trust/culture dynamic between engineers and the team lead that the tool makes more consequential by giving it a new surface.

## Failure Chain

1. Engineer hits a genuine blocker: waiting on infra, stuck on a design question, needs a code review, has a dependency on another team.
2. Engineer hesitates to mark "blocked." Reasons may include: fear of looking incompetent, uncertainty about whether this "counts" as a blocker worth surfacing, belief that they should solve it themselves first, or habit from a previous culture where surfacing problems had negative consequences.
   - *Intervention (prevention):* Team norm established explicitly: "blocked means you're waiting on something outside your control, not that you failed." This norm must come from the team lead's behavior, not just a stated policy.
   - *Intervention (prevention):* Team lead models psychological safety in 1:1s — when blockers surfaced there are quickly acted on, not noted with concern.
3. Card remains "in progress." Timestamp is updated (not stale). The dashboard shows no problem.
4. Time passes. The engineer is stuck but invisible. Nobody offers help because nobody knows. **harm begins**
5. The block either resolves on its own (possibly suboptimally — engineer made a bad decision to keep moving, or spent hours unblocking themselves that a quick conversation would have resolved), or surfaces in standup or at a missed deadline.
6. Team lead acts to unblock. **harm ends** — but the intervention was later than it could have been, and the pattern may persist.

**Cascade:** If this pattern is widespread, the team lead's picture of blockers is systematically optimistic. Planning decisions (sprint scope, deadline commitments, hiring needs) are made on a false premise.

## Observations

- **Severity:** High — the team lead identified this as an existing dynamic already visible in 1:1s. The tool introduces a new surface for this pattern but doesn't create it; however, the tool could make the pattern more consequential by providing false assurance that blockers would be visible.
- **Related failures:** Failure 4 (visibility chilling) shares a downstream harm but has a different cause — this is not about management surveillance but about the existing relationship between engineers and their team lead.
- **Key distinction:** This failure is not fixable with a UI change. The intervention lives in 1:1 cadence, team culture, and how the team lead responds when blockers are surfaced.

## Intervention Points

### Prevention
- Team lead establishes and models the norm: "blocked = waiting on something outside your control; surfacing it is the right move, not a sign of weakness"
- 1:1s structured to make it easy and low-stakes to surface blockers before they're visible on the dashboard
- Team lead acts quickly and visibly on surfaced blockers — the behavioral feedback loop that makes future surfacing feel safe

### Detection
- Team lead notices systematic absence of "blocked" status on the dashboard relative to what they hear in 1:1s — this discrepancy is the signal
- Standup reveals blockers that weren't on cards — pattern of late disclosure

### Mitigation
- Direct conversation in 1:1 when the team lead suspects someone is stuck but showing green
- Normalize asking "are you blocked on anything?" as a regular check-in, not an accusation

### Recovery
- Re-establish psychological safety if a negative response to a surfaced blocker has damaged it
- The tool itself cannot recover this — requires human action by the team lead

---

## Management Plan

[Not yet developed. Run failure management to develop a plan for this failure mode.]
