# Failure: Silent Operational Degradation

## Summary

A critical infrastructure component — the Slack integration, the nudge cron job, or the OAuth token — stops working without producing any visible error. Engineers receive no nudges; updates stop; the dashboard goes stale. Neither engineers nor the team lead know the tool has broken. The dashboard looks normal until the data is noticeably old. This team has prior direct experience with this exact failure pattern on other Slack integrations.

Variants:
- Slack webhook or bot token becomes invalid (app uninstalled, token revoked, workspace policy change)
- Nudge cron job errors silently after a deployment or configuration change
- Slack OAuth tokens expire, locking engineers out of the web app update path

## Failure Chain

1. Slack integration and cron job are healthy; nudges fire daily and engineers can update via slash command.
2. An external event disrupts the integration without producing a visible user-facing error: Slack workspace admin revokes the bot token, the cron job throws an uncaught exception after a deployment, Slack changes an API endpoint.
3. The failure is silent. Slash commands return a generic Slack error that engineers don't report ("the bot is having issues"). Nudges simply stop arriving — engineers notice the absence only if they were expecting the nudge.
   - *Intervention (detection):* Daily heartbeat check — if N nudges should have fired in the last 24-hour window but none did, send an alert to the team lead via email. Email is the fallback precisely because Slack may be the broken component.
   - *Intervention (detection):* On application startup and daily, validate Slack bot token and connectivity; log and alert on failure.
4. Engineers can't update via Slack (if slash command is broken) and don't, because the web UI is the fallback path most won't use. Or nudges stop, and without the prompt engineers don't update proactively.
5. Cards go stale → dashboard integrity failure (Failure 1) begins. **harm begins** — false coordination picture.
6. Team lead discovers the problem only when the dashboard is visibly wrong — typically after a coordination failure surfaces, or when a VP sync reveals stale data.
7. Engineering resolves the integration issue (token refresh, cron fix, bot re-installation).
8. Engineers re-update their cards. **harm ends** — though any coordination failures that occurred in the silent window are not recoverable.

## Observations

- **Severity:** High — prior experience on this team makes this a known and credible risk, not a theoretical one.
- **Related failures:** Directly triggers Failure 1 (dashboard integrity). The team has seen this before with other Slack integrations.
- **Variants:** webhook/token invalidation, cron failure, OAuth expiry

## Intervention Points

### Prevention
- Slack OAuth token refresh implemented on the backend (use refresh tokens, not just access tokens)
- Cron job health monitoring (dead man's switch pattern: job must check in; failure to check in triggers alert)

### Detection
- **Daily heartbeat monitor:** If nudges should have fired in the last 24h and none did, email the team lead. This is the primary mitigation — catches the failure within one workday.
- Slack integration status visible on a simple internal status page the team lead can bookmark

### Mitigation
- Web update path always available as fallback; team lead can manually prompt engineers if nudges stop

### Recovery
- Token refresh or re-installation of Slack app; re-run nudges for engineers whose cards are stale
- Documented runbook for "Slack integration is broken" — what to check, how to restore

---

## Management Plan

[Not yet developed. Run failure management to develop a plan for this failure mode.]
