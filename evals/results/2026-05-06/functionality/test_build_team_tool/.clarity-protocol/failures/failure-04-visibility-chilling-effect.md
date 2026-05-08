# Failure: Visibility Chilling Effect

## Summary

The VP snapshot feature causes engineers to optimize their card content for appearance rather than accuracy. Once engineers believe (correctly or not) that their cards are visible to management, they understate risk, avoid the "blocked" status, and choose descriptions that read well. The dashboard looks healthy and current, but reflects what engineers want management to see — not what's actually happening.

Variants:
- Snapshot URL forwarded beyond the team lead (email chain, broader Slack channel, exec presentation)
- Engineers become aware the URL exists and assume it's always watched

## Failure Chain

1. Team lead generates a snapshot URL and uses it in a VP sync. The URL is shareable by design.
2. The URL is forwarded in an email or posted somewhere engineers can see it. Or engineers simply learn it exists and assume the VP is monitoring it regularly.
3. Engineers begin treating their card as a performance signal rather than a coordination tool. They avoid "blocked" status (looks bad), soften risk language, and post descriptions that sound productive.
   - *Intervention (prevention):* Team lead communicates explicitly: "The VP snapshot exists; it is used only when I'm asked; it is not monitored daily." Making this norm explicit reduces the chilling effect.
   - *Intervention (prevention):* Snapshot URL is clearly separate from the team dashboard URL — different domain or path — so engineers can see they're different things.
4. Cards appear current and optimistic. The real risk picture is hidden. **harm begins** — same downstream failure as Signal Quality (Failure 3): dashboard provides false assurance.
5. A blocked engineer gets no help because their card shows green. Or a coordination failure happens in an area that a card downplayed. Or the team lead notices discrepancies between card content and 1:1 reality.
6. Trust between the team lead and engineers erodes if the gaming is noticed. Or a coordination failure surfaces that the dashboard should have flagged. **harm ends** when the card is corrected and team norms are restored.

## Observations

- **Severity:** Medium — the team lead assessed this as lower risk than it appears, because VP access is on-demand and not a constant feed. The risk is real but manageable through explicit communication about how the snapshot is used.
- **Related failures:** Same downstream harm as Failure 3 (signal quality) and Failure 5 (blocker under-reporting). The cause is distinct — not friction or culture, but the tool's own visibility design.
- **Note:** The more insidious form of this failure is not engineers gaming cards, but engineers under-reporting blockers specifically — which is already captured as Failure 5.

## Intervention Points

### Prevention
- Team lead explicitly communicates at launch: the snapshot is used only when asked; it is not monitored; the dashboard is for the team's benefit, not management surveillance
- Snapshot URL regeneration is easy — old link can be revoked if it's been shared too widely
- Dashboard design reinforces that the tool is peer visibility, not management monitoring (framing, not just words)

### Detection
- Team lead notices discrepancies between card content and what engineers say in 1:1s — this is the primary signal
- Persistent "blocked" undercount relative to what the team lead hears directly

### Mitigation
- Direct conversation with the team; re-establish norms
- Regenerate snapshot token if the old one has been too widely shared

### Recovery
- Restore psychological safety around the "blocked" status; reinforce that surfacing blockers is valued

---

## Management Plan

[Not yet developed. Run failure management to develop a plan for this failure mode.]
