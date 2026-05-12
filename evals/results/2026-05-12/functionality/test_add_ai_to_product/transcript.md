## Turn 1

**User:**
Hey — I need help thinking through an AI roadmap for our product. We sell expense management software to finance teams, mid-market companies. My CEO is pushing hard for an "AI story" ahead of our next board meeting, and a couple of our bigger customers have been asking about it directly in QBRs. I need to figure out what we actually build and be able to walk into a budget conversation with a concrete ask.

Can you help me work through this?

**Assistant:**
Absolutely — this is exactly the kind of decision worth thinking through carefully. There's a lot of "AI washing" happening right now, and finance teams are skeptical buyers. Getting this right matters.

Let me start capturing what you've told me while I ask a few more questions.Yes, let's dig in. A few things would really help me understand the shape of this:

**On the customer signal:** When customers ask about AI in QBRs, what are they actually asking for? Are they saying "your competitors have X and we need it," or "we have a specific pain point and wondering if AI could help," or mostly "we heard AI is a thing, what are you doing about it"?

**On your product today:** What does the expense workflow currently look like — where do finance teams spend the most time, and where do things go wrong? (Knowing the actual friction points helps figure out where AI can genuinely help vs. where it would be bolted on.)

**On the competitive landscape:** Are your direct competitors shipping AI features? If so, what are they claiming?

**On timeline and budget:** When's the board meeting, roughly? And do you have a sense of the budget range you're trying to justify — are we talking a small bet ($200-500K) or a major investment?

## Turn 2

**User:**
Good questions. Let me give you the specifics.

On customer signal — honestly, it's mostly the third thing. "We heard AI is a thing, what are you doing?" One customer mentioned something about their current tool doing "smart categorization" but they didn't have details. It wasn't a threat to leave over it, more like a check-in question.

On the product: the biggest friction is categorization. Receipts come in, our OCR pulls out the merchant and amount, and then users have to map it to a chart of accounts category. Our category suggestions are rules-based and they're wrong enough that most people just ignore them and pick from the dropdown manually. We're probably getting corrections on about 30% of OCR extractions too — wrong merchant name, mangled line items, that kind of thing.

On competition: one direct competitor announced an "AI assistant" three months ago. I've only seen the press release — something about "intelligent expense management." I haven't seen a demo. Honestly I don't know if they've shipped anything real.

On timeline: board meeting is in about 10 weeks. Budget conversation is sooner — probably 3 weeks.

**Assistant:**
This is really clarifying. A few things jump out:

The OCR quality and categorization problems are *real, measurable friction* — not manufactured AI opportunity. That's actually good news. It means there's a genuine product story here, not just marketing.

Let me capture this and ask the questions that would most change my recommendation.Three more questions — these would most change what I'd recommend:

**On data:** Do you have historical records of user corrections? Meaning: when someone overrides a category suggestion or fixes an OCR extraction, do you log what it was changed *from* and *to*? That data is the foundation of any ML-based improvement. If you have it, the categorization problem is much more tractable than if you're starting from scratch.

**On "shipped vs. vision":** For the board meeting — does your CEO want to walk in with something *already live* (even if small), or is a credible roadmap + early results enough? These lead to very different strategies: one is "ship a narrow improvement fast," the other is "design the right thing and show a plan."

**On engineering capacity:** Roughly how many engineers do you have, and do any of them have ML/AI experience? Or is this likely to require hiring or a vendor?

## Turn 3

**User:**
On data — yes, we log corrections. Every time a user overrides a category, we capture the before and after. We've got about 2 years of that across ~4,000 customers. We've honestly never done much with it beyond basic analytics dashboards, but it's there.

On shipped vs. vision — I think my CEO would prefer something live, but 10 weeks is tight. If I'm being realistic, a credible roadmap with something in beta or early access would probably land. He's not going to know the difference between "we shipped this" and "we have 50 customers piloting this" at a board meeting.

On engineering: 22 people total. Zero shipped ML features. I have one backend engineer who took a Coursera ML course and is interested, but that's it. So realistically, if we're building something custom, we're probably hiring or using a vendor — I haven't decided which yet, and that's partly what I need to figure out for the budget ask.

**Assistant:**
Okay — this is a really clear picture now, and it's actually a better situation than it might feel like. You have something most companies don't when they start talking about AI: *two years of labeled training data from 4,000 customers*. That's a genuine asset, not just a talking point.

Let me capture everything and then share what I think the real decision is.Here's what I'm seeing clearly now, and then one more question:

**The real opportunity isn't a chatbot.** The most defensible AI story you can tell — to the board *and* to customers — is: *"We took two years of correction data from 4,000 customers, and we used it to build a categorization engine that actually learns. Our suggestions go from being ignored to being right."* That's a measurable improvement, it solves a real pain, and your correction data is a moat that a competitor announcing an "AI assistant" in a press release doesn't have.

The "AI assistant" angle (chat interface for expense queries) is faster to build with vendor LLMs, but it's the kind of thing customers demo once and forget. Finance teams don't want to chat with their expense software — they want the tedious parts to disappear.

**The key open question before we go further:** Does your CEO already have a specific vision for what "AI" looks like in the product — like, does he use the word "chatbot" or "copilot" or "assistant"? Or has he left the definition to you? This matters because if he's already anchored on something specific, you may need to either align to it or actively reframe before the budget conversation.

Also — one more thing about the chart of accounts: is it standardized across your customers (e.g., everyone uses the same category taxonomy), or is it custom per company? Per-company learning is more powerful but requires a different architecture.

## Turn 4

**User:**
That framing actually resonates more than I expected. The "suggestions go from being ignored to being right" — that's something I could actually say to a customer without them rolling their eyes.

On my CEO: he hasn't been specific. He keeps saying "AI story" and "like what the competitors are doing" — but when I press him on what he actually saw, it's just the press release. He hasn't said chatbot explicitly. I think he'd be fine with whatever I bring him as long as it sounds credible and isn't vaporware. The framing you just gave me is something I could walk him through.

On the chart of accounts: it's custom per company. Every customer has their own taxonomy. Some are using standard accounting categories, some are pretty idiosyncratic. That's actually part of why our rules-based suggestions are bad — they're trying to be generic and failing.

And look, I want to make sure I understand what you're saying. You're telling me to skip the chatbot angle entirely and go all-in on better categorization? Because my instinct was to do both — something visible and flashy for the board narrative, and something more functional underneath. Is that wrong?

**Assistant:**
Not wrong — but the order matters, and so does what you mean by "both."

Here's the honest tradeoff:

**The case for "both":** A chatbot is fast to build with an LLM API — potentially 3-4 weeks with vendor tooling. It's demo-able. Boards like things they can see. And a natural language query interface ("show me all travel expenses over $500 this quarter") is genuinely useful for finance teams, not just a toy.

**The risk with "both":** If the chatbot becomes the thing you're demoing, it sets the expectation that's your AI story — and then the categorization work, which takes longer and requires more thought, becomes the "also we're doing this." The thing that's actually valuable ends up subordinated to the thing that looks impressive but that nobody asked for. That's how companies end up with an AI assistant that gets demoed once and never used.

**The smarter version of "both":** There's a coherent story where these aren't separate things. The same per-company learning model that fixes categorization *is* the intelligence layer — and a natural language interface is just a surface on top of it. You build the foundation first (categorization), then you can put the query interface on top. That way your demo at the board meeting shows both: "Here's accuracy before and after. And here's how a CFO can now ask questions about their data." The story is *one AI layer*, not two separate initiatives.

The question is really: what do you have capacity to actually ship in 10 weeks given your team? Because "both" with constrained resources often means neither is done well.

Two more things I want to nail down before we move into requirements and solution options:

**On success criteria:** After the board meeting, what does "this worked" look like for *you* specifically? Is it budget approved, a specific feature shipped, positive customer feedback, something else?

**On the per-company chart of accounts:** Do customers maintain their own category lists in your product, or are they bringing them from external accounting systems (QuickBooks, NetSuite, etc.)? This affects how you'd build per-company learning.

## Turn 5

**User:**
The "one AI layer" framing is useful — that's actually something I can sell internally. Rather than "we're building a chatbot AND improving categorization," it's "we're building a learning engine, and here's what it unlocks." That's a cleaner story.

On success criteria: honestly, the first milestone is budget approved in 3 weeks. After that, I want something in front of customers before the board meeting — even a beta. And longer term, I want to see categorization acceptance rate go up measurably. Right now users mostly ignore our suggestions. If we can get that to where people are accepting them more than half the time, that's a real metric I can track and report.

On the chart of accounts: it comes from NetSuite or QuickBooks. Customers sync it when they set up their integration. So we already have their category taxonomy in our system — it's not something they're manually maintaining inside our product.

One thing I keep coming back to: I still need a number for the budget meeting in 3 weeks. I don't need a full engineering plan but I need to walk in with a range and a rough breakdown. When do we get to that part?

**Assistant:**
We're closer than you might think — maybe two more pieces of information and then we can sketch the budget. Let me capture what you just told me first.Good — two more questions and then we can get into the budget math:

**Transaction volume:** Roughly how many expense receipts/transactions does your platform process per month, across all customers? Order of magnitude is fine — thousands, hundreds of thousands, millions? This is the biggest variable in what an LLM-based approach costs to run.

**Compliance constraints:** Do you have SOC 2 or similar certification? Any data residency requirements from customers? Some finance teams are sensitive about sending transaction data to third-party APIs — knowing whether that's a real constraint affects which vendors are available to you.

Once I have those, I can give you three budget options (conservative, mid-range, more ambitious) with rough breakdowns — enough to walk into the budget conversation with a range and a rationale.

## Turn 6

**User:**
Transaction volume: I'd estimate somewhere in the low hundreds of thousands per month. Our customers are 50-500 employee companies, so expense volume is real but not enterprise scale. If I had to guess — maybe 200,000-400,000 receipts a month across the full customer base.

On compliance: yes, we're SOC 2 Type II. Data residency hasn't come up often but we have a handful of customers in financial services who've asked about it. We've generally handled it on a case-by-case basis. It's not a universal constraint but it's not zero either.

I'll also flag — my engineering lead has mentioned before that we're cautious about sending raw customer financial data to third-party APIs. It's not a hard block but it's something we'd want to think through carefully. We'd probably need to at least anonymize or aggregate before sending anything out.

Okay, what are the three budget options?

**Assistant:**
Okay. Here are three real options. I've done the math on API costs at your volume — some of the numbers will surprise you.

---

**Option A: API-first, ~$220–350K year one**

Use an LLM API (GPT-4o-mini or similar) to power categorization. For each receipt, you send the merchant name plus the company's chart of accounts plus a handful of similar historical corrections from that company's own data — that's the "learning" part. Before anything leaves your system, you run it through a privacy layer that tokenizes merchant names and strips amounts and user info. What the API sees is essentially a pattern-matching problem, not financial data.

The numbers: at 300K receipts/month, this costs roughly $500–800/month in API fees. Not a budget line item — a rounding error. The real cost is engineering: two dedicated engineers for about 12 weeks to build the categorization service plus the privacy/anonymization layer. Call it $150–200K in engineering time. Add $50K for an outside ML contractor to design the approach and review the model, and you're at $200–250K in year one. Ongoing cost after that is minimal.

Timeline: beta with real customers in 8–10 weeks is realistic with this approach. It fits your board meeting.

Risk: you're dependent on a vendor API long-term, and if they raise prices or you outgrow the approach, migration is work. Also, the privacy layer needs real design — your engineering lead is right to flag it.

---

**Option B: Build to own, ~$550–750K year one**

Hire one or two ML engineers, train a categorization model on your correction history, and run it entirely on your infrastructure. Nothing leaves your system. The model can learn per-company patterns with no API dependency. This is the moat version — your 2 years of correction data becomes a proprietary asset that a competitor with a press release can't replicate.

The numbers: one ML engineer fully loaded is $200–280K/year. Two dedicated existing engineers for 6–9 months. Infrastructure for model training and serving runs $60–90K/year. Total year one: $500–700K.

Timeline problem: hiring takes time you don't have. An ML engineer search typically runs 8–12 weeks. Even if you start today, you're not in front of a board with a beta on this path. This is a year-two story unless you contract rather than hire.

Risk: high upfront commitment before you know if the approach works. Hiring an ML engineer for a problem you haven't validated yet is expensive if the direction changes.

---

**Option C: Staged — $300–450K year one, recommended**

Phase one (now through board meeting, 10 weeks): build the beta using the API-first approach. Two engineers, API with privacy layer, target 20–40 customers in early access. Spend roughly $80–100K to get there. This gives you real pilots, real data on acceptance rate improvement, and a concrete story for the board.

Phase two (post-board, Q1/Q2 next year): use the beta results to justify a bigger investment. Hire one ML engineer, build the proprietary model, migrate off the API. Spend $250–350K on the build-out.

Total year one across both phases: $330–450K. But critically — you're asking for phase one now ($100K, low risk) and making the bigger ask after you have evidence. That's a much easier conversation with both your CEO and your board than walking in asking for $600K on a hypothesis.

---

**What I'd actually put in the budget ask:**

Ask for $120–150K to cover phase one: two engineers for three months plus an ML contractor for design plus API costs and privacy/security review. Frame it as: "We're committing to a beta with measurable results by the board meeting. The follow-on investment depends on what the beta shows." This is defensible, low-risk, and lets the results do the selling for the larger spend.

The one thing that would change this: if your data residency/financial services customers would object even to anonymized data leaving the system, Option A becomes more complicated and Option B becomes necessary sooner. Worth a quick check with your two or three most compliance-sensitive customers before the budget meeting.

Does this give you enough to build the ask? And do you want to now think through the actual product requirements and what "the learning engine" needs to do — so you have something concrete to show the engineers when you come out of the budget meeting?

## Turn 7

**User:**
This is exactly what I needed. Option C is clearly right — I'm not going to walk into a budget meeting asking for $600K on a hypothesis when I can make a $120K ask and let the results justify the rest. That's a much easier sell to my CEO.

The privacy layer point is worth flagging to my engineering lead before I finalize anything. I want to make sure we're aligned on what "anonymized" means in practice before I promise that approach to compliance-sensitive customers.

On the follow-on question — yes, I do want to think through the product requirements. Partly because I need to know what I'm actually asking the engineers to build, and partly because when the board asks "so what does this do exactly," I need an answer that's more specific than "AI categorization."

What does the learning engine actually need to do, and what does it look like to a user? That's where I get fuzzy. Like, does the user see anything different, or does it just quietly get better in the background?

**Assistant:**
Good question — and the answer matters a lot, because "quietly gets better" is a terrible board story even if it's technically accurate. Let me think through both the user experience and the requirements at the same time.

**What the user sees today vs. what they'd see:**

Right now the flow is: receipt comes in, system shows a category suggestion that's wrong often enough that everyone ignores it, user scrolls the dropdown, picks manually. The AI version of this isn't a new screen or a chatbot — it's the same screen where the suggestion is now *right most of the time*, displayed prominently enough that accepting it is the path of least resistance.

Concretely: instead of a dropdown with a wrong answer pre-selected, the user sees something like: *"Client Entertainment — based on your company's history with similar expenses. Accept / Change."* One tap. Done. When they do override, that's a training signal. The model gets better per-company, permanently.

The finance manager experience is where it gets more compelling for the board story: instead of reviewing expenses one by one, they see a batch view — "62 of 74 expenses have confident category suggestions ready for your review." They can bulk-accept, spot-check, or step through the uncertain ones. That's a workflow change, not just a quality improvement.

**What the board answer is:**

*"When an employee submits a receipt, we now suggest the right category based on how that specific company has handled similar expenses before. For companies that've been using us a year or more, we're right more than half the time. Finance managers can review and approve in bulk. The more they use it, the better it gets."*

That's concrete, non-vague, and doesn't require the word "AI" to land.

---

Now let me capture the actual requirements so you have something to hand to engineering.I've written up the full requirements — here's the shape of it:

**6 must-haves for beta** (the 10-week sprint):
1. Per-company model using correction history
2. Confidence scoring (high confidence → single prominent suggestion, low → show top 3)
3. One-click accept in the submission flow
4. Correction loop that feeds overrides back in real-time
5. Privacy/anonymization layer before any API calls
6. Acceptance rate tracking per company (this is how you prove it worked)

**2 more for GA** (beta → launch): bulk manager review UI and explanation text ("Based on 23 similar expenses in your company").

**Phase 2**: natural language queries and OCR improvement — explicitly framed as follow-on, not promises.

I also called out what's explicitly *not* in scope — automated approval, cross-company training, generative AI for policy writing. That's as important as the requirements list; it prevents scope creep during the build and manages board expectations.

One thing worth checking with your engineering lead before the budget meeting: requirement #4, the correction loop. The question is whether "update before their next submission" means updating in real-time (within the same session) or nightly batch. Real-time is a much more complex system; nightly batch is almost as good in practice. Worth having that conversation early.

Do you want to also work through the stakeholder picture and any open questions before we move on — or do you feel like you have enough to go into the budget conversation and come back to work through the solution design more deeply?

## Turn 8

**User:**
I think I have enough to go into the budget conversation — honestly this is more clarity than I expected to have going in. The staged ask makes sense, the requirements feel right, and the board narrative is something I can actually say out loud.

One thing I'm realizing: I have all of this in a chat window. What I actually need to bring to the budget meeting is something I can put in front of my CEO and CFO. Is there a summary or brief you can pull together — the problem we're solving, the approach, the three options with the recommendation, the phase one ask — something I could hand to someone who wasn't in this conversation?

**Assistant:**
The brief is written. It's at `/Users/yzunger/.copilot/session-state/51945009-4e4f-4824-ac83-bf23d94a29e8/files/ai-roadmap-brief.md` — you can open, copy, or export it from there.

It covers: the situation, the real opportunity (correction data + categorization friction), the approach ("one AI layer"), all three options with the recommendation, the Phase 1 ask broken down by spend, and the three open items to resolve before finalizing.

The "Open Items" section at the end is intentional — walking into a meeting with unresolved questions flagged explicitly reads as rigorous, not unfinished. It also gives you something to say when the CFO asks "what are the risks."

A few things to do before the meeting:
- **Get a demo of the competitor's product** if you can. The brief notes this; if they've shipped something real, your framing might need to sharpen.
- **Align with your engineering lead on the privacy layer** before you commit anything in writing. That conversation should happen before, not after, you present this.
- **Fill in your actual cost of engineer-time** — I used estimates, but you know what two engineers for three months actually costs at your company.

Do you want to keep going and work through the stakeholder map and failure modes before the board meeting — or is this a good stopping point for now?

## Turn 9

**User:**
This is genuinely useful, thank you. The open items framing is right — I'd rather walk in with flagged unknowns than get blindsided by a question I didn't think of.

On failure modes: I'm tempted to say yes, partly because my CFO is going to ask about risks and I want a real answer. But I also don't want to over-engineer this before the budget meeting. Is that something we could do quickly — like, what are the two or three failure modes that actually matter for a phase one bet like this? Or is it more of a deep dive that I should save for after I have budget approved?

**Assistant:**
You don't need the full process for the budget meeting. You need three honest answers to CFO questions. Here they are:

**Risk 1: The model isn't actually better than the rules.** Your correction data might be noisier than it looks. If different employees at the same company categorize "Starbucks" six different ways, the model learns confusion, not patterns. *Mitigation:* Before building any UI, run an offline test — take the last six months of correction data and see if you can predict the most recent corrections from the earlier ones. If the backtest doesn't beat your current rules, stop before spending the engineering time. This should be week one work, not a post-launch discovery.

**Risk 2: The privacy layer is harder than expected.** "Anonymize before sending" sounds simple until legal and engineering sit down together and disagree about what "anonymized" means, or a compliance-sensitive customer says even tokenized merchant data is off-limits. *Mitigation:* Legal and engineering review in the first two weeks, before writing a line of product code. If this blocks the API approach entirely, the fallback is running a smaller model on your own infrastructure — achievable but adds 4-6 weeks to the timeline.

**Risk 3: The beta is a ghost town.** If you recruit 30 beta customers by who's most enthusiastic about AI, you might get companies that don't submit many expenses. No expenses, no data, no story at the board meeting. *Mitigation:* Recruit beta participants by expense volume, not enthusiasm. You want the customers who submit 500+ receipts a month, regardless of whether they asked for this feature.

---

Those are the three a CFO will actually probe. The honest version for the room: *"We've identified the three ways this phase one bet could fail and we have a mitigation for each before we spend significant money."* That's a strong answer.

The deeper failure analysis — failure modes around the full product, the learning engine at scale, competitive responses — is worth doing after budget approval when you're designing the actual system. Save that for then.

Want me to add these three risks to the brief before you finalize it?

## Turn 10

**User:**
Yes — add them to the brief. That section on risks is probably the most important thing I can walk in with.

This has been more useful than I expected. I came in thinking I needed an "AI strategy" and I'm leaving with a specific bet, a budget ask, a backtest to run in week one, and a brief I can actually hand to someone. That's a better outcome than I had this morning.

I'll take it from here — align with engineering lead, run the backtest framing by them, and set up the budget conversation. If the phase one results are interesting I'll want to come back and work through the full solution design before the board meeting.

Thanks.

**Assistant:**
Done — risks section is in the brief.

Good luck with the budget meeting. The sequence you're walking in with is solid: backtest in week one to validate the data, privacy review in week two, then build. If either of those surfaces a problem, you learn it cheap. If they don't, you build with confidence.

When you come back after phase one — bring the acceptance rate data. That number will do most of the work for the follow-on ask.
