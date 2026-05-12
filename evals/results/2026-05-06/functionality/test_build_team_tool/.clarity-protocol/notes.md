# Notes

[To be determined. Guiding principles and cross-phase observations will be added here as the project develops. Items tagged `[for: <phase>]` are actionable observations for a specific phase; untagged items are permanent guiding principles.]

## Team Status Dashboard

Problem clarification, solution design, failure analysis, and architecture completed in one session.

Key design philosophy: the tool must feel like the team's coordination layer, not management's visibility tool. That framing governs everything from the snapshot URL design to how blockers are surfaced.

The most important non-technical action before launch: establish the team norm around "blocked" status in 1:1s. The tool makes blocker under-reporting more consequential (false green instead of nothing), so psychological safety around surfacing blockers needs to be in place before the dashboard goes live.

Marcus is the engineer building this. Walk him through collision deduplication logic and the heartbeat check before he starts — both are easy to skip in an initial build and both are first-class features.
