## Turn 1

**User:**
Hi — I'm hoping you can help me work through something that's been bothering me for a few weeks. I own a cross-functional product team and I'm pretty confident our velocity has been declining over the last quarter. Stakeholders are starting to notice and complain, and when I sit in sprint reviews it just *feels* like we're shipping less than we used to.

I have some candidate interventions in mind but I want to make sure I'm picking the right one. Figured it was worth thinking through properly rather than just grabbing the first fix that sounds reasonable.

**Assistant:**
Good instinct to think before acting — the "grab the first fix" trap is real, especially when stakeholders are applying pressure.

A few things I want to understand before we dig into interventions:

**What does "velocity declining" look like concretely for you?** Is it story points, features shipped, time-to-merge, something else? And do you have a rough sense of *when* it started slipping — did it coincide with anything (a reorg, new hires, a big launch, a shift in tech stack)?

Also — when you say you have candidate interventions in mind, what are you considering? Even a rough list helps, because the right diagnostic depends partly on what you're already tempted to do.

## Turn 2

**User:**
Sure. Here's what I've got:

- **Points per sprint:** Q1 (6 sprints) averaged 38. Q2 so far (5 sprints) averaging 43.
- **Stories shipped per sprint:** Q1 averaged 9, Q2 averaging 7.
- **Time-in-progress for shipped stories:** Q1 averaged 4 days, Q2 averaging 7 days.

The stories-closing number and the cycle time are what's bothering me. Fewer stories closing, each one taking nearly twice as long — that reads as slower to me, regardless of the point totals.

On timing: I haven't identified anything material. No reorg, no new EM, no major tech changes. That's actually part of why I'm here — if there were an obvious cause I'd have a more obvious fix.

Candidate interventions I've been considering: tighter definition of ready, a stricter WIP limit, more focused retros, or more aggressive story decomposition. I'm genuinely not sure which lever to pull.

**Assistant:**
There's something interesting buried in your numbers. Points went *up* — 38 to 43 — while stories went down and cycle time nearly doubled. That means stories got bigger on average: ~4.2 points each in Q1, ~6.1 in Q2. A 45% increase in average story size.

That reframes the question. The team isn't necessarily slower — they may be working on larger chunks. Which makes **story decomposition** look like the most data-supported lever of your four options, before we even discuss WIP or readiness.

But I want to rule something out before anchoring there: **are stories carrying over sprint boundaries at a higher rate in Q2?** If a lot of in-progress stories are bleeding into the next sprint, that would inflate both cycle time and story size metrics in a way that decomposition alone wouldn't fix — WIP limits would be the right call instead.

And one more: **has the work itself gotten more complex**, or are stories being *written* larger? If you moved from feature work to platform/infrastructure work, or took on a more technically uncertain product area, the size increase might reflect reality rather than a scoping habit.

## Turn 3

**User:**
Okay, that's a reframe I didn't make myself — I was so focused on the story count and cycle time that I didn't do the division. I'll sit with it.

On your questions: I don't have carryover rate tracked explicitly, but gut says it's up — I see more stories in "in progress" at sprint close than I used to. So that's probably a real signal.

On whether the work got more complex versus stories being written larger — honestly, this is where it gets uncomfortable. I've noticed our backlog grooming meetings have been running long lately, and writing stories has felt harder. I chalked it up to a more mature product with more edge cases, but I haven't connected that to the size trend you're pointing out. It could be that we're not decomposing well rather than the work genuinely being harder.

So maybe the framing isn't "velocity is declining" but "story scope has inflated and that's creating the symptoms I'm seeing." Is that where you're landing?

**Assistant:**
Yes — that's where I'm landing, and I think it's a more useful frame than "velocity is declining."

One refinement worth making: even if the work *has* gotten genuinely harder (more edge cases, more mature product surface), that doesn't justify larger stories — it means decomposition has to work harder. Complexity is a reason to decompose more aggressively, not a reason to accept bigger chunks. So "harder work" and "poor decomposition" aren't mutually exclusive; they compound.

Given everything, here's how your four interventions look to me now:

| Intervention | Relevance |
|---|---|
| **Story decomposition** | Primary lever — directly addresses the root cause |
| **Definition of ready** | Complementary — add a "too large to start" criterion and it catches bloat before it enters the sprint |
| **WIP limits** | Addresses the carryover symptom but not the cause — worth adding, but won't fix the underlying problem |
| **More focused retros** | Indirect — useful for self-correction over time, but too slow to act as a primary fix |

My read: decomposition + a size check baked into your definition of ready is the core intervention. WIP limits as a forcing function alongside it. Retros as a monitoring mechanism, not a fix.

Before we move forward — does this match your read, or is there something about the team or the work I'm missing that would change the picture?

## Turn 4

**User:**
That matches my read, and the table is exactly the kind of clear prioritization I needed. The "too large to start" criterion in definition of ready is something I hadn't thought of explicitly — that's a practical addition I can implement immediately.

One thing I want to make sure I get right: how do I actually change decomposition behavior? I can put it on the retro agenda, I can talk about it in grooming, but in my experience "we should break stories down more" is advice that doesn't stick without a structural change. Do you have a view on what makes decomposition discipline durable rather than a one-sprint improvement?

**Assistant:**
Good question, and you're right to be skeptical of "talk about it more" as a fix. The reason decomposition advice doesn't stick is that it relies on habit change under time pressure — and grooming runs long precisely *because* the work is hard to scope. People default to writing the story that's in front of them.

What makes it durable is removing the social enforcement and replacing it with structural enforcement:

**The most reliable mechanism: a hard gate, not a guideline.** If your DoR says "no story over 3 points enters sprint planning," then the story *literally cannot be pulled* until it's been decomposed. The team stops debating whether to decompose and starts debating how. One rule replaces ongoing reminders.

**Make size visible on the sprint review dashboard.** Average story size next to velocity. Once the team sees it as a metric they own, they self-correct. It also defuses the "we're doing complex work" rationalization — the data either supports that or it doesn't.

**Invest once in decomposition patterns.** Teams often struggle because they don't know *how* to break things down, not because they lack motivation. A 30-minute session on concrete patterns — happy path vs. edge cases, CRUD splits, workflow steps, persona-based slices — gives people tools. That knowledge compounds over time in a way that repeated reminders don't.

The combination that tends to hold: hard size gate in DoR (structural) + size on the dashboard (visibility) + one decomposition patterns session (capability). The retro then becomes a place to catch regressions, not the primary enforcement mechanism.

The gate is the keystone. Without something that physically blocks large stories from entering the sprint, everything else is advisory.

## Turn 5

**User:**
The hard gate framing is the piece I was missing. "No story over 3 points enters sprint planning" is something I can actually put in the DoR document and hold to — it doesn't require me to remind people every two weeks.

The decomposition patterns session is also useful; I think you're right that the issue is partly capability. I'll schedule that before we roll out the gate so the team has the tools when the constraint kicks in.

This has been genuinely useful. I came in convinced I had a velocity problem and needed to pick a fix. I'm leaving with a different diagnosis and a clearer set of actions. Appreciate the pushback on the framing — I wouldn't have gotten there on my own with those numbers.

**Assistant:**
Glad it clicked. The sequencing you landed on — patterns session first, then gate — is exactly right. Give people the capability before the constraint, or the constraint just creates frustration.

Good luck with the rollout.
