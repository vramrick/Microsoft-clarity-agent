## Turn 1

**User:**
Hey — I need to ship Workflow Automation V2 by Friday and I'm trying to nail down the final week. Specifically looking for help on: scope cuts to make sure we actually land it cleanly, what to say at the all-hands next week, and a CSM enablement plan so the field can position it well. Can you help me work through all three?

**Assistant:**
Good, this is a meaty launch week problem — scope, narrative, and field enablement all at once. Before I can help you make the right cuts and craft the right story, I need a bit of context:

1. **What's actually in V2?** What are the headline features — and what's the stuff that's "almost done but not quite"?

2. **What's the current risk picture?** Anything you're privately worried about not landing by Friday?

3. **Who's at the all-hands?** Employees only, or does it include customers/partners? And what's the mood — is V2 a big deal internally, or has it been a long time coming with some frustration along the way?

4. **CSM context:** How many CSMs, and are they starting from zero on V2 or do they have partial context already? Is the ask "explain what's new" or more "help them have consultative conversations" with customers?

The answers will shape everything — scope cuts especially depend on what you can defer without breaking the story.

## Turn 2

**User:**
Okay, here's where we are:

**What's in V2:** The core is a multi-step workflow builder — users can chain more than one trigger-action pair, with conditional branching (if/else logic). On top of that we added a visual canvas so you can see the flow as a diagram. The "almost done" stuff is mostly the canvas — the underlying logic engine is solid but the canvas has some rough edges, specifically around how it renders complex nested branches. It works, it's just not pretty.

**Risk picture:** The canvas rendering is my main worry. It degrades on workflows with more than ~4 branch levels. Not broken, just ugly. The branching logic itself I feel good about.

**All-hands:** Employees only, ~200 people. V2 has been talked about for a while so there's some "finally" energy, but also a couple of engineers who got pulled onto this from other projects, so I want it to land well.

**CSMs:** About 15 CSMs. They have high-level awareness but no hands-on time yet. The ask is more consultative — they need to be able to talk to our larger accounts about what this unlocks, not just read changelog bullets.

**Assistant:**
Good, I have enough to start. Let me capture this and work through all three areas.Here's my take on all three:

---

## 1. Scope cuts

The key insight: **the logic engine is the product; the canvas is a viewer.** Don't let the viewer define the release.

**Recommended cut:** Constrain the canvas to workflows up to 4 branch levels, and document it explicitly — not as a bug, but as a deliberate scope boundary for V1 of the canvas. Something like: *"The visual canvas is optimized for workflows up to 4 levels of nesting. Complex workflows with deeper branching are fully supported by the logic engine and run correctly — the canvas view for those cases is coming in a follow-on update."*

This does three things:
- Keeps the canvas in the release (so you don't lose the visual demo moment)
- Reframes ugly rendering as a known constraint, not a defect
- Sets up a fast-follow story you can actually deliver

**Don't cut:** The branching logic itself. That's the headline — multi-step + conditionals is what customers have been waiting for. Don't soften that story.

**One question before you finalize:** Are any of your target launch customers likely to have workflows deeper than 4 levels in their initial use? If yes, you may want to flag that proactively in onboarding.

---

## 2. All-hands narrative

With "finally" energy and some team strain, the wrong move is a pure hype frame — it'll feel hollow to people who lived through the hard parts. The right frame is: **acknowledge the real, celebrate the durable.**

A rough structure:

> *"V2 has been in the works for a while, and I want to be honest about that — it was harder than we expected. [Brief, specific acknowledgment of what was hard.] What came out of that is a workflow engine we're genuinely proud of. Here's what it actually does for customers…"*

Then: concrete customer value (what they could never do before), a quick demo of the happy path, and a specific thank-you to the teams who got pulled in — named if possible.

Close with: *"We're shipping Friday. Here's what the next 30 days look like."* People want to know what happens after the release, especially if they sacrificed other work for it.

**What I need from you to sharpen this:** What's one real customer workflow that V2 enables that V1 couldn't handle? That becomes the demo/anchor story for the all-hands.

---

## 3. CSM enablement

For consultative positioning, CSMs need three things: the value story, the qualifying questions, and the objection responses. Changelog bullets give them none of those.

**Suggested structure for a CSM enablement doc:**

1. **The V2 pitch in one sentence** — what it is, for whom, why now
2. **What V1 couldn't do / what customers complained about** — the "before" picture
3. **Three customer personas / use cases** for larger accounts (with example workflows)
4. **5 discovery questions** to open a V2 conversation with an existing customer
5. **Top 3 objections + responses** (e.g., "we're already using Zapier," "we tried automations before and they broke")
6. **Known constraints** (the canvas limitation) — so they're not caught flat-footed

I can draft this entire document if you can give me: What are the 2-3 most common automation workflows your larger customers try to build? And what's the one objection your CSMs hear most often on automation features?

---

Want to tackle these in order, or is there one that's most urgent right now?

## Turn 3

**User:**
This is helpful, the scope framing especially — I like "the logic engine is the product, the canvas is a viewer." That's actually how I'm going to pitch the cut internally.

To your questions: for the all-hands anchor story, the best example I have is an HR onboarding workflow — right now customers have to build 4 separate automations to handle new hire setup, and V2 lets them do it as one flow with branch logic for different employee types. It's clean and concrete.

For CSM stuff: the two most common workflows are that HR onboarding use case and approval routing (manager approves → notify → escalate if no response). The top objection is "we already have a workaround" — most power users have duct-taped together multiple V1 automations.

But — and I've been trying not to think about this too hard — I keep feeling like we should have done more discovery before building this. The strongest signal we have came from our CSMs, not directly from customers. And honestly the branching and the canvas both got added during the build based on internal calls, not customer research. I'm not saying we got it wrong, but... is that going to be a problem?

**Assistant:**
That concern is worth sitting with, not suppressing. Let me be honest with you about it.**The honest answer:** It's a real risk, but not a catastrophic one — and you can do something about it this week.

Here's how to think about it clearly:

**What you actually have:** CSM signal is real signal, just filtered. CSMs tell you what customers *complain about*, which skews toward workarounds and friction, not toward what would genuinely change how someone works. The HR onboarding and approval routing use cases are concrete enough that they're probably right. The canvas — added mid-build, currently rough — is the part most consistent with "we built what sounded good internally."

**The "workaround" objection is the key tell.** If your power users already have duct-taped V1 automations that work, V2's value isn't "easier" — it needs to be "enables things you literally couldn't do before." The HR onboarding example holds up there (4 separate automations → one coherent flow). Approval routing with escalation probably does too. But you should stress-test that framing this week, not discover it's wrong from a customer call after launch.

**What you can actually do before Friday:**

1. **Use CSM enablement as a forced validation pass.** Get 3-4 CSMs on a 45-minute call and walk through the value story. Not a training — a stress test. Tell them: "Push back on anything that doesn't match what you actually hear from accounts." You'll learn fast whether the story holds.

2. **Identify 2-3 anchor customers** who already have the duct-tape problem and get them hands-on this week — even a single session. Their reaction tells you more than any internal review.

3. **Design the launch to be a learning instrument.** Ship Friday, but build in a 2-week feedback sprint. Instrument for the specific question: do the "I have a workaround" accounts actually convert, and if not, why? That's the discovery you should have done earlier — you can run it as a tight post-launch loop instead.

**For the all-hands:** Don't pretend the discovery was rigorous. The "finally" energy means your team knows this build was hard and sometimes uncertain. Owning that you shipped on your best current signal and are committed to a tight feedback loop post-launch reads as credible leadership, not weakness. The alternative — overselling confidence you don't have — tends to come back around when the first customer feedback hits.

The discovery gap is real, but the practical question now is: how do you use this week to pressure-test before Friday and learn fast after? Want to work through the CSM enablement doc with that dual purpose in mind — both enabling the field *and* using them as a validation instrument?

## Turn 4

**User:**
Okay, this is the conversation I needed to have and have been avoiding. The CSM-as-validation-instrument framing is smart — I can actually pitch that call this week as "help us sharpen the launch story" without it feeling like a fire drill.

The anchor customer idea I'm less sure about. Getting someone hands-on by Friday is tight and I'd hate for a rough session to spook an account right before we announce.

On the all-hands: I hear you, but I can't stand up in front of 200 people and say "our discovery was thin." I need something I can say honestly without torching confidence in the team or the product. Is there a version of that framing that doesn't read as an apology?

Yes, let's work through the CSM doc — and I want to build in those discovery questions you mentioned. If I can get the CSMs asking the right things in their account conversations this week AND post-launch, that's probably the fastest way to close the evidence gap.

**Assistant:**
Good calls on both. Forcing anchor customers this week is the wrong move — you're right that a rough session creates a story you don't want right before announce. Let me handle the all-hands framing first, then build the full CSM doc.

---

## All-hands framing (the honest, non-apology version)

The move is to reframe discovery as a continuous process — not something that should have been completed before you built, but something the launch itself advances. This is actually true.

Here's a version you could say out loud:

> *"We built V2 on the strongest signal we had: our CSMs, who between them talk to hundreds of accounts and hear the same friction over and over. New hire onboarding duct-taped across four automations. Approval chains that break when someone doesn't respond. The pattern was clear. What we're doing Friday is taking what we built from that signal and putting it in customers' hands — which is where you find out what's really true. That's not uncertainty. That's how this works."*

Then pivot to the team:

> *"This took longer than we planned, and some of you got pulled in from other work. I want to name that because it's real — [names if possible]. We got here because of that."*

Then close forward, not backward:

> *"We're shipping Friday. Here's what the next 30 days look like: [specific things — beta feedback program, first CSM-led customer calls, fast-follow for the canvas]. The launch is the starting line for the next phase."*

What makes this work: it positions CSM signal as legitimate (it is), treats the launch as intentional learning (it now is), acknowledges the team strain specifically, and ends with forward motion. No apology, no false confidence. The audience will feel the difference.

---

## CSM Enablement Doc

Let me draft the full document now.Here's what I've built. The full CSM doc is ready — here's the structure:

**Sections:**
1. One-sentence pitch (consultative, not changelog)
2. The before picture — V1 fragility as the setup
3. Two use cases with the V1 problem, V2 story, and opening question for each
4. **5 discovery questions** — written to open real conversations *and* tell you whether the value prop holds. Each one has a "listen for" note so CSMs know what signal to capture.
5. **What to report back** — explicit ask for CSMs to surface whether customers validate or push back on the "couldn't do this before" framing
6. Objection handling for "we already have a workaround" — the key move is agreeing the workaround works, then asking what maintaining it costs
7. Canvas constraint, scripted honestly
8. Prep checklist

The "what to report back" ask is your validation instrument — it gives you a reason to debrief CSMs after their conversations this week and after launch without it feeling like a research project.

**One thing to add before you finalize:** Is there a third use case beyond HR onboarding and approval routing? If CSMs are talking to larger accounts, a third example (ideally from a different business function) gives them more surface area. What's the third-most common workflow request you hear?

And practically: do you want me to help you draft the "help us sharpen the launch story" framing for the CSM call invite this week? That's a short piece but worth getting right.

## Turn 5

**User:**
The all-hands framing is exactly right. "The launch is the starting line" — I can say that and mean it. I'm going to use that almost verbatim.

Third use case: finance teams building invoice approval workflows. It comes up a lot with our mid-market accounts — they want to route based on dollar thresholds, different approvers depending on amount, escalation if overdue. Very similar pattern to the approval routing case but different buyer persona and different conversation entry point for CSMs.

Yes, please draft the CSM call invite. It needs to feel like I'm bringing them in as experts, not like I suddenly need to do discovery I should have done earlier. The "help us sharpen the story" framing you suggested is right — I just need the actual words.

**Assistant:**
Good — invoice approval added to the doc. Now the invite:

---

**Subject:** V2 launch Friday — 45 min to sharpen the field story

Hi all,

We're shipping Workflow Automation V2 on Friday. Before we do, I want to make sure the story lands well with your accounts — and honestly, you know those conversations better than anyone on the product side does.

I'd like to get 45 minutes with the group this week to walk through the positioning together. I have a draft value narrative and a set of use cases; I want you to push back on anything that doesn't match what you actually hear in the field. If something sounds off, or if we're missing the real objection, I'd rather find out now.

There's no prep required — just come ready to tell me where the story feels thin.

[Calendar link] — I'll have materials in advance so you're not walking in cold.

Thanks —
[Your name]

---

**Why this works:** "You know these conversations better than anyone" is both genuine and flattering. "Push back on anything that doesn't match what you hear" makes them the expert, not the audience. "I'd rather find out now" signals confidence, not panic. And "no prep required" lowers the bar to say yes.

One small thing to add if it fits your culture: a specific name or two in the invite ("especially want [CSM lead] and [whoever has the big accounts]") makes it feel less like a broadcast and more like you specifically want them.

---

Here's where we stand on everything:

| | Status |
|---|---|
| Scope framing | ✅ Done — "logic engine is the product" |
| All-hands narrative | ✅ Done — "the launch is the starting line" |
| CSM doc | ✅ Done — 3 use cases, 5 discovery questions, objection handling, canvas constraint |
| CSM call invite | ✅ Done above |

The CSM doc is saved at `files/csm-enablement-v2.md` in the session folder if you want to pull it out and edit it directly.

Anything you want to refine, or are you ready to go execute the week?

## Turn 6

**User:**
This is everything I needed. Honestly more than I came in expecting — I thought this was a tactical conversation and it turned into the strategic one I'd been avoiding.

The thing I'm taking away beyond the deliverables: "the launch is the starting line" isn't just an all-hands line, it's actually how I need to be running this. I'm going to set up a real debrief cadence with the CSMs after launch, not just hope feedback surfaces organically.

I'll send the invite today and send the CSM doc ahead of the call. Thanks for pushing on the discovery question — I needed someone to name it.

**Assistant:**
Good luck Friday. You came in with three tactical problems and left with a way to run the next phase — that's the right outcome.

The debrief cadence is the real thing to protect. It's easy to skip once the launch adrenaline fades. If you put it on the calendar before Friday, it'll happen. If you don't, it probably won't.

Come back after the all-hands if you want to work through what you heard and what it means for what's next.
