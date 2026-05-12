# Failure: Dashboard Integrity

## Summary

Cards show outdated or inaccurate state, causing engineers and the team lead to make coordination decisions based on a false picture of the team. The tool exists and appears functional, but its data doesn't reflect reality. Affected stakeholders: engineers (don't see real overlap), team lead (wrong mental model, bad VP answers), indirectly engineers who share work areas with the stale card owner.

Variants:
- Nudge habituation: engineer dismisses nudge daily without updating
- Done-as-escape-hatch: engineer marks done to silence the nudge, not because the work is done
- Blocked-left-stale: block resolves but card isn't updated; or engineer stays blocked without updating
- One stale card poisons trust: chronically stale card causes others to stop trusting the board

## Failure Chain

1. Engineer's card reflects their current state accurately.
2. Something disrupts the update cycle: nudge is dismissed habitually; "done" is used to silence the nudge rather than mark real completion; block resolves but engineer forgets to update; engineer is overwhelmed and deprioritizes it.
   - *Intervention (prevention):* Make the update path as frictionless as possible — pre-filled modal means a single button press changes one field.
   - *Intervention (prevention):* Make the done state visibly time-limited in the UI ("expires in ~18h") so using it as an escape hatch feels transparent, not like a trick.
3. Card shows outdated state. The content may not look obviously wrong — "in progress on billing refactor" may still be true, just stale.
   - *Intervention (detection):* Explicit 48h visual warning on the card (distinct color or badge). Stale-first sort means the team lead sees the worst offenders immediately.
4. Engineers and team lead form decisions based on the card's stale content. **harm begins**
5. A teammate starts work in the same area without awareness, because the card showed no active risk flag. Or the team lead gives an incomplete answer to the VP. Or a blocked engineer receives no help because the block is invisible.
6. The coordination failure manifests — at code review, in a VP sync, or at the next incident.
   - *Intervention (mitigation):* Team lead sees stale cards prominently (stalest-first sort, 48h badge) and can follow up directly before the failure manifests.
7. Team lead follows up; engineer updates their card. **harm ends** — correct information restored, though any downstream effects (missed overlap, wrong VP answer) may not be recoverable.

**Cascade:** If one engineer's card is chronically stale, others gradually stop trusting the board overall → adoption collapse.

## Observations

- **Severity:** High — this is the core failure the tool was built to prevent. A stale dashboard is worse than no dashboard if people act on it.
- **Related failures:** Failure 2 (silent operational degradation) can trigger this cascade; Failure 3 (signal quality) is the parallel failure where cards are current but content is misleading.
- **Variants:** nudge habituation, done-as-escape-hatch, blocked-left-stale, chronically-stale-card-trust-collapse, roster drift (no admin UI to remove departed engineers — their orphaned cards read as stale indefinitely)

## Intervention Points

### Prevention
- Pre-filled update modal minimizes friction to the point where updating is the path of least resistance
- Done state shows visible countdown in UI ("expires in ~18h") — removes incentive to use done as an escape hatch
- Team norm established at launch: "update your card when you pick something up, and when you put it down"

### Detection
- 48-hour visual warning badge on cards (distinct from stale-first sort, which is ordering — the badge is a signal)
- Team lead can see at a glance which cards are stale before VP sync or standup

### Mitigation
- Stale-first sort means problematic cards are always at the top of the team lead's view
- Team lead direct follow-up (the dashboard makes the problem visible; the response is human)

### Recovery
- Engineer updates their card; staleness resolves immediately
- No automated recovery possible — requires human action

---

## Management Plan

[Not yet developed. Run failure management to develop a plan for this failure mode.]
