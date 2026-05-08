# Team Status Dashboard

Engineering teams run on coordination, and coordination runs on knowing what people are doing. For most teams, that knowledge lives in someone's head — usually the team lead's — and it's always a little stale. Standup helps, but standup is a snapshot, not a live view. Jira exists, but nobody updates it until the sprint review.

This project is a lightweight team status dashboard: a shared whiteboard that stays current. Engineers log their current focus, flag when they're in shared or sensitive parts of the system, and the whole team can see it in 30 seconds. The primary way to update it is a Slack slash command that opens a pre-filled modal — fast enough that people actually do it.

The design directly targets three real failures: two engineers working in the same area without knowing it (solved by collision detection that fires a Slack alert the moment someone tags a shared component someone else is in), duplicated investigation work (solved by passive visibility — you check the board before you start), and stale answers to management questions (solved by a shareable read-only snapshot that doesn't require anyone to create an account).

It's not a Jira replacement. It's the thing that makes standup richer because everyone already knows the basics before they walk in.
