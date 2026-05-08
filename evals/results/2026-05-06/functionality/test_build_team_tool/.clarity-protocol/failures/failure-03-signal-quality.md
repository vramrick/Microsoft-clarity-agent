# Failure: Signal Quality

## Summary

The dashboard runs and cards appear current, but their content is misleading — the tool gives the team lead and engineers a false sense of coordination coverage. Unlike Failure 1 (stale cards), these cards have recent timestamps and don't trigger staleness warnings. They simply don't convey the real work happening. The tool exists and appears healthy; the coordination failures it was meant to prevent happen anyway.

Variants:
- Vague task descriptions hide real work ("misc cleanup" when touching auth or billing)
- Tag list doesn't match engineers' mental model → wrong or missing component tags → collision detection silent
- Collision detection fires so often for habitual co-workers that alerts are ignored (notification fatigue)
- Primary-focus norm never established → cards show project epics or to-do lists instead of current focus

## Failure Chain

1. Engineer picks up work in a shared or sensitive area and opens the update modal.
2. They can't find the right component tag (the list uses different terms than the engineer does), or they write a description that's technically accurate but not informative ("refactoring"), or they're unsure what "current task" means and post their backlog.
   - *Intervention (prevention):* Tag list is co-designed with engineers at launch — use the terms they already use for codebase areas.
   - *Intervention (prevention):* Team norm established explicitly at launch: "your card should tell a teammate what they'd need to know before touching the same area."
3. Card is submitted. Timestamp is fresh. No staleness indicator fires.
4. The card does not reflect the actual work or area of risk. Collision detection doesn't fire because the component tag is absent or wrong. The dashboard looks fully up to date.
5. A teammate enters the same area without awareness. **harm begins** — same overlap failure as the original 2am incident, but now the tool exists and silently failed to prevent it.
6. The overlap manifests at code review or as a production incident.
   - *Intervention (mitigation):* Team lead can catch signal quality issues in standup by comparing cards to what engineers say they're working on — discrepancies are flags.
7. Overlap is discovered and addressed. **harm ends** — but trust in the tool as a coordination layer is damaged.

**Note:** This failure is harder to detect than Failure 1 because there are no staleness signals. A dashboard full of recent-timestamp but misleading cards is indistinguishable from a healthy dashboard without reading the content carefully.

## Observations

- **Severity:** High — potentially worse than Failure 1 because it provides false assurance. A visibly stale dashboard makes people distrust it; a misleading-but-current dashboard is trusted when it shouldn't be.
- **Related failures:** Failure 1 (dashboard integrity) is about cards being stale; this is about cards being wrong while appearing current. Both end in the same harm. Failure 5 (blocker under-reporting) is a special case of signal quality driven by a different cause.

## Intervention Points

### Prevention
- Tag list co-designed with engineers at launch (not imposed top-down)
- Team norm established explicitly: "current task = what a teammate should know before touching the same area"
- Collision detection deduplication: if two engineers are always co-located in the same area, suppress repeat alerts after N days and only re-alert on new combinations

### Detection
- Team lead spot-checks card descriptions against standup reality; discrepancies surface the problem
- Collision alert fatigue tracked: if the same pair fires the same alert repeatedly, flag for the team lead as a potential noise problem

### Mitigation
- Team lead can ask engineers directly when a card description looks off — the dashboard surfaces the conversation prompt even if the content is imperfect

### Recovery
- Update the tag list to match how engineers actually think about the codebase
- Re-establish the team norm if it drifts; retrospective on any incident where a vague card contributed

---

## Management Plan

[Not yet developed. Run failure management to develop a plan for this failure mode.]
