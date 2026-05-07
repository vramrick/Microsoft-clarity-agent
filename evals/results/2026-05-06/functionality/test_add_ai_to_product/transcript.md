## Turn 1

**User:**
Hey — I need help thinking through an AI roadmap for our product. We sell expense management software to finance teams, mid-market companies. The CEO wants an "AI story" for the board meeting next quarter, a couple of our bigger customers have asked about it in QBRs, and our main competitor just announced something. I need to figure out what we actually build, how to scope it, and how to talk about it internally to get budget approved.

Can you help me work through this?

**Assistant:**
Absolutely — this is exactly the kind of thing Clarity is built for. Multiple pressures converging (board narrative, customer asks, competitive move) often produce rushed decisions, and it's worth being deliberate.

Before I start taking notes, a few questions to make sure I understand the situation:

1. **The competitor announcement** — do you know what they actually shipped, or is it mostly marketing? And are they your closest competitor, or one of several?

2. **The customer asks** — were they asking for something specific ("can you auto-categorize receipts?") or more general ("what's your AI plan?")?

3. **Internally** — who else is in the room on this? Is it just you driving it, or do you have product, engineering, and sales all needing to align?

The reason I'm asking: "AI story for the board" and "what we actually build" can pull in very different directions, and understanding which pressures are real vs. perception will shape how we think about this.

## Turn 2

**User:**
Good questions. On the competitor — honestly, it's mostly marketing as far as I can tell. I saw their press release and a LinkedIn post from their CMO. Nobody on my team has actually seen a demo. They're our closest competitor though, so I can't just ignore it.

The customer asks were pretty generic — "what's your AI roadmap?" type stuff. Not "can you do X specifically." Which is part of why I'm here — I don't have a crisp answer yet.

Internally it's me plus my engineering lead and our CEO. Sales is aware this needs to happen but they're not driving it. I'm the one who needs to show up with a proposal.

**Assistant:**
Good context. So the external pressure is mostly optics right now — that's actually useful, because it means you have time to be thoughtful rather than reactive. The real challenge is you need a *genuine* answer, not a marketing response to marketing.

That points to the core problem being: **what does AI actually do for a finance team using expense management software?** The board story and the budget case both flow from that — but only if the answer is real.

Let me ask the more grounding question: **where do your users actually suffer today?** When a finance manager or an employee thinks about expenses — submitting, reviewing, approving, reconciling, reporting — what's the part that's genuinely painful or slow?

## Turn 3

**User:**
Honestly, two things come to mind. The OCR is a real pain point — receipts come in, the extraction is wrong, users have to manually fix line items. That's probably happening on 30% of submissions. People grumble about it.

The other one is categorization. We have a rules-based system for suggesting which expense category something falls into, and it's wrong enough that most users just ignore the suggestion and pick from a dropdown themselves. That's friction on every single expense.

Those are the two things I hear about most in support tickets and from our CS team.

**Assistant:**
Those are excellent — and importantly, they're *workflow-embedded* problems, not "wouldn't it be nice" features. That's the right place to start with AI.

A few things I notice: both of these have the same shape — AI replaces a broken or absent automation with something that actually works, reducing manual correction. That's a much stronger story than "we added a chatbot." It's accuracy and time savings at every single submission.

Let me push on the scoping questions:

**On OCR** — is that your own OCR pipeline, or a third-party service you're passing receipts through? And is the failure mode mostly wrong numbers/amounts, or is it more structural (wrong fields, missing line items)?

**On categorization** — does each customer have their own chart of accounts / category taxonomy, or do you use a standardized set? This matters a lot for how you'd build it — per-company learned models versus a shared classifier.

And one more: **do you have a sense of how many expense submissions you're processing monthly?** Order of magnitude is fine. I'm asking because it'll shape the "what's the impact" part of the budget case, and also because some approaches that work at 10K submissions/month are different from what you'd want at 1M.

## Turn 4

**User:**
OCR is third-party — we're piping receipts through a vendor service. The failure mode is all over the place, honestly. Wrong amounts, merchant names garbled, sometimes missing fields entirely. It's not one clean failure type.

On categorization — customers have their own chart of accounts. That's a core part of the product, they map it to their NetSuite or QuickBooks setup. So it's not a standardized taxonomy, it varies by company.

Volume — rough ballpark, probably 2-3 million submissions a month across the customer base. We've never really broken that down for a business case before but that's my estimate.

**Assistant:**
Okay, now I can see the shape of this clearly.

At 2-3M submissions/month, even modest accuracy improvements are enormous in aggregate. If OCR is failing on 30% of submissions, that's potentially 600K-900K manual corrections per month across your customer base. If you cut that by half, that's hundreds of thousands of hours saved annually — that's a real business case number, not a hand-wavy "AI is the future" argument.

Here's what's interesting technically: **both problems are now much more tractable than they were 2 years ago.**

For OCR — modern vision models (GPT-4o, Claude, Gemini) are dramatically better at receipt extraction than traditional OCR vendors. You could augment or replace your vendor pipeline with a vision LLM call, get structured output (amount, merchant, date, line items), and likely cut that 30% failure rate significantly. It's a relatively contained change.

For categorization — you actually have a hidden asset: **historical approved transactions per company**. Every time a user picks a category and it gets approved, that's a labeled training example. You can use that company's history as few-shot context for an LLM categorizer. Personalized per company, improves over time, no need for a shared taxonomy.

Before I help you frame the roadmap and the ask — one more thing I need to understand: **what's your engineering capacity here?** How big is the team, and do you have anyone with ML/AI experience, or would this be net-new for them?

## Turn 5

**User:**
22 engineers total. Nobody has shipped ML features. We have one backend engineer who took a Coursera ML course and is enthusiastic about it, but that's it. This would be genuinely new territory for the team.

That's actually part of what I need to figure out — do I need to hire someone, bring in a contractor, use an API-based approach that doesn't require deep ML expertise? I have a budget conversation coming up and I don't have a number to ask for yet.

**Assistant:**
This is actually clarifying, not a problem. It changes the answer from "should we do ML?" to "should we use ML APIs?" — and the answer to the second question is almost certainly yes, and it doesn't require hiring ML engineers.

Here's why: both problems — receipt extraction and categorization — are solvable today by calling a vision LLM API with a well-crafted prompt. You're not training models. You're writing software that calls an API and parses structured output. Your existing backend engineers can do that. The Coursera engineer is a bonus, not a requirement.

The work is really:
- **Integration plumbing** — route receipts through a vision model call, parse the output, feed it back into your submission flow
- **Prompt engineering** — get the model to return exactly the fields you need reliably
- **Evaluation** — measure before/after accuracy so you can prove it worked
- **Cost and latency management** — LLM API calls aren't free or instant, you need to handle that gracefully

That's a 2-engineer, 6–8 week proof of concept. Not a year-long ML platform build.

**The budget ask probably has three lines:**
1. Engineering time (internal reallocation, no new headcount initially)
2. API costs — at your volume this could be meaningful, worth modeling
3. Possibly a short-term advisor for 4–8 weeks to help set up the architecture and evaluation framework right the first time

One thing I want to flag: at 2-3M submissions/month, API costs could add up fast. Do you have a rough sense of what you're currently paying the OCR vendor? Because there's a real question of whether you're swapping one cost for another — or whether the accuracy improvement justifies a cost increase.

## Turn 6

**User:**
That framing actually helps a lot. I was mentally preparing for a "you need to hire two ML engineers" conversation, so this is different than I expected.

On the OCR vendor cost — I'd have to pull the actual number, but it's not nothing. If we're swapping one line item for another I need to know that going into the budget ask. That's a fair point.

Can we work toward what this actually looks like as a proposal? I need to walk into two conversations — one with the CEO and board, one with my engineering lead — and they need different things. The board wants a narrative. My engineering lead wants to know what we're actually asking him to build. Can you help me structure both?

**Assistant:**
Yes — and they're actually the same story told at different altitudes. Getting that right is the work. Let me make sure I have what I need to structure both well.

**I can already see the shape of the engineering proposal** — it's concrete enough to draft. Phase 1: receipt extraction POC, 2 engineers, 6–8 weeks, measurable accuracy target. Phase 2: per-company smart categorization. API-based, no ML hires. Evaluation framework baked in from day one.

**The board narrative** needs one more thing from you: what's the angle on the competitor? You have two choices —

- **Ignore them explicitly** — don't mention the competitor, just tell a confident story about your roadmap grounded in customer pain. (Stronger if your AI story is genuinely better.)
- **Address it head-on** — acknowledge the market is moving, position your approach as more substantive. (Works if you can credibly say "they announced, we're shipping.")

Which of those feels right given what you know about the competitive situation? And roughly how many weeks until the board meeting — are we talking 6 weeks or 12?

That'll let me help you structure both documents. While you answer, I'll get the rest of our notes into shape.

## Turn 7

**User:**
Board meeting is probably 10 weeks out. So there's a chance — not a guarantee — that we could be running a POC by then, which changes the narrative from "here's our plan" to "here's what we're already testing."

On the competitor — given that their announcement was mostly marketing and I haven't seen anything real from them, I think the confident story grounded in customer pain is the right call. If I bring them up and then can't say anything specific about what they actually built, it just makes us look reactive. Better to say "here's the user problem, here's what we're doing about it, here's early evidence it works."

How do you want to structure this from here? Do you have a document we can build out, or do you want to keep talking through it?

**Assistant:**
Ten weeks with a possible POC changes everything — "here's what we're already testing" is a completely different kind of board moment than a slide deck with boxes and arrows. That's the goal.

Let me build the actual documents now. I have enough. I'll write the core planning docs, then draft the two things you need to walk into those rooms with — the board narrative and the engineering proposal. Give me a moment.Now the two artifacts you'll actually walk into the room with:Okay — both documents are drafted. Here's where things stand:

**Board narrative** — structured as a 5-minute discussion arc: the specific problem, why the timing is right, what you're doing, why it compounds, what you're asking for. The "we're running a POC right now" line is the most powerful sentence in it — if you start the POC before that meeting, you get to say it.

**Engineering proposal** — specific enough that your engineering lead can read it and respond with "yes, we can do this" or "here's what I'd change." Week-by-week breakdown, clear exit criteria, risk table, explicit list of what it's *not*.

**One open item in both:** the OCR vendor cost number. That's the only gap. Pull it before either conversation — you don't want the CEO asking "what does this cost?" and not having the comparison ready.

A few things worth checking before you finalize:
1. Does the 2-engineer, 8-week estimate feel right to your engineering lead, or should you validate that with him first before taking it to the CEO?
2. Do you have access to a labeled set of ~500 historical receipts with known-correct values? The evaluation framework depends on that.

What would you like to work on next — sharpen either document, think through failure modes ("what could go wrong with this plan"), or something else?

## Turn 8

**User:**
Can you share what you actually wrote? I'd like to read both documents before I take them anywhere. And yes — I should probably run the engineering estimate by my lead before I commit to a number in front of the CEO. That's good hygiene. On the labeled receipts — that's a real question, I'd need to check with the team on what's accessible in our data pipeline.

**Assistant:**
Here they are in full.

---

**Board Narrative: AI Strategy**

> **The one-paragraph version**
> Expense management is a workflow product — the value is in frictionless submission, accurate data, and fast approvals. AI makes all three better. We're building it into the core submission flow, starting with the two highest-friction points our customers tell us about: receipt extraction and expense categorization. This isn't a chatbot feature or a roadmap slide — it's a targeted, measurable improvement to something every one of our users does every day.

**Narrative arc (5-minute board discussion):**

**The problem is specific.** About 30% of receipt scans require manual correction. Category suggestions are wrong often enough that most users just ignore them. That's friction on every single submission, for every user, every day.

**The opportunity is now.** The underlying technology has crossed a threshold in the last 18 months. The approach doesn't require ML engineers or infrastructure — it's API-based, executable by our existing team.

**What we're doing.** Running a POC on receipt intelligence — swapping our OCR vendor pipeline for a vision model. Target: cut manual correction rates from 30% to under 10%. In parallel, designing a per-company smart categorization system that learns each customer's chart-of-accounts mapping from their own approval history.

**Why this compounds.** Every approval is a training signal. This starts as an accuracy improvement; it becomes a switching-cost moat.

**What we need.** Two engineers focused for 8 weeks, plus a decision on API costs vs. our current OCR contract.

**QBR talking point:**
> "We're embedding AI directly into expense submission — the core workflow. Near-term: dramatically better receipt extraction and categorization suggestions that match your chart of accounts. We're in early testing now. The design point is AI that works invisibly when it works, not a new interface to learn."

---

**Engineering Proposal: AI Receipt & Categorization**

**Phase 1: Receipt Intelligence POC (Weeks 1–8)**
- Replace/augment OCR vendor with vision LLM API (GPT-4o, Claude)
- Structured JSON output: amount, merchant, date, line items, currency
- Needs: 2 backend engineers, API access, ~500 labeled historical receipts
- Exit criterion: manual correction rate below 10%

| Weeks | Work |
|-------|------|
| 1–2 | API selection, integration, structured prompt v1 |
| 3–4 | Evaluation framework, baseline accuracy |
| 5–6 | Prompt iteration, edge cases, fallback logic |
| 7–8 | Controlled rollout, live accuracy metrics |

**Phase 2: Smart Categorization (Weeks 6–16)**
- LLM classifier + each company's approval history as few-shot context
- No custom model training — uses existing approved transactions as signal
- Exit criterion: >60% user acceptance of suggested category on pilot cohort

**Risks covered:** accuracy misses, API cost delta, latency, prompt reliability at scale.

**The ask:** 2 engineers for 8 weeks · API costs [TBD vs. OCR contract] · Optional advisor $30–60K

---

Two things to do before either conversation: validate the 8-week estimate with your engineering lead, and pull the OCR vendor cost. Everything else is ready. What do you think — anything in here that doesn't feel right, or that needs a different emphasis?

## Turn 9

**User:**
This is solid. The board narrative feels right — the "every approval is a training signal / switching-cost moat" line is exactly the kind of thing that lands in a board room.

One flag: the QBR talking point says "we're in early testing now." I can't say that yet. I'd need to either start the POC first or soften it to "we're beginning testing this quarter."

The engineering proposal looks usable. I'll want to sit down with my engineering lead and walk through it — the week-by-week is helpful for that conversation. The $30–60K advisor line is useful too, gives me something concrete to put in the budget ask.

My main outstanding question: on the categorization exit criterion — 60% user acceptance on a pilot cohort — how did you land on that number? I want to make sure I can defend it if someone pushes back.

**Assistant:**
Good catch on the QBR line — easy fix, I'll update it. "We're beginning testing this quarter" is actually stronger anyway; it's a commitment, not a status report.

On the 60% number: I'll be honest about how I arrived at it, because that's exactly what you need to be able to say when someone pushes back.

**The logic:**

The current baseline is effectively 0% — users ignore the suggestion and go to the dropdown. So any meaningful threshold needs to clear "most of the time, the AI is right." 60% is the lowest number that achieves that while still being a majority. It's also the approximate breakeven for user experience: if the suggestion is wrong more than it's right, you've added a dismissal step to an already-manual workflow and made it worse.

**How to defend it:**

> "The rules-based system has near-zero acceptance today — users have learned to ignore it. 60% means the AI is right more often than not, every time. That's the threshold where the feature saves time rather than creating a new thing to dismiss. We picked it as a conservative bar — if we hit 60% on the pilot cohort, we have clear evidence the approach works. We'd expect it to improve from there as each company's history grows."

**The honest caveat you should know:** the number is somewhat judgment-based, not derived from a study. Your engineering lead might want to adjust it based on their intuition about what "shippable" feels like, and that's a legitimate conversation. What matters more than the specific number is that you have *a* number with a rationale — that's what boards and engineering leads actually want to see.

If someone pushes hard, the right response is: "We'll validate the threshold in the pilot before committing to broad rollout." That's the real protection.

Let me update the QBR line now:Done. You're in good shape to take both documents into those conversations. The two things still on your plate before you do: validate the timeline estimate with your engineering lead, and pull the OCR vendor cost number. Everything else is ready.

Anything else you want to work through — failure modes for the plan, or how to handle specific objections you're anticipating?

## Turn 10

**User:**
The 60% rationale is clear and defensible — I can work with that.

Actually yes, let's do failure modes. Specifically: what are the ways this blows up after we've already committed? I'm less worried about "what if the POC fails" and more worried about "what if we ship it and it creates new problems we didn't anticipate." That's the thing that keeps me up at night with any AI feature.

**Assistant:**
This is the right question to ask, and the answer is more interesting than the standard "what if accuracy is bad" list. Let me think through the real post-ship failure modes — the ones where you've committed, users are on it, and something goes sideways in a way you didn't design for.There are three categories that matter here, ordered by how much they should worry you:

---

**Category 1: Financial data integrity failures** *(these are the ones that keep you up at night)*

**Confident hallucination on amounts.** Vision LLMs can return a plausible-but-wrong number with no signal that it's wrong — no blank field, no obvious garbling, just $120 instead of $1,200. The old OCR failed visibly; users learned to check it. The new system is right 90% of the time, so users stop checking. That one wrong amount gets approved, reimbursed, and hits the books. Worse at scale: this isn't a demo, it's 2-3M submissions/month.

*Mitigation:* Confidence scoring and explicit uncertainty signals in the UI. When the model's extraction is ambiguous, show it — don't silently serve the result. Also: audit logging from day one so you can reconstruct what the AI returned vs. what got submitted.

**Miscategorization with compliance consequences.** If the AI suggests "Meals & Entertainment" for something that should be capitalized, or categorizes a non-deductible expense as deductible, that's not a UX problem — it's a tax and audit liability for your customer. Finance teams have compliance obligations. The AI making a confident wrong suggestion is worse than no suggestion at all for this class of error.

*Mitigation:* For high-value or high-risk expense types (anything above a threshold, anything touching specific GL codes), either suppress the AI suggestion entirely or require explicit user confirmation. Don't treat all categorizations as equal risk.

---

**Category 2: Third-party dependency failures** *(medium-term strategic risk)*

**Data privacy exposure you didn't anticipate.** You're sending receipt images — which may contain hotel room numbers, personal addresses on delivery receipts, meal details, account numbers — to OpenAI or Anthropic's API. Some of your enterprise customers will have contractual restrictions on sending data to third-party AI services. Some are in jurisdictions with GDPR implications. If this surfaces after you've shipped, you have a customer escalation problem, not a product bug.

*Mitigation:* Before you ship publicly, audit your customer contracts for data processing restrictions. Update your DPA (Data Processing Agreement). Give customers an opt-out. This is a legal/compliance conversation that needs to happen in parallel with the POC, not after.

**Model drift breaking your prompts overnight.** OpenAI ships a GPT-4o update. Your carefully tuned prompt no longer returns well-structured JSON reliably. Acceptance rates drop, extraction errors spike. You don't know why immediately. This is a real operational risk with API-dependent AI features that doesn't exist with a traditional vendor contract.

*Mitigation:* Pin to specific model versions where the API allows it. Build regression tests into your evaluation framework that run on a schedule. Alert on accuracy drops before customers feel them.

---

**Category 3: The "AI amplifies your bad data" problem** *(easy to miss, slow-burning)*

**Learning bad habits from bad history.** Your categorization model is trained on each company's approval history. But some companies have years of approvals that were technically miscategorized — a finance manager rubber-stamping submissions without checking the category. The AI learns their patterns and recommends them confidently. You've made incorrect categorization *sticky* and given it an air of authority.

*Mitigation:* Consider a confidence threshold below which you show the suggestion as tentative rather than a strong recommendation. And think about whether to weight recent approvals more heavily than old ones — a company's chart of accounts mapping from 3 years ago may not reflect current practice.

**Uneven performance creating a two-tier product.** The categorization model works well for customers with 18+ months of history, poorly for new customers with sparse data. You ship it uniformly and new customers get a worse experience — an AI that's confidently wrong more often than the old rules engine. Churn risk isn't from your best customers, it's from newer ones who haven't built the history yet.

*Mitigation:* Gate the feature by company tenure or transaction volume. New customers get the old rules engine until they've accumulated enough history. This is embarrassing to explain but much better than shipping a feature that actively degrades the new customer experience.

---

The one I'd prioritize above all others before you ship: **sort out the data privacy and DPA question early.** It's the failure mode most likely to create a customer escalation that's genuinely out of your control to fix quickly, and it's the one that's easiest to address now while you're still in POC.

Want me to write these up as a structured failure document, or does this give you what you need to bring into the conversation with your engineering lead?

## Turn 11

**User:**
The confident hallucination one is genuinely concerning — you're right that we've trained users to check OCR because it fails visibly. If we make it mostly right, they stop checking, and then the one-in-ten wrong amount gets through. That's a support nightmare.

The data privacy point I had not thought about at all. That's a real gap. We have enterprise customers who are definitely going to ask about this, and I don't want to find out about contractual restrictions after we've shipped. That needs to go on the pre-ship checklist explicitly.

Write these up as a structured document — I want to bring the full picture to my engineering lead, not just the happy path. And add the data privacy item as a dependency, not just a risk. We shouldn't ship Phase 1 without having resolved that.

**Assistant:**
Done. Here's what's in the document:

**Seven failure modes, in priority order:**

| # | Failure | Severity | Phase |
|---|---------|----------|-------|
| F1 | Confident hallucination on amounts | High | Phase 1 |
| F2 | Miscategorization with compliance consequences | High | Phase 2 |
| F3 | Data privacy exposure | **Pre-ship dependency** | Phase 1 |
| F4 | Model drift breaks prompts without warning | Medium | Both |
| F5 | AI amplifies historical miscategorization | Medium | Phase 2 |
| F6 | Uneven performance for new customers | Medium | Phase 2 |
| F7 | Latency degradation at p99 | Low–Medium | Phase 1 |

Each has a causal chain and a concrete management plan, not just "monitor it."

F3 (data privacy) is written as a hard dependency with a checklist: legal review, DPA update, opt-out mechanism. The framing is "Phase 1 does not ship without these" — same weight as a technical exit criterion. That gives your engineering lead something to schedule in parallel with the POC, not after it.

The document ends with a pre-ship checklist you can hand directly to your engineering lead.

One thing worth raising with your lead: F1 (confident hallucination) and F7 (latency) are design decisions that need to be made upfront — async extraction with visible processing state, and confidence-gated confirmation for large amounts. These aren't things you can bolt on after the fact.

Anything else to work through, or are you in good shape to take this into those conversations?

## Turn 12

**User:**
This is what I needed. I came in with a vague "add AI" mandate and I'm leaving with a scoped proposal, a board narrative, and a list of things that could blow up in my face. That's a different conversation than I would've had if I'd just started writing slides.

Next step for me is the engineering lead conversation — I'll take the proposal and the failure doc, get his reaction on the timeline, and pull the OCR cost number. Then I'll refine the budget ask and take it to the CEO.

Thanks for not just giving me a "here are five ways companies use AI" response.

**Assistant:**
Good luck with the engineering lead conversation. A few things to keep in mind when you walk in:

- **Lead with the failure doc, not the happy path.** Engineers trust proposals more when the failure modes are already named. It signals you've thought it through.
- **The OCR cost number will shape the whole budget ask** — get that before you talk to the CEO, not after.
- **The data privacy item needs legal in the room.** It's not an engineering question; your lead can't resolve it. Flag it as a parallel workstream that needs to start now.

When you come back — after the engineering conversation, or when you're ready to refine the budget ask or prep for the CEO — everything we worked through is saved. The board narrative, engineering proposal, and failure analysis are all in the protocol directory and will be here when you return.
