## Turn 1

**User:**
Hi — I'm hoping you can help me think through a research program I'm trying to scope. I run Customer Success at a B2B SaaS company, and we've got a churn problem I need to get a handle on. Gross logo churn has gone from about 7% to 11% over the last three quarters, and my COO asked me point-blank last week whether I actually know why we're losing accounts. Honest answer: not rigorously, no.

I have about 6 weeks before our annual planning cycle kicks off and I need to present a "churn plan." I want to design a proper research program — exit surveys, interviews with churned customers, cohort analysis of usage patterns, segmentation by persona and vertical — something I can actually defend. Can you help me scope that out and figure out what to prioritize?

**Assistant:**
Good context — let me write down what I know already, then ask a few things that will shape how we scope this.Good, I've got the rough shape of the problem captured. A few questions that will significantly affect how we scope this:

1. **What do you already suspect?** Before we designed anything — gut instinct, anecdotal signals, patterns your CSMs have noticed. Even rough hypotheses help us design the right research rather than fishing blindly.

2. **What data do you already have access to?** CRM (Salesforce, HubSpot?), product usage analytics (Mixpanel, Amplitude, Pendo?), support ticket history, NPS/CSAT scores? The cohort analysis piece depends heavily on what's already instrumented.

3. **How many churned accounts are we talking about?** Ballpark — 20? 200? This matters a lot for whether interviews are feasible vs. surveys doing more of the work.

4. **What does your CS team look like?** Specifically — do you have analysts who can pull data, or is that a cross-functional ask? And do you have bandwidth to run interviews yourself, or does someone else need to?

5. **What format does the churn plan need to be?** A slide deck to the COO? A written memo? And is the audience just internal leadership, or does this feed into board materials?

## Turn 2

**User:**
Good questions. Let me run through them:

On gut instincts: the three things I hear most from my CSMs are pricing pressure (a competitor came into our space about 18 months ago at a lower price point), onboarding friction for accounts that didn't get a dedicated implementation resource, and a feeling that some accounts never really got value from the core workflow features. But those are vibes, not data.

On data: I actually have a reasonable stack — product usage (feature adoption, DAU, session depth), support ticket history with sentiment tags, quarterly NPS (though response rate is only about 15%), and CRM notes from renewals and cancellations. The CRM notes are inconsistent quality — some CSMs are thorough, some write one line.

Churned accounts: roughly 40 over the last two quarters. No one has done a structured analysis of any of them.

Team/bandwidth: 4 CSMs plus me. I have an analytics partner I can pull in for the data side, but she's shared with the whole revenue team. I can run interviews myself — probably my best use of time honestly — but I can't do 40 of them.

Format: the COO wants a "churn plan" as input to annual planning. My assumption is a slide deck, probably 10-15 slides. It may roll up into board materials eventually so it needs to be defensible.

**Assistant:**
This is a well-formed problem with three real hypotheses to test — that's actually a strong starting position. Two more things before I can help scope the research properly:

1. **Do you have any read on which accounts churned?** Anything that stands out about the 40 — were they concentrated in a particular size band (SMB vs. mid-market?), vertical, acquisition cohort, or contract length? Even a rough "it feels like a lot of our smaller accounts" would be useful.

2. **What's your relationship situation with churned customers?** Can you reach them for interviews, or did some leave on bad terms? And how recent were the churn events — are there accounts from 6 months ago where the contact has moved on?

The reason I'm asking: these two things together determine whether we lead with qualitative (interviews) or quantitative (data) work — and whether we try to test all three hypotheses simultaneously or have to sequence them.

## Turn 3

**User:**
On which accounts: my gut says it skews toward the smaller end of our mid-market range — the 50-200 employee accounts. We also had a few in logistics and field services that felt clustered, but I haven't verified that. I genuinely don't know if that's signal or just where we have more accounts to lose. That's part of what I want to figure out.

On relationships: mixed. Some churned cleanly — contract ended, they told us why, no hard feelings. Probably 15-20 accounts in that bucket where I think we could get a conversation. Another chunk went quiet — renewals where the champion had moved on or the deal just kind of died. And a few where it was contentious, I wouldn't bother reaching out. My rough estimate is maybe half the 40 are reachable in some meaningful way.

The timing varies too — some are 3-4 months out, some closer to 12. The older ones I'm less confident about being able to get real candor from.

**Assistant:**
Good — that's enough to scope this well. Let me get the documents current and then lay out the research program.The problem is well-defined. Here's the research program I'd scope for you — four workstreams running mostly in parallel:

---

**Workstream 1: Cohort & Usage Analysis** *(analytics partner lead, weeks 1–3)*
Pull usage data for all 40 churned accounts + a matched retained cohort. Test: did churned accounts have lower core feature adoption? Did accounts without dedicated implementation activate more slowly? Does churn concentrate in 50–200 employee or specific verticals? This directly tests the onboarding friction and value realization hypotheses with hard data.

**Workstream 2: CRM Note Tagging** *(CSMs lead, week 1)*
Have each CSM go through their churned accounts and tag notes against a structured schema: primary stated reason, competitive mention Y/N, onboarding issue Y/N, champion departure Y/N, value complaint Y/N. 40 accounts, shouldn't take more than an hour per CSM. This transforms inconsistent notes into a countable dataset and surfaces the competitive signal.

**Workstream 3: Exit Interviews** *(you, weeks 2–4)*
Target 10–12 accounts from your reachable 15–20, prioritizing the 3–6 month churns. 30-minute structured conversations — not a sales recovery call, explicitly framed as research. Probe directly on all three hypotheses. This is your highest-signal source and worth protecting your calendar for.

**Workstream 4: Exit Survey** *(light lift, weeks 2–3)*
For the accounts that won't do interviews — send a 6-question survey to the remaining reachable accounts. Quantitative but thin. Useful for validating interview themes, not for primary conclusions.

---

**The 6-week timeline shakes out roughly:**
- **Week 1**: Analytics partner starts data pull; CSMs do CRM tagging; you send interview outreach
- **Weeks 2–3**: Interviews begin; survey fielded; cohort analysis first pass
- **Week 4**: Interviews complete; support ticket sentiment analysis (your analytics partner can run this off ticket history)
- **Week 5**: Synthesis — do the data workstreams and interviews tell the same story? Where do they conflict?
- **Week 6**: Deck

---

Before I write this up formally — a few things worth flagging as genuine open questions:

- **Matched cohort**: Do you have enough retained accounts in the same size/vertical bands to build a meaningful comparison group for the usage analysis?
- **Interview access**: Have you stayed in contact with those 15–20 reachable accounts, or does outreach need to go through the CSMs who owned the relationship?

Are you happy with this overall shape, or does something feel off-sized?

## Turn 4

**User:**
This is close to what I had in my head, but cleaner. The workstream structure helps — I'd been thinking about it as one big sequential project rather than things that can run in parallel.

On your two open questions: the matched cohort is a fair flag. We have a few hundred active accounts so I think we can find matches, but it'll be cleaner in some segments than others. Worth a quick conversation with my analytics partner before she starts pulling data, just to confirm the comparison group is valid.

On interview access — it varies by CSM. Some of those relationships stayed warm, some I'd need to re-approach myself because the CSM relationship ended on the way out. I'll handle that coordination.

One thing I'm wondering about: the CRM tagging exercise in week 1. My CSMs are going to want to know what we're doing with those tags. If this surfaces that one CSM's book of business had significantly more onboarding issues flagged, that becomes a performance conversation I'm not sure I'm ready to have in the middle of a research sprint. Is that a risk I should just accept, or is there a way to structure it that doesn't put CSMs in a defensive posture?

Also — I notice you haven't asked what the research is actually supposed to *decide*. My COO will. I have a vague answer and I'm aware that's a gap.

**Assistant:**
Two really sharp observations — let me take them in order.

**On CRM tagging and CSM defensiveness:**

The cleanest solution is to not ask CSMs to tag their own accounts. The notes are already written — you or your analytics partner can do the tagging pass directly using a rubric you define. This completely removes the self-interest problem and has a side benefit: the tagging will be more consistent because one person is applying the schema, not four people with different interpretations of what "onboarding issue" means.

If you do want CSM involvement (because they have context the notes don't capture), consider cross-tagging: each CSM reviews accounts they *didn't* own. Still surfaces account-level patterns without the defensiveness dynamic.

Either way — communicate the purpose explicitly before anyone touches the data: *"We're diagnosing accounts, not evaluating CSMs. I'm not drawing performance conclusions from this exercise."* Say it once, clearly, and the anxiety largely disappears. The time to have a performance conversation about onboarding quality is after you have a full picture, not mid-sprint.

---

**On "what does this research decide" — you're right that it's a gap, and your COO will absolutely ask.**

Here's the honest frame: your research can surface *what* is causing churn, but the decisions it feeds are likely in a few buckets, and they're different enough that it's worth naming them now. At planning, the findings will be used to justify something — probably some combination of:

- **Headcount**: Add implementation specialists, or adjust CSM:account ratios for smaller accounts
- **Playbooks**: Redesign onboarding, add an early-value milestone, rebuild QBR cadence
- **ICP / segmentation**: Stop selling to segments that churn, or price/resource them differently
- **Product escalation**: Bring specific capability gaps to the product roadmap
- **Competitive response**: Pricing, packaging, or positioning changes (probably above your paygrade, but you'd be the one raising it)

The question is: which of these is *actually on the table* at your company's planning cycle? Because that should drive what your research needs to prove — not just directionally, but to what confidence level.

For example: if headcount investment is feasible and the hypothesis is onboarding friction, you need the data to show clearly that "no dedicated implementation" correlates with churn. If ICP tightening is politically viable, you need the segmentation to be airtight. If none of those decisions are actually in scope for your team, the bar is lower — you're raising a flag, not writing a prescription.

**So: what decisions are realistically yours or your COO's to make at planning?** That's what shapes how much rigor each piece needs.

## Turn 5

**User:**
That's the question I've been avoiding, honestly.

What's realistically mine: playbooks, CSM coverage models, how we resource onboarding. If the data says "accounts without a dedicated implementation resource churn at 2x the rate," I can build a case to the COO to either add an implementation specialist headcount or change which accounts get that resource. That's a conversation I could win if the data supports it.

ICP tightening is a joint call — I could raise it but sales and the CEO would have to own it. Same with product gaps — I can escalate with evidence but I don't run the roadmap.

So if I'm honest, the decisions that are actually mine to drive are probably: onboarding process changes, CSM playbook updates, and potentially a headcount ask for implementation support. The bigger structural stuff (stop selling to X segment, reprice for Y) — I can surface it, but I'm not the one deciding.

What that tells me, I think, is that the onboarding friction hypothesis is the one where I need the tightest data, because that's where I'm actually asking for something. The competitive pricing hypothesis is worth understanding but even if I confirm it, the response is above me.

Does that mean I should weight the research design toward the onboarding/value realization thread more heavily than I had been?

**Assistant:**
Yes — and the logic you just walked through is exactly right. Let me make it concrete.Yes — weight toward onboarding/value realization, but don't drop competitive entirely. Here's the precise reframe:

The research design stays the same structurally, but **the analytical depth per hypothesis changes**:

- **Onboarding friction** gets the most rigorous treatment: a proper cohort split (had implementation resource vs. didn't), churn rate differential with a real number, corroborated in interviews. This is the evidentiary core of your headcount ask. If the data says 2x churn rate, you can win that conversation. If it says 1.1x, you probably can't — and it's better to know that now than at the planning meeting.

- **Value realization gap** gets solid but not exhaustive treatment: which core workflow features did churned accounts *not* use, and when did adoption drop off? This feeds playbook changes and is politically uncontroversial — you don't need to fight for it, just demonstrate it.

- **Competitive pricing** gets a light pass: tag it in CRM notes and ask directly in interviews. "We see competitive mentions in X of our last 40 churns, here's what they said" is all you need to escalate credibly. The decision to respond isn't yours, so calibrate the evidence to the conversation you're actually having.

One thing worth flagging: onboarding friction and value realization might turn out to be the same causal chain. Accounts that got dropped into self-serve onboarding → didn't adopt core features → didn't get value → churned. If the data tells that story, your headcount ask gets stronger, not weaker — you're not just arguing "implementation resources reduce churn," you're arguing "implementation resources are the activation mechanism for feature adoption, which is the actual retention driver."

Two quick things to resolve before your analytics partner starts pulling data — both are just conversations, not research projects:
1. **Is the matched cohort valid?** Do you have enough retained accounts in the 50–200 employee bands to make the comparison meaningful?
2. **What's your COO's actual bar for a headcount ask?** Directional trend vs. statistically meaningful differential — you probably know from experience how she evaluates these.

Ready to move into designing the actual research program in detail — interview guide, survey structure, the cohort analysis spec? Or is there anything about the problem framing you want to push back on first?

## Turn 6

**User:**
The causal chain framing is useful — I hadn't explicitly connected those three things as a single mechanism, but that's probably what the data will show. And you're right that it strengthens the ask if it does.

On your two quick things: I'm fairly confident on the matched cohort. We have a couple hundred active accounts in that size band so finding a comparison group should be workable — I'll confirm with my analytics partner but I don't anticipate a problem. On the COO's bar — she's quantitative, she'll want a number not a trend line. "2x churn rate in accounts without implementation support" lands; "we think onboarding might be an issue" doesn't. So the cohort analysis needs to actually produce a rate differential, not just a correlation.

Let's move into the details. I want to get the interview guide right especially — I've done exit interviews before but I've never run a structured research program, and I'm worried about accidentally turning them into recovery calls or leading witnesses. What does a well-structured 30-minute exit interview look like for this specific set of hypotheses?

**Assistant:**
Good — let me write the interview guide. The two failure modes you named (recovery call, leading the witness) have specific causes, and both are preventable by design.

**What turns an exit interview into a recovery call:** You start with "we really value the relationship" and end with "is there anything we could do." The subject hears *sales call* and either gets defensive or performs politeness instead of honesty. Fix: open by explicitly ruling it out, and never close with an offer.

**What leads a witness:** Naming your hypotheses as questions. "Did you feel like onboarding was a problem?" gives them your answer to confirm. They'll confirm it even if it wasn't the main issue, because it's easier than contradicting you. Fix: ask for the story first, probe on specifics only after they've told you what mattered.

Here's the guide:

---

**Opening (2 min)**

*"Thanks for making time. I want to be upfront: this is a research call, not a sales call — I'm genuinely not trying to win you back. I'm trying to understand what happened so we can get better. The conversation stays with me. If it would be useful to you, I'm happy to share a summary of what I learn across all these conversations — sometimes that's valuable for people evaluating vendors. Any questions before we start?"*

Why this works: you've ruled out the sales dynamic, created a reciprocity incentive, and given them a reason to be honest.

---

**Context-setting (3 min)**

*"Before we get into the decision itself — can you remind me where things stood for your team when the renewal came up? What were you trying to accomplish with [product], and how was it going?"*

You want them grounded in the experience, not performing a post-hoc rationalization. Let them tell you the story from their frame.

---

**The decision (10 min)**

*"Walk me through how the renewal decision actually played out — who was involved, what were the main conversations?"*

Listen for: who drove it (champion? budget holder?), when it was effectively decided vs. when it was official, what alternatives they considered. Don't interrupt.

After they finish: *"What were the two or three factors that mattered most?"* 

Now probe on whatever they mentioned — not on your hypotheses yet. If they named price, ask about price. If they named feature gaps, ask about feature gaps. Follow their lead for 5 minutes.

---

**Experience probes (10 min)**

Only after they've told you what mattered unprompted, go back and fill in the gaps your hypotheses need. Use open questions, not leading ones:

- **Onboarding / value**: *"Take me back to the first 90 days — what did your team actually accomplish during that period?"* → If they mention friction, ask what specifically. If they don't mention onboarding at all, that's also data. Follow up: *"When did you feel like your team was getting real value from the product? Did that moment come?"*
- **Value realization**: *"Which parts of the product did your team use regularly? Were there things you bought expecting to use but didn't?"*
- **Competitive**: *"Did you end up going with an alternative, or did you just step away from this category?"* If they chose a competitor: *"What made that feel like the better fit?"* Don't ask about price directly — let them bring it up.

---

**The time machine question (3 min)**

*"If you could go back and change one thing about how we worked together — something on our side, not yours — what would it be?"*

This is your highest-signal question. It surfaces operational failures that people are too polite to volunteer. They've been giving you the diplomatic version for 25 minutes; this question often gets you the real one.

---

**Close (2 min)**

*"This has been genuinely useful. Is there anything you expected me to ask that I didn't?"*

Then thank them and stop. No offer, no pitch, no "we're working on exactly that."

---

**Your field notes (do this right after each call)**

Before you move on: write down the one or two things that felt like the real reason, separate from what they said explicitly. Then code against your three hypotheses: primary factor, secondary factor, not mentioned. This is how you turn 12 conversations into patterns rather than 12 separate stories.

---

The last thing: the framing email before the call matters almost as much as the call itself. Want me to draft that outreach too?

## Turn 7

**User:**
This is exactly what I needed. The time machine question especially — I can already think of two or three conversations where I would have stopped before getting there, and I'm pretty sure that's where the real answer lives.

One thing on the field notes: when you say "code against your three hypotheses," how do I make sure I'm doing that consistently across 12 conversations? I'm a little worried that after the first three calls I'll start hearing the story I expect and fitting things into it. Is there a lightweight way to keep myself calibrated — like reviewing the notes batch by batch with a second person, or some other check?

And yes, please draft the outreach email. That framing of "research, not recovery" is the right instinct but I tend to over-explain in writing, and I'm guessing the email should be pretty short.

**Assistant:**
**On coding consistently — the bias problem is real, and worth taking seriously.**

The root cause is that after a few calls you stop hearing what's said and start hearing whether it fits. Two lightweight fixes:

**Pre-commit to disconfirmation.** Before call 1, write down: *"What would I need to hear across these interviews to conclude each hypothesis is WRONG?"* Something like: *"Onboarding friction is NOT the driver if fewer than 3 of 12 people mention it unprompted, and the people who churned fastest had dedicated implementation."* Writing this down matters — if you can't describe what falsification looks like, you'll unconsciously find confirmation. Do this once, before you start.

**Simple coding sheet, filled out within an hour of each call.** Not a narrative — forced choices. Something like:

| | Primary factor | Secondary factor | Mentioned but minor | Not present |
|---|---|---|---|---|
| Pricing / competitive | | | | |
| Onboarding friction | | | | |
| Value realization | | | | |
| Champion departure | | | | |
| Budget / unrelated | | | | |

Plus: *"The real answer in one sentence"* and *"What surprised me."* The surprise field is especially useful — if you're never surprised, that's a sign you're pattern-matching to expectations.

**Mid-sprint blind check.** After interviews 5–6, share your notes (names removed) with one of your CSMs and ask them to fill out the same coding sheet independently. Where your codes diverge is exactly where your bias may be operating. This takes your CSM maybe 45 minutes total and gives you a calibration point before you've locked in a narrative. Pick someone who wasn't close to those accounts.

That's the whole system: pre-commitment, structured coding within an hour, one blind check at the halfway point. Nothing fancy.

---

**Outreach email:**

---

Subject: Quick ask — 20 minutes to share what you saw

Hi [Name],

I'm doing a structured research project on why some of our customers have decided not to renew, and I'd love 20 minutes of your honest perspective.

This isn't a sales conversation — I'm genuinely not trying to win you back. I'm trying to understand what we got wrong so we can fix it. Your name won't appear in anything I publish internally.

If you're open to it, I'm happy to share a summary of what I hear across these conversations when I'm done — sometimes that's useful context if you're evaluating vendors in this space.

Would you have 20 minutes in the next two weeks? [Calendly link]

Thanks either way —
[Name]

---

Short version of why this works: it's direct about the purpose in the first sentence, explicitly rules out the sales dynamic in the second, and the reciprocity offer (sharing findings) gives them a reason beyond politeness to say yes. The Calendly link reduces friction — if they're willing, make it easy.

One thing to adjust: if you have any warmth in the relationship, add one sentence at the top that's personal — *"I've been thinking about the conversations we had during your renewal"* or *"I remember you were using [specific feature] — I'd love to understand how that landed."* Generic research emails feel like surveys. A sentence of specific memory makes it feel like a conversation they're being invited into.

Ready to move into the cohort analysis spec for your analytics partner, or do you want to work through the synthesis framework first — how you'll turn the four workstreams into a coherent story for the deck?

## Turn 8

**User:**
The pre-commitment to falsification is the piece I would have skipped and regretted. I would have designed the research, run the interviews, and found what I was looking for. Writing down what "wrong" looks like before I start is going to feel uncomfortable, which probably means I need to do it.

The outreach email is right. Short, honest, no hedging. I'll add the personal line — for most of these accounts I can pull something specific from the CRM notes before I send.

On where to go next: I want the synthesis framework. The cohort analysis spec I can work through with my analytics partner directly — she'll push back and improve it on the technical side, and I'll share the hypotheses with her. But the synthesis piece — how I take four workstreams of messy data and turn them into a coherent narrative for a planning deck — that's where I'm most likely to lose the thread. I've seen a lot of "here's what we found" slide decks that just list findings and never actually make a case. I don't want to do that.

**Assistant:**
The difference between a deck that makes a case and one that lists findings is this: **a case has a spine — one sentence the whole thing is built around.** Findings decks have no spine; they have sections.

Your job in week 5 isn't analysis — analysis happens in weeks 1–4. Week 5 is about finding the sentence.

---

**Step 1: Build the evidence table first (days 1–2 of week 5)**

Don't touch the deck yet. For each hypothesis, fill out this table from your four workstreams:

| | Cohort data (WS1) | CRM tags (WS2) | Interview themes (WS3) | Survey (WS4) | Verdict | Confidence |
|---|---|---|---|---|---|---|
| Onboarding friction | | | | | confirmed / partial / disconfirmed | high / med / low |
| Value realization | | | | | | |
| Competitive pricing | | | | | | |

Confidence is **high** if two independent sources agree. **Medium** if one is clear and others are ambiguous. **Low** if sources conflict or data is thin. Be honest — low-confidence findings get a different treatment in the deck (flagged as "likely" or "warrants monitoring"), not the same treatment as high-confidence ones.

One important rule: **quantitative data outranks self-report when they conflict.** If interviews say "pricing" but cohort data shows churned accounts had feature adoption rates half of retained accounts, believe the data. There's a well-documented dynamic where "price" is the socially acceptable exit narrative — it's not embarrassing to say you found something cheaper. "We never figured out your product" is harder to admit. CRM usage data can't rationalize. People can.

---

**Step 2: Find the sentence (day 2–3)**

Look at your completed evidence table and ask: is there a story that connects the confirmed findings? Three possible structures, in order of how strong a case they make:

**Single mechanism** — all roads lead to one cause. *"Mid-market accounts without dedicated implementation never reach core feature adoption, don't perceive ROI at renewal, and churn at 2x the rate of accounts that got implementation support."* This is the best possible outcome — one sentence, two supporting numbers, clean ask. If your data tells this story, you've won.

**Segmented story** — different causes explain churn in different groups. *"For accounts under 100 employees, competitive displacement is the primary driver. For 100–200 employee accounts, it's the onboarding-to-value chain."* Still a strong case, just more complex. The plan has two tracks.

**Multiple independent causes** — genuinely distinct drivers with no connecting thread. This is the hardest to turn into a focused plan. If you're here, resist the temptation to present three equal findings — **force a hierarchy.** Which cause explains the most churn by volume? Lead with that.

---

**Step 3: Build the deck spine**

Once you have the sentence, the deck almost writes itself. It's a six-part argument:

1. **The situation** — Churn went from 7% to 11%. Here's what that means in ARR. We didn't have a rigorous explanation.
2. **The method** — We ran a 6-week research program: cohort analysis, exit interviews, CRM analysis, survey. Here's how we tested for noise.
3. **The finding** — [Your sentence.] Here's the number.
4. **The mechanism** — Here's *why* it happens. (The causal chain slide — this is often the most important one, and most decks skip it.) *"Accounts without dedicated implementation complete onboarding at 40% the rate of supported accounts, reach core feature activation 90 days later, and show half the engagement at the 6-month mark."*
5. **The plan** — Here's what we're changing. Here's what we're asking for. Each ask maps explicitly to a finding.
6. **What we don't know** — What we looked for and didn't find, or where confidence is medium rather than high. This slide makes everything else more credible. A COO who hasn't seen a "what we don't know" slide in a planning deck will notice it.

---

**Step 4: The "so what" discipline**

Every slide title should be a conclusion, not a description. 

- ❌ *"Interview Themes"*
- ✅ *"Churned accounts consistently describe an onboarding experience without a clear value moment"*

- ❌ *"Cohort Analysis Results"*  
- ✅ *"Accounts without dedicated implementation churn at 2.1x the rate of supported accounts"*

If you can't write a conclusion title for a slide, the slide isn't ready to be in the deck — either the finding isn't clear enough, or it doesn't belong.

---

**The scenario you want to avoid** is synthesizing too early, before you have the evidence table. The temptation is to start building the deck in week 4 when interviews are still running and data is still coming in. Don't. The deck should take 2–3 days, not 2 weeks. If it takes longer, you're still doing analysis in deck form, which is a sign the synthesis step got skipped.

---

I've been keeping the research program documented as we go. Want me to pull together a clean summary of the full program — workstreams, timeline, interview guide, synthesis framework — as a single artifact you could actually hand to your analytics partner and CSMs as a brief?

## Turn 9

**User:**
Yes, please do that. A clean brief I can hand to my analytics partner and use to kick off the conversation with my CSMs would save me significant time — right now it's all in my head and in this conversation.

Two things I want to make sure are in it: the falsification criteria (what each hypothesis looks like if it's wrong), because I know that's the piece I'll skip under time pressure, and the "what we don't know" slide in the deck structure. I would not have included that. The COO will trust the findings more if I'm explicit about the limits of the analysis — that's the kind of thing that makes or breaks credibility with her.

One honest reaction to the synthesis framework: I'm hoping the data tells the single-mechanism story, because that's the one I can actually act on with a focused ask. But I'm aware I might be hoping for it a little too hard. The pre-commitment to falsification is going to be important for keeping me honest about which story the data actually tells.

If you can pull together that summary artifact, I think I have what I need to actually run this program.

**Assistant:**
The brief is written. It's self-contained — someone picking it up without this conversation has everything they need to execute.

What's in it, in order:
- The three hypotheses with explicit falsification criteria for each
- WS1 spec (what to pull, what analysis to run, the scoping conversation first)
- WS2 tagging schema (ready to use, with the note about not self-tagging)
- WS3 full interview guide including the outreach email, the time machine question, the coding sheet, and the anti-bias protocol
- WS4 survey questions, ready to send
- The 6-week timeline
- The full synthesis framework: evidence table, the three story structures, the deck spine with the "what we don't know" slide, and the slide title discipline

The last section — "How to Use This Brief" — is addressed separately to your analytics partner, your CSMs, and you personally. The falsification note at the end is flagged explicitly as the piece most likely to get skipped.

One thing I added that you didn't ask for but will matter: the weighting rule for when sources conflict. If your interviews say "pricing" but your cohort data shows low feature adoption, the brief tells you to believe the data. That's the kind of judgment call that's hard to make in the moment without having written it down in advance.

You have a program. Good luck with it.
