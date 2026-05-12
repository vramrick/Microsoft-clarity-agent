## Turn 1

**User:**
Hi — I'm hoping you can help me think through a research project. I'm Head of Customer Success at a B2B SaaS company and our logo churn has been creeping up — from around 7% to 11% annually over the last three quarters. My COO has asked me to come in with a "churn plan" for annual planning, which starts in about six weeks.

I want to do this rigorously. My instinct is that we need a proper research program — churned customer interviews, cohort analysis of usage patterns pre-churn, maybe a survey — so we can actually understand *why* we're losing accounts rather than guessing. I'm looking for help scoping that out: what methods to use, how to structure the analysis, what questions to ask, and how to present findings to the COO.

Can you help me think through that?

**Assistant:**
Good context — let me save what you've described and ask a few questions to sharpen the scope.Good start. A few questions that would shape the research design significantly:

**1. Do you have any working hypotheses already?** Has anything shown up in exit interviews, renewal conversations, or support tickets that might point to a cause — product gaps, a competitor, onboarding issues, pricing? Or is it genuinely opaque right now?

**2. What does your churned customer pool look like?** Roughly how many accounts have churned in the last 3 quarters, and are they concentrated in any particular segment (company size, industry, product line, time-to-churn)? This affects whether interviews are feasible and what cohort cuts make sense.

**3. What data infrastructure do you have access to?** E.g., product usage analytics (Mixpanel, Amplitude, etc.), CRM data, health scores — or is usage data sparse? This determines how much of the diagnosis can come from quantitative analysis vs. needing to be primary research.

## Turn 2

**User:**
Good questions. Let me take them in order.

On hypotheses: we have hunches but no rigorous evidence. The CSMs mention pricing competitiveness and a specific competitor (there's one that's been aggressive in our mid-market space) pretty often. Onboarding struggles come up too — we've had a few accounts that never really got traction after implementation. But honestly, these are vibes from QBR notes, not data. My COO asked me last week if I actually *know* why we're churning and I had to admit I didn't.

On the churned pool: roughly 40 accounts over the last two quarters. I don't have a clean segmentation in front of me but off the top of my head it's not obviously concentrated — mix of sizes and verticals. That said, I haven't done a structured look at it, which is part of the problem.

On data: we have a decent amount, actually. Product usage — feature adoption, DAU, session depth. Support ticket history with sentiment tags. Quarterly NPS (though response rate is low, around 15%). And CRM notes from the renewal and cancellation conversations, though those are inconsistent — some CSMs are thorough, some leave one-liners. Nobody has done a structured analysis of the churned accounts in the last 18 months.

**Assistant:**
This is a strong foundation. You have the three elements that make rigorous research possible: a defined population (40 accounts), quantitative behavioral data, and qualitative signal to build hypotheses from. Two more questions before I help you design the program:

**1. What does the COO actually want out of "churn plan"?** Is she expecting (a) a diagnosis with root causes, (b) a set of proposed interventions and what they'd cost/require, or (c) a full plan-on-a-page with projected impact on next year's churn rate? The ambition level of the output shapes how much time you can spend on research vs. synthesis vs. planning.

**2. Who's doing this work?** Is this largely you, or do you have CSM analysts, a data analyst, or RevOps support who can pull and model the quantitative data while you design and run interviews?

## Turn 3

**User:**
On the COO's expectations — honestly, I think she wants (b), interventions with some sense of what they'd take. She's pragmatic. She's not going to sit still for a 20-page research report; she wants to know where to put resources. But I don't think she'd accept interventions that aren't grounded in actual diagnosis — she pushed back on me last year when I proposed a new onboarding program without a clear problem statement. So I need the diagnosis, I just can't stop there.

On resourcing: it's mostly me, with some help from our analytics partner — one person, shared with the broader ops team, so maybe 20-30% of their time if I prioritize it. My four CSMs can contribute to things like interview outreach and synthesizing their own accounts' notes, but I can't put them on research full time. They have books to manage.

**Assistant:**
Good. Now I have enough to design this. Let me update what we have and then lay out a concrete research program.Here's how I'd structure the research program:

---

## Proposed Research Design: 6-Week Churn Diagnosis

### The core structure: quantitative first, qualitative second, synthesis third

With 6 weeks, limited bandwidth, and good existing data, the right approach is to front-load the quantitative analysis so your interviews are *informed*, not exploratory. That way you walk into conversations knowing which accounts behaved unusually and what to probe on.

---

### Phase 1 — Cohort Analysis (Weeks 1–2, analytics-led)

This is where your analytics partner earns their 20-30%. The work:

**Segment the 40 churned accounts** along 3-4 dimensions: ARR tier, company size, time-to-churn (fast vs. slow), industry vertical. You're looking for concentration — is the increase driven by a specific segment, or is it broad?

**Build behavioral signatures** by comparing churned accounts to a matched retained cohort. Look at:
- Feature adoption in first 90 days (early indicator of onboarding success)
- DAU/seat utilization trend in the 90 days *before* churn notice
- Support ticket volume and sentiment in the 60 days pre-churn
- NPS score trajectory where available

**Mine CRM cancellation notes.** Even inconsistent notes yield signal when you code them structurally. Have each CSM do a 60-minute pass on their churned accounts: tag by stated reason (price, competitor, product gap, no ROI, org change), and flag whether there were warning signs in QBR notes.

**Output:** A segmentation of churned accounts, a behavioral "fingerprint" of pre-churn patterns, and a preliminary ranking of stated reasons.

---

### Phase 2 — Churned Customer Interviews (Weeks 2–4, overlapping)

With 40 accounts, you can realistically complete 10–12 interviews if you start outreach in Week 1. That's a meaningful qualitative sample for B2B.

**Who to interview:** Purposive sample — not random. Target:
- 3–4 accounts that match the competitor hypothesis (mid-market, similar deal size)
- 3–4 accounts with onboarding/adoption signals from Phase 1
- 2–3 accounts that *don't* fit either pattern (they'll surprise you)
- Weight toward accounts with higher ARR — their story matters more to the plan

**Outreach:** CSMs do warm intros ("I'd love to understand your experience and hear your feedback") — dramatically higher response rate than cold CS outreach. Frame it as a listening session, not a post-mortem.

**Interview structure (30–45 min):**
1. Walk me through the timeline of the decision — when did it start feeling uncertain?
2. What alternatives did you consider or move to?
3. What was the moment it tipped for you?
4. What would have had to be true for you to stay?
5. Is there anything we could have done differently?

Don't lead with your hypotheses. Let their narrative surface the causes.

**Output:** Tagged themes, direct quotes for the COO deck, patterns across interviews.

---

### Phase 3 — Synthesis (Week 4–5)

Cross-reference what the data says with what customers said. You're looking for:
- **Confirmed hypotheses** — competitor threat shows up in both segment analysis *and* interviews
- **Surprises** — something the quant data flags that customers confirm (e.g., low feature adoption = no perceived ROI)
- **Contradictions** — stated reason is price, but usage was already near-zero before the renewal conversation (price was the excuse, not the cause)

Prioritize root causes by two dimensions: **frequency** (how many accounts does this explain?) and **ARR impact** (what portion of churned revenue does this represent?).

---

### Phase 4 — Interventions + COO Narrative (Week 5–6)

For each confirmed root cause, map a specific intervention:

| Root cause | Intervention | Who owns it | Rough lift |
|---|---|---|---|
| Competitive pricing in mid-market | Pricing strategy review / targeted discounting | CS + Finance | Medium |
| Onboarding failure → no ROI | Onboarding redesign + success milestones | CS + Product | High |
| Low feature adoption → perceived low value | Adoption playbook, executive check-ins | CS | Low-medium |

The COO presentation story: **"Here's what we found, here's the 2–3 things driving it, here's what we're asking for to fix it."**

---

### What I'd drop: the survey

You mentioned a survey as a possibility. I'd skip it given your constraints. A survey of at-risk accounts takes 2–3 weeks to design, deploy, and analyze, and self-report churn risk data is notoriously noisy. Your existing product data is more reliable than survey responses, and your interviews will give you the depth you need for the COO story. If this becomes a recurring program, a quarterly relationship survey makes sense — but not for this cycle.

---

Does this structure feel right? The two biggest questions before we go further: (1) do you have the analytics relationship to get the Phase 1 work done in 2 weeks, and (2) are there any churned accounts that are politically off-limits to reach out to?

## Turn 4

**User:**
This is really well-structured. Honestly, I came in thinking this was a 2–3 month program and you've mapped it to 6 weeks without obviously cutting corners — I want to sit with that a bit but my first reaction is that it's right-sized for what the COO actually needs.

The "quant first so interviews are informed" logic is compelling. I've done it the other way — jumped straight to interviews with no data context — and you end up in conversations where you're hearing surface-level post-rationalization rather than the real story. The behavioral fingerprint idea is particularly useful.

On your two questions: yes, I think I can get the analytics relationship scoped for a 2-week sprint if I frame it clearly and get the request in this week. That's on me to move on.

On politically sensitive accounts — there are probably 2–3 where the relationship ended badly. One in particular where there was a service failure and the account was actively hostile by the end. I'd want to tread carefully there, but I don't think they're off-limits, just need to be handled thoughtfully — maybe I do that outreach myself rather than through the CSM.

One thing I want to push on: you dropped the survey pretty quickly. I take your point about the design-deploy-analyze timeline, but I was also thinking of it as a way to reach the accounts we *can't* get to in interviews. Are there no circumstances where a lightweight survey of the full 40 would be worth it?

**Assistant:**
You're right to push back — I dismissed it too cleanly. Let me revise.

The version I was imagining was a designed-from-scratch survey deployed mid-program, which eats 2-3 weeks. That's not worth it. But the version you're describing — a lightweight coverage mechanism for the accounts you can't interview — is a different instrument. Here's when it's worth doing:

**The case for a short-form survey of all 40:**

You'll realistically interview 10–12 accounts. That leaves 28–30 whose signal you'd otherwise lose entirely. Even a 20% response rate on the remaining pool gives you 5–6 additional data points on a population of 40 — that's meaningful at this scale.

The key is keeping it honest about what a survey *can* do. It can't give you depth or uncover surprises — people post-rationalize churn reasons and check the first plausible box. But it can give you frequency data to test whether interview patterns generalize.

**How I'd use it:**

Deploy it in Week 1 as part of the same outreach wave as interview invitations. Frame it as "if you can't do a call, 3 minutes here would help us." Five questions max:

1. Primary reason for not renewing (multiple choice: pricing, product gaps, competitor, no ROI, org change, other)
2. Did you move to another solution — and if so, which one?
3. How far in advance had you made this decision? (within 30 days / 1–3 months / 6+ months)
4. What, if anything, could we have done differently? (open text)
5. Would you be open to a brief call? (routes to interview scheduling)

Question 5 does double duty — it's a survey *and* your interview recruitment tool. You'll get some yeses from people who wouldn't have responded to a cold call request.

**The caveat:** Don't let the survey crowd out the interviews. The qualitative depth is where your COO narrative comes from — a survey gives you percentages, not stories. If resources get tight, protect the interviews.

So: yes, add a lightweight survey — but as a parallel channel, not a replacement layer. Does that feel right?

Also — one thing I want to capture before we move to structuring the full plan: the politically sensitive accounts. You mentioned doing that outreach yourself. I'd actually suggest a different framing than the standard listening-session script for those. Do you want to think through how to approach the service-failure account specifically, or is that something you'd rather handle instinctively?

## Turn 5

**User:**
Yes, that framing works for me. Survey as a parallel channel with a clear ceiling on what it can tell us — I can get behind that. And the double-duty Q5 is smart, I wouldn't have thought to combine recruitment into the survey.

On the service-failure account — I think I'd rather think it through than wing it. The short version: there was a significant outage that affected this customer during a critical period for their business. It dragged on longer than it should have, we were slow to communicate, and by the time it was resolved they'd already made the call internally to leave. The CSM relationship was damaged. The customer was pretty vocal about it in their final calls.

I don't want to re-litigate the incident or make them feel like we're coming back for data extraction. But I also think there might be real signal there — was this genuinely the tipping point or were there cracks before the outage? That's actually a useful thing to understand. If it was a one-time operational failure that accelerated an otherwise-stable relationship, that's a different intervention than if they were already disengaged.

How would you approach that?

**Assistant:**
The research question you've identified is exactly the right one: *was the outage the cause, or an accelerant?* Those have completely different implications. Cause → fix your incident response and communication. Accelerant → the reliability failure was the final straw on a relationship that was already fragile, which means the real intervention is earlier.

Here's how I'd approach it:

**The outreach**

Do this yourself, not through the CSM. Short, direct email:

> "I've been doing a personal review of accounts we lost this past year, including yours. I wanted to reach out directly — not to revisit what happened or ask you to relitigate it, but because I think I can learn something from your experience that would make us better. I understand completely if you'd rather not, and there's no pressure. But if you'd be willing to give me 20 minutes, I'd be grateful."

Three things that email does: it signals this is coming from the top (not delegated), it explicitly names and neutralizes their biggest fear (being asked to relitigate), and it's a shorter ask than your standard interview. Give them a real opt-out.

**The conversation**

Don't open with the outage. Open with the arc:

> "Can you walk me through when your relationship with us first started to feel uncertain?"

Let *them* locate the tipping point. If they immediately go to the outage, that's your answer. If they start six months earlier — a QBR where something didn't land, a product gap that kept coming up, a budget conversation — that's also your answer. You learn more from where they start than from anything you ask directly.

When the outage comes up (and it will), don't explain or defend. Just: *"Tell me more about what that period was like for your team."* You want to understand the experience from their side, not correct the record.

Then, to test the accelerant hypothesis directly:

> "Before that happened, how would you have described your team's relationship with the product?"

> "Had there been any internal conversations about the renewal before the incident?"

Those two questions will tell you whether the departure was manufactured by the outage or merely confirmed by it.

**What you're listening for**

If they say things like *"we were happy before that happened"* or *"we would have renewed otherwise"* — and especially if your Phase 1 data shows strong usage up until that point — that's operational failure as cause. The intervention is reliability and incident communication.

If they say things like *"honestly, it had been a question for a while"* or *"the outage just made the decision easier"* — and your usage data shows a declining pattern before the incident — that's accelerant. The intervention is earlier relationship management and health monitoring.

Either answer is useful. The fact that this customer was vocal means they actually have opinions worth hearing. Vocal churned customers are often more informative than the polite ones who quietly leave.

**One thing not to do:** don't bring structured questions or a survey to this one. It needs to be a conversation. The moment they feel like they're filling out a form, you've lost the signal.

---

I think we now have enough to write out the full research plan and stakeholder picture. Want me to do that — capture everything we've discussed into a properly structured plan you could actually hand to your analytics partner and CSMs to kick off?

## Turn 6

**User:**
That's genuinely useful. The "where do they start" framing is something I wouldn't have thought to be deliberate about — I would have jumped straight to the outage because that's the obvious story. And the two probe questions to test accelerant vs. cause are exactly what I needed. I'll use those.

Yes — please write out the full plan. I need something I can actually share with my analytics partner this week to scope the Phase 1 work, and something I can use to brief my CSMs on what I'm asking them to do. If it's structured enough that I can pull the relevant sections for each audience, that would be ideal.

And if there's a way to capture the COO narrative arc in there too — even in skeleton form — that would help me. She's going to want to see this is heading somewhere actionable, not just a research exercise.

**Assistant:**
Now let me write the full plan document:The full plan is written. Here's what exists and who gets what:

**For your analytics partner this week** → Section 1: three scoped deliverables (segmentation, behavioral fingerprint, CRM note coding), with explicit instruction to surface contradictions rather than resolve them. Should take 15 minutes to read and scope.

**For your CSMs** → Section 2: two specific asks with time estimates (60–90 min for note review, warm outreach in Week 1), a clear framing for what to say and not say, and explicit notes that you're handling sensitive accounts yourself.

**Interview + survey materials** → Sections 3 and 4: outreach templates for three scenarios (standard, service-failure account, survey), the full interview guide with questions in order, and the post-call writeup format.

**Synthesis framework** → Section 5: the cross-validation matrix and cause/accelerant distinction you'll use in Week 4.

**COO narrative** → Section 6: a 7-slide skeleton you can fill in once findings are in hand. The structure is already argument-shaped — situation, method, findings, surprise, recommendations, ask — so you're not building the story from scratch in Week 5.

One thing to flag for that last slide: you'll want to loop in Finance or RevOps before the presentation to get the ARR impact numbers. The "what we're asking for / what it's worth" framing is much stronger when you can put a dollar figure on the retained ARR.

Is there anything you want to adjust in the plan before you start moving on it?

## Turn 7

**User:**
This is exactly what I needed. The structure maps to how I actually work — I can pull the analytics partner brief, hand it off this week, and come back to the interview materials when Phase 1 is wrapping up.

The Finance/RevOps note is a good catch. I tend to get deep in the CS story and forget I need the dollar framing to land with the COO. I'll make a note to loop them in around Week 4 before the synthesis is done.

One question: can I actually access the full document somewhere, or is this a summary of what you'd recommend the sections contain? I want to make sure I have the actual interview questions, outreach templates, and the slide skeleton written out — not just the structure — before I start.

**Assistant:**
It's all written out in full — every template, every question, the slide skeleton. The file is at:

```
.clarity-protocol/solution/solution.md
```

Let me show you the document so you can confirm everything is there:It's all there — every template, every question, the full slide skeleton. 258 lines of usable content.

If you want to copy sections out to share with specific people, the cleanest path is to open the file directly at `.clarity-protocol/solution/solution.md` in whatever editor you use. Each section is clearly labeled and self-contained, so you can copy Section 1 for your analytics partner and Section 2 for your CSMs without needing to edit anything first.

The one thing to add before Week 5: once your synthesis is done, you'll want to come back and fill in the actual findings in Section 6. That's when this becomes the real deck rather than the skeleton.

Good luck with the kick-off this week — the analytics scoping is the critical path item. Get that in motion and the rest will follow.

## Turn 8

**User:**
Good. I'll pull that file up and review it in full before I send anything out. Knowing it's structured in self-contained sections I can share selectively is exactly what I needed.

Analytics partner brief goes out today. Thank you — this was more useful than I expected. I came in thinking I needed 2-3 months to do this right; I'm leaving with a 6-week plan I can actually defend to my COO. That's a better outcome.

**Assistant:**
Good luck. The hardest part was actually what happened in this conversation — being willing to run a rigorous process instead of going straight to solutions. The COO will see that discipline in the presentation.

If you come back after the analytics sprint delivers, or once interviews are underway and patterns are emerging, this is a good place to work through the synthesis. Sometimes what you find doesn't fit the framework you built going in — that's worth thinking through before you stand in front of your COO.
