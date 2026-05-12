# Failure: Rating System Dysfunction

## Summary

The platform's reputation engine — the key mechanism for differentiating quality writers — becomes unreliable. Two failure modes: rating inflation (editors give uniformly high scores to avoid awkwardness, making rankings meaningless) and retaliatory ratings (editors use low ratings to punish writers who assert their rights, chilling disputes and concentrating power). Either failure destroys the signal that editors pay subscriptions for.

Stakeholders harmed: editors (can't differentiate quality writers), writers (rankings misrepresent quality; or fear of retaliation suppresses legitimate grievances), platform (loses core discovery value).

## Failure Chain

1. Platform relies on editor ratings to rank writers and signal quality to other editors.
   - *Intervention point (prevention):* Rating system design should account for social pressure toward inflation and power-differential pressure toward retaliation.
2. **Branch A — Inflation:** Editors give 4-5 stars uniformly to avoid awkward interactions with writers they may work with again. Over time, almost all writers have near-identical high scores.
   **Branch B — Retaliation:** Editor receives dispute or complaint from writer. Editor submits a low rating as punishment. Writer receives low rating for asserting legitimate rights.
   - *Intervention point (prevention — inflation):* Forced distribution or comparative ranking ("rate this writer relative to others you've worked with")
   - *Intervention point (prevention — retaliation):* Blind rating window (ratings submitted but not published until both parties have rated, or after a cooling period following disputes)
3. Ranking signals become disconnected from actual quality. **Harm begins.**
4. **Inflation outcome:** Editors can no longer use rankings to find the best writers. Subscription value drops; editors stop relying on the platform's signal.
   **Retaliation outcome:** Writers learn that asserting rights causes ranking damage. Legitimate grievances go unreported. Power balance shifts dramatically to editors.
5. Discovery value erodes to levels comparable to generic platforms. Writers with legitimate complaints have no safe recourse. **Harm ends** only if the rating system is redesigned.

## Observations

- **Severity:** High — directly undermines the core discovery value proposition, and retaliation creates a hostile community environment.
- **Related failures:** Failure 4 (payment exploitation) — retaliation often follows payment disputes. Failure 1 (curation quality) — if ranking is meaningless, quality differentiation is lost.
- **Variants:** Rating inflation, retaliatory negative ratings

## Intervention Points

### Prevention
- Comparative/relative rating mechanisms rather than absolute scales
- Blind rating window: ratings only published after both parties submit, or after dispute cooling period
- Rating categories (quality, professionalism, communication) rather than single score — harder to game consistently

### Detection
- Statistical analysis of rating distributions per editor: flag editors with unusually low variance (always 5-star) or suspicious timing (low rating immediately post-dispute)
- Overall platform rating distribution monitoring: if median climbs above threshold, system is likely inflated

### Mitigation
- Rating adjustment/calibration by Chris for flagged patterns
- Dispute flag that triggers rating hold: ratings submitted during active disputes are held pending review

### Recovery
- Periodic rating recalibration if systemic inflation is detected
- Retroactive review of retaliatory ratings with correction option

---

## Management Plan


## Management Plan

### Strategy

Design the rating system to resist both inflation and retaliation from the start — these problems are much harder to fix once the culture is set. Use structural mechanisms (blind ratings, multiple categories, dispute holds) rather than relying on users to behave perfectly.

### Interventions

**Anti-inflation:**
- Multi-category ratings: rate separately on Quality, Professionalism, and Communication. Harder to uniformly inflate than a single score.
- Relative ranking prompt: after rating, editors see "How does this writer compare to others you've worked with?" — encourages calibration.
- Statistical monitoring: if an editor's average rating is >4.8/5 across all their writers, flag for calibration review.

**Anti-retaliation:**
- Blind rating window: ratings are submitted but not published until both parties have submitted, OR 14 days after project close — whichever comes first. Neither party can see the other's rating before submitting.
- Dispute hold: any project with an active formal dispute has ratings suspended until the dispute is resolved. Ratings submitted within 48 hours of a dispute opening are flagged for review.
- Chris can redact a rating with evidence of retaliation; redacted ratings are replaced with a neutral average so the writer's score isn't harmed.

**Long-term:**
- After ~50+ ratings per writer, introduce a comparative tier system based on statistical distribution, not raw averages — this automatically corrects for editor-specific inflation tendencies.

### Residual Risk

Some inflation will persist — it's a social norm that's hard to fully eliminate. The multi-category approach and relative comparison prompts reduce it significantly without adding excessive user friction.

### Monitoring

- Monthly: distribution analysis of ratings platform-wide; flag any editors with suspiciously low variance
- Dispute-adjacent rating audit: review all ratings submitted within 7 days of a dispute
