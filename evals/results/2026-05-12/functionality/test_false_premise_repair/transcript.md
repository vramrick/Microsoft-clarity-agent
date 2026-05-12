## Turn 1

**User:**
Hi — I'm hoping you can help me think through a problem I've been sitting with for a few weeks. I'm a PM, and my instinct is that my engineering team's velocity has been declining over the last quarter. Stakeholders are starting to complain about shipping pace, and in sprint reviews it just feels like we're closing less than we used to. I want to figure out what's driving it and what I should actually do about it.

**Assistant:**
That's a meaty problem — and the fact that you're feeling it before you have a crisp explanation is pretty common. Let me start taking some notes while we talk.A few things would help me understand the shape of the problem:

**Do you have any data to work from**, or is this mostly pattern recognition so far? For example — story points per sprint, ticket close rates, cycle time, anything like that. Even rough numbers matter; I want to know whether we're diagnosing a confirmed trend or validating an instinct.

And separately: **has anything changed on the team or in the environment over the last quarter?** New people joining or leaving, a big architectural shift, a new process the org imposed, a particularly hairy project — anything that could be load-bearing in the explanation.

## Turn 2

**User:**
Yeah, I have data. Here's what I've pulled together:

- **Q1** (6 sprints): averaging 38 points/sprint, 9 stories shipped/sprint, stories averaging 4 days in progress
- **Q2** (5 sprints in): averaging 43 points/sprint, 7 stories shipped/sprint, stories averaging 7 days in progress

So points are technically up slightly, but we're closing fewer stories and each one is taking longer. That's the pattern that feels like a slowdown to me.

On the environment question — honestly, nothing material that I've identified. No new EM, no major framework change, no acute cross-team dependency issue blowing up. That's part of why I'm here; the numbers feel like they should explain themselves and I can't fully close the loop.

**Assistant:**
This data is really useful — and I think it's telling a more specific story than "the team is slower." Let me share what I see.The numbers point to something specific: your stories are getting bigger, not your team getting slower. In Q1, the average story was ~4.2 points; in Q2 it's ~6.1 points — about 45% larger. If the team were just moving more slowly, you'd expect points to drop too. But they went up. The team is doing more work per sprint by their own measure, but closing fewer discrete units.

That shifts the diagnostic question from "why is the team slower?" to something more like: **why are stories getting larger and taking longer to close?** A few distinct possibilities:

1. **Story sizing drift** — stories are being written bigger than before (scope crept in during refinement)
2. **Work complexity shift** — the nature of the work has genuinely gotten harder (more interconnected systems, more unknowns)
3. **Technical debt drag** — each story carries hidden rework overhead that didn't exist before
4. **WIP creep** — engineers are juggling more in-flight work, so individual stories stall mid-sprint
5. **Estimation drift** — the team is inflating points while the actual work hasn't changed, masking the real picture

Do you have a sense of whether stories feel different at the *writing* stage, or does the size surprise everyone mid-sprint? That would help distinguish between story composition changing versus execution getting harder once work starts.

## Turn 3

**User:**
Okay, that reframe is actually landing. I hadn't put those two numbers together — I was just anchoring on "fewer stories, slower cycle time" and calling it a slowdown.

And to your question: yes, honestly, stories *have* felt harder to write lately. Backlog grooming has been running long. I've noticed my designer and the engineers going back and forth more during refinement than they used to. But I hadn't connected that to the velocity question — I was treating it as a separate annoyance.

So if I take your framing seriously: the problem isn't that the team is executing slowly, it's that we're feeding them larger, murkier work. That would explain the cycle time increase too — stories that are fuzzier at the start probably generate more mid-sprint clarification loops.

That changes what I should actually fix. What are you seeing as the highest-leverage intervention given that diagnosis?

**Assistant:**
The reframe holds up well, but let me flag one thing before you start changing processes: we have a strong hypothesis, not a confirmed diagnosis yet. The two patterns — murky stories and longer cycle times — are consistent with each other, but it's worth spending 20 minutes pulling up 5-6 stories from Q2 and checking *where* the time actually went. Did stories stall at the start (clarification loops)? In review? At the end waiting for deployment? The answer slightly changes the fix.

That said, assuming the hypothesis holds, here's where I'd focus:**Highest-leverage intervention: raise the "ready for sprint" bar.**

Right now it sounds like stories are entering sprints with open design questions, which means engineers are doing clarification work *during* the sprint that should have happened before it. The fix is a Definition of Ready — a short, explicit checklist a story must pass before it's sprint-committable. The essentials:

- Acceptance criteria written and agreed upon by engineer + PM
- Design finalized and linked (no open design questions)
- Story can be completed by one engineer in 3 days or fewer; if not, split it

The designer/engineer back-and-forth you're seeing in grooming is actually useful signal — it means the gap is visible. The intervention is to move that conversation *earlier*, before refinement, so by the time a story hits grooming it's a sizing and scoping conversation, not a design conversation.

**Secondary: fix the design → engineering handoff timing.**

It sounds like design work and engineering intake are happening in the same meeting. Those need to be two separate gates: (1) design complete, reviewed by PM, and (2) engineering-ready, meaning acceptance criteria written and story sized. Right now you're doing both at once, which is why grooming runs long.

**What I'd hold off on:**

Don't touch points-based velocity targets or sprint commitments yet. If the root cause is story quality, fixing that will naturally bring cycle time down and story count up — you don't want to layer on process pressure while the underlying cause is still resolving.

Is the team aware that this pattern is happening, or have they been experiencing it without the data framing you just got?

## Turn 4

**User:**
The team knows grooming has been painful — that's been a visible thing. But I don't think they've seen the data framed this way. They've probably felt the "stories are getting fuzzier" problem without having the numbers to confirm it isn't an execution issue on their end. That's actually a meaningful distinction, because if they've been wondering whether *they're* the problem, showing them this framing could help.

The audit you're suggesting before I change anything makes sense. I'll pull a sample from Q2 and trace where the time went.

On the Definition of Ready — I've had that on my candidate list, but I'd been thinking about it as a WIP / discipline problem. Framing it as a "design conversation before engineering intake" problem makes it feel more surgical. The two-gate structure you described is cleaner than what I had in mind.

One question: how do I bring this to the team without it landing as "PM is saying your stories are bad"? I own the backlog, so some of this is on me. I want the conversation to be diagnostic, not blame-adjacent.

**Assistant:**
The framing question is actually the most important thing you've asked so far, and you're already halfway there by owning that the backlog is yours.**Lead with the data, and lead with what it exonerates.** Before you propose anything, show them the numbers. "Points are up, stories are bigger, cycle time is longer — this isn't an execution problem. You're working harder, not slower." That lands differently than "here's the new process I want to try." It also sets up the conversation as diagnostic rather than corrective.

**Own your share explicitly, early.** Something like: "I own the backlog, and I think a big part of this is that stories have been arriving at sprints before they're actually ready. That's on me and design more than it is on you." Saying this before anyone asks diffuses the blame question entirely — and because it's true, it'll land as honest rather than performative.

**Don't walk in with the solution pre-decided.** Bring the diagnosis, not the prescription. Ask them to validate your read first: *"Does this match what you've been experiencing?"* Engineers almost always have a sharper view of where work actually stalls than the PM does from the outside. If you propose the two-gate structure after they've confirmed the diagnosis, it becomes a shared conclusion rather than a PM imposing a process.

**Venue matters.** This probably warrants its own conversation — not a retro item, which can feel routine. A focused 45-minute session with the team lead, maybe your designer, framed as "I want to show you what I've been looking at and get your read" is the right weight.

The thing that'll make or break it is whether they feel like they're helping you figure out the solution or receiving a decision you've already made.

Is there an EM in the picture you'd want to loop in beforehand, or are you running this team more directly?

## Turn 5

**User:**
Yes, there's an EM — we work closely. I'd definitely loop her in before bringing this to the team. She'll want to know the framing ahead of time, and honestly she'll have useful context on whether any of this matches what she's been hearing from engineers in 1:1s.

I think the move is: show her the data and the diagnosis first, get her read, then run the team session together. That also means it's not just me standing up and explaining a process change — she can co-own it.

This has been genuinely useful. I came in thinking I needed to pick between WIP limits, tighter retros, or a Definition of Ready, and I would have been solving the wrong problem. The reframe is the thing I needed.

**Assistant:**
That's the right sequence — EM first gives you a reality check and a co-presenter, which changes the dynamic entirely.Good. Here's what you're walking away with:

**The diagnosis:** This isn't an execution slowdown — it's a story quality problem. Stories are ~45% larger than Q1 and arriving at sprints with open design questions, which generates clarification loops that inflate cycle time.

**The immediate actions:**
1. Audit 5-6 Q2 stories to confirm where time is actually going (validates the hypothesis before you change anything)
2. Brief the EM first — share the data, get her read and any 1:1 signal she has
3. Run a joint team session framed as diagnostic, not prescriptive
4. Implement a two-gate Definition of Ready: design complete before engineering intake, stories splittable to ≤3 days

**What not to do:** Don't touch velocity targets or sprint commitments while the underlying cause is still resolving.

If you want to come back and think through the stakeholder narrative — how to talk about this with leadership while the fix is in flight — or work through what the Definition of Ready should actually say, that'd be a natural next step here. Otherwise you have what you need to move.
