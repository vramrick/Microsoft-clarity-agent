# Failure Modes

1. **[Dashboard Integrity](failure-01-dashboard-integrity.md)** (High) Cards go stale or contain false state — due to nudge habituation, using "done" to silence nudges, or forgetting to clear a resolved block — and engineers or the team lead make coordination decisions based on outdated data. The 2am overlap incident recurs; VP gets wrong answers; blocked engineers get no help. **No mitigation plan yet.**

2. **[Silent Operational Degradation](failure-02-silent-degradation.md)** (High) The Slack integration or nudge cron job breaks without surfacing any visible error. Nudges stop; updates stop; the dashboard goes stale while appearing functional. This team has prior direct experience with this failure pattern on other Slack integrations. Primary mitigation: daily heartbeat monitor that emails the team lead if expected nudges don't fire. **No mitigation plan yet.**

3. **[Signal Quality](failure-03-signal-quality.md)** (High) Cards are recently updated but misleading — vague task descriptions hide real work areas, wrong or missing component tags disable collision detection, or the primary-focus norm was never established and cards show project epics instead of current focus. The tool appears healthy but the coordination failures it was built to prevent happen anyway. Harder to detect than stale cards because timestamps look fresh. **No mitigation plan yet.**

4. **[Visibility Chilling Effect](failure-04-visibility-chilling-effect.md)** (Medium) Engineers learn the VP snapshot exists and optimize their cards for appearance — understating risk, avoiding "blocked," writing descriptions that sound good. The root cause is the VP visibility feature; the mitigation is explicit team communication about how and when the snapshot is used, not UI changes. **No mitigation plan yet.**

5. **[Blocker Under-Reporting](failure-05-blocker-underreporting.md)** (High) Engineers avoid marking "blocked" because of an existing trust/culture dynamic where surfacing problems feels risky. The dashboard shows false green on the most actionable signal. This failure predates the tool and is not fixable with a UI change — the intervention is how the team lead runs 1:1s and responds when blockers are surfaced. **No mitigation plan yet.**

## Cross-Cutting Patterns

**Shared intervention: make the real state visible, not just current.** Failures 1, 3, 4, and 5 all involve cards that look fine but aren't. The staleness indicators (48h warning, stale-first sort) address Failure 1 but not the others. Failures 3, 4, and 5 require human-layer interventions — team norms, 1:1 cadence, psychological safety — that no UI feature can substitute for.

**Pinch point: trust.** Failures 4 and 5 both hinge on whether engineers trust that the dashboard is a coordination tool for the team, not a surveillance tool for management. This trust is established by the team lead's behavior, not the system's design — but the system's design can undermine it (VP snapshot) or support it (framing, explicit norms at launch).

**Cascade relationship:** Failure 2 (silent degradation) can trigger Failure 1 (dashboard integrity) silently. Failure 1, if chronic in one engineer, can cascade to full adoption collapse. Failure 5 (blocker under-reporting), if unaddressed, makes the team lead's planning systematically overoptimistic.
