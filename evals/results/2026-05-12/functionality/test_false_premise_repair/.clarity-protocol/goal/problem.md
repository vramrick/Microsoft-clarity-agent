# Problem Statement

A PM's engineering team shows a pattern that looks like declining velocity but is more precisely described as: fewer stories shipped per sprint, longer cycle times, but slightly higher points per sprint.

**Q1 baseline (6 sprints):** 38 pts/sprint, 9 stories/sprint, 4-day avg cycle time → ~4.2 pts/story  
**Q2 current (5 sprints):** 43 pts/sprint, 7 stories/sprint, 7-day avg cycle time → ~6.1 pts/story

The key signal: points are UP ~13%, but stories are DOWN ~22% and cycle time is UP 75%. This means the team is completing roughly 45% larger stories on average. No obvious environmental cause has been identified (no EM change, no framework migration, no acute cross-team blocker). The root cause is unclear — story sizing drift, work complexity increase, technical debt accumulation, WIP creep, or estimation drift are all candidates. The PM wants to diagnose the actual driver and identify concrete actions.

## Why This Matters

Sustained velocity decline damages stakeholder trust, erodes team morale if left unaddressed, and risks missing important commitments. Acting without a clear diagnosis risks prescribing the wrong fix.

## Success Criteria

- Root cause of the pattern confirmed (via story audit tracing where cycle time is actually spent)
- EM aligned on diagnosis and framing before team conversation
- Team conversation lands as diagnostic, not blame-attributing — engineers co-own the solution
- A Definition of Ready implemented with a two-gate structure (design complete → engineering intake)
- Story count and cycle time trending back toward Q1 baselines within 2-3 sprints of process change
