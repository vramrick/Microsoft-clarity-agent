## Turn 1

**User:**
Hi — I'm hoping you can help me think through something. I'm a Director of Engineering at a B2B SaaS company, and I'm caught in the middle of a conflict between Sales and Engineering that I've been trying to resolve for three days now without much luck.

The short version: our VP of Sales committed to a large enterprise customer that we'd ship an SSO and user provisioning feature set in Q2 — it's a $1.2M expansion deal. The problem is, I wasn't in the room when that commitment was made, and my most senior engineering lead says Q3 at the earliest. The work is genuinely complex (SAML, SCIM, fine-grained roles, audit logging), and the team already has a platform migration underway that was prioritized last quarter.

I'm trying to figure out how to balance these competing needs. What do I do this week?

**Assistant:**
That's a genuinely hard spot — and the 3-day stall suggests it's not just a scheduling problem, it's a political one too.

Before I can help you figure out what to do *this week*, a few things would really sharpen the picture:

1. **What does "Q2" actually mean in practice?** Is this end-of-June, or is there a specific contractual date? How many weeks are we talking?

2. **What exactly did the VP of Sales commit to?** Is it the full feature set (SAML + SCIM + roles + audit logging), or is there room to interpret what "SSO and user provisioning" means? Sometimes these commitments are vaguer than they feel in the moment.

3. **Who else knows about this?** Does your CTO/VP Eng know? Has this surfaced at the exec level, or is it still being handled between you and the VP of Sales?

4. **What's the state of the platform migration?** Is it blocking the SSO work, or could they run in parallel with a separate squad?

The answers change the strategy significantly — some paths here are about buying time, some are about scoping, and some are about escalating cleanly before it escalates messily.

## Turn 2

**User:**
Good questions. Let me go through them.

Q2 means end of June — the customer's procurement deadline. We probably have 7 weeks.

On what Sales committed to — that's actually part of the problem. I've seen the email chain and it's not precise. It says "SSO and user provisioning capabilities." That's it. So there's some room, but I don't know how much wiggle room the customer will accept versus what they *think* they were promised.

VP of Engineering knows — he's the one who prioritized the platform migration in the first place. He's said "I'll back what you decide" which honestly feels like he's punting. The CEO has not been briefed in any substantive way. I've been trying to handle it at my layer.

On the migration: it's the same team. Raj's team is doing both. We don't have a separate squad we could spin up, and staffing up would take longer than 7 weeks regardless.

**Assistant:**
This is actually more tractable than it feels right now. A few things stand out:

**The vague commitment is your biggest asset.** "SSO and user provisioning capabilities" is not a spec. SAML SSO alone — without SCIM automation, without fine-grained roles, without audit logging — *is* SSO and user provisioning in the way most enterprise buyers think about it. The question isn't whether you can negotiate scope; it's whether you know what the customer's minimum acceptable version is. Right now, you don't.

**The VP of Sales is your next conversation, not your adversary.** They need this deal too. The right framing isn't "you made an impossible promise" — it's "I need your help understanding what the customer actually needs, so I can find us a path." Go into that conversation asking: *What problem is this customer trying to solve? Is SSO a procurement checkbox for them, or is it actively blocking their onboarding?* That answer changes everything.

**"I'll back what you decide" is actually permission, not abdication.** Your VPE just handed you the authority to make a call and bring a recommendation. Use it — but bring him a concrete proposal, not the problem.

Here's how I'd structure the week:

**Today/tomorrow:** Get a real scope conversation with Raj. Not "can you do Q2?" — that's a yes/no trap. Instead: *"If we drew a hard line at SAML SSO + basic user invitations via IdP, no SCIM, no audit log, what would that take? And what would we have to pause on the migration?"* You need a number, not an estimate.

**Midweek:** Sit down with VP Sales — together, as problem-solvers. Share what you've learned about what's realistic and ask them to help you understand the customer's actual use case. Ideally you come out of this with: (a) a scope definition the customer might accept, and (b) Sales owning the customer conversation with you supporting.

**Thursday/Friday:** Brief VPE with a clear recommendation. Then, depending on what you learn about the customer's flexibility, either: prepare a phased delivery proposal, or flag to VPE that CEO may need to be involved in a customer relationship conversation. *Don't let the CEO get surprised.*

One thing I'm still uncertain about: **has anyone talked directly to the customer yet about this?** And do you know why SSO matters to them — is it a hard procurement blocker, a security compliance requirement, or something a champion wanted?

## Turn 3

**User:**
The VP Sales framing is useful — I've been going into those conversations a little defensively and that's probably not helping.

To your question: no one has talked to the customer directly about scope. That's been VP Sales' lane and I haven't pushed to get in it. But your point about "procurement checkbox vs. actively blocking their onboarding" is the exact thing I don't know, and it probably matters a lot.

My instinct has been that SAML alone might get us there — if it's a compliance checkbox situation — and I do have some scope reduction options I've been turning over. SAML in Q2 plus SCIM in Q3. Or basic SSO without fine-grained roles if the contract language lets us defer that. I haven't fully worked through which of those is actually viable.

What I'm not sure your week plan resolves is: what if Sales and I do all this work, come up with a phased proposal, and VP Sales goes back to the customer and they say no, it has to be the full set by June? At that point it does land on the CEO's desk whether I manage it there or not. I'm not sure I'm better positioned by having done three more days of prep versus just surfacing it now.

**Assistant:**
You're putting your finger on something real. Let me be direct about it.

You're not deciding between *prep first* and *escalate now*. Those aren't mutually exclusive, and treating them as a sequence is probably what's been costing you days.

**Brief the CEO tomorrow.** Not to dump the problem — to give visibility and potentially arm them. Something like: *"We have a commitment to a $1.2M customer that Engineering's current capacity may not support. I'm working with Sales on a phased proposal this week. There's a scenario where we need you involved in a customer conversation — I want you to see it coming."* That's a 15-minute conversation. It converts the CEO from a landmine into a resource, and it changes the dynamics with VP Sales too — people move differently when they know the CEO is watching.

The prep work still matters, but for a different reason than you think. If the customer says "full scope by June or we walk," you'll be asking the CEO to make a call — and the call is: *authorize pulling the platform migration entirely to hit this deal, or tell the customer we can't do it.* You need to show up to that conversation knowing what the migration pause actually costs, not just that it exists. That's not three days of work — that's one focused afternoon with Raj.

So the real week looks more like:

- **Today:** Get the actual cost of migration pause from Raj. One number: "if we stop the migration now and focus on SAML-only, what can we ship by June 30?"
- **Tomorrow morning:** Brief the CEO. Short, factual, "heads up, here's what I may need."
- **Tomorrow afternoon:** The collaborative conversation with VP Sales, now with CEO already looped.
- **By Thursday:** You either have a phased proposal the customer might accept, or you're walking into a customer call with the CEO and VP Sales already aligned on what you're offering.

The thing you want to avoid is the CEO hearing about this *from the customer* before they hear it from you. That's the only scenario that's genuinely bad for you.

Does the CEO have an existing relationship with this customer's champion, or would their involvement be cold?

## Turn 4

**User:**
Okay. That last point lands — the CEO hearing it from the customer first is genuinely the bad outcome I've been trying to avoid, and ironically I might be creating the conditions for it by waiting.

I've been framing "briefing the CEO" as escalating, like I'm failing to manage it at my level. But what you're describing is different — it's not handing it up, it's giving visibility before they need to act. That's a distinction I think I've been missing.

To your question: the CEO has met this customer's VP of IT at a conference, I think, but it's not a deep relationship. It wouldn't be cold exactly, but they're not texting each other either. So if the CEO does need to get on a call, it would be a managed thing, not a relationship call they could just make informally.

The thing that still makes me nervous: I walk into the CEO's office tomorrow with "here's a problem I haven't solved yet." Does that read as me being on top of it, or does it read as me coming to them without answers?

**Assistant:**
It reads as you being on top of it — but only if you walk in with the right framing. The framing is everything here.

There's a version of this conversation that reads as "I'm struggling and I need help." And there's a version that reads as "I'm managing something and I want to make sure you're not surprised." The content is nearly identical. The difference is posture and what you're asking for.

**What you're not saying:** "I don't know what to do."

**What you are saying:** Something like —

> *"I want to give you visibility on something I'm actively managing. Sales committed SSO to a $1.2M customer for Q2. Engineering's current capacity makes the full scope a stretch — my lead is saying Q3. I've got a meeting with Sales tomorrow to figure out if there's a scoped version the customer will accept, and I'm getting exact engineering numbers today. I think there's a viable path. But if the customer won't take a scoped version, we may need an executive presence on a call to hold the relationship. I wanted you to see that scenario coming rather than have it land on your desk cold."*

That's not "I have a problem I haven't solved." That's "I've been working this, here's my plan, here's the one thing that might require you." Those read completely differently.

The CEO's fear isn't that you came without answers. Their fear is being surprised. You walking in tomorrow is the thing that prevents the surprise. That's doing your job well, not failing at it.

One more reframe worth internalizing: you've been managing this for three days. You're not coming in fresh and overwhelmed. You're coming in with three days of context and a clear next step. That's a different posture than it feels like from the inside.

How are you feeling about the Raj conversation — do you have a good enough relationship that you can get a straight answer on what a SAML-only scope would actually take?

## Turn 5

**User:**
Yeah, Raj and I are solid. He's not going to sandbag me or tell me what I want to hear — if anything he leans toward surfacing bad news clearly, which is why I trust his Q3 estimate. I can have that conversation today and get a real answer.

The script you just wrote for the CEO — that's actually useful. I've been dreading that conversation partly because I couldn't see how to open it without it sounding like I was in over my head. The "I want you to see this coming" framing takes some of that pressure off.

I think I know what I'm doing this week. Get the real number from Raj today. CEO tomorrow morning, with that framing. VP Sales tomorrow afternoon. Come out of that with either a phased proposal or a flag that the customer won't flex, and brief VPE by Thursday with a clear recommendation.

Is there anything about the VP Sales conversation I should be thinking about specifically? That one still feels like it could go sideways — they've been pretty dug in on "we have to make this work."

**Assistant:**
The "dug in" position is almost certainly defensive, not strategic. They made a commitment, they feel accountable for it, and every Engineering conversation so far has probably felt like "you made a mistake and we can't fix it." That's a position people dig into, not out of.

So the single most important thing: **don't open with what Engineering can't do.** Open with the customer.

Something like: *"Before we talk about what's realistic on our end, I want to make sure I understand what Acme actually needs here. What's driving the SSO requirement for them — do you know if it's a procurement checkbox, a security mandate, something their IT team wants?"*

That opening does a few things. It signals you're trying to find a path, not assign blame. It gives VP Sales something to contribute rather than something to defend. And it gets you the information you actually need — because if VP Sales says "honestly, their VP of IT just wanted it and it's not a hard blocker," that's a completely different conversation than "it's in the contract language for their legal team."

A few other things to hold onto:

**Give them the agency to be the hero.** If you land on a phased proposal, VP Sales is the one who goes back to the customer with a creative solution — not admitting a mistake, but delivering a plan. That's a better story for them than "Engineering said no." Frame it that way explicitly.

**The CEO brief changes the room.** Once you've done that in the morning, you can mention it neutrally in the afternoon: *"I gave the CEO a heads-up this morning — wanted to make sure we had alignment if we need executive involvement in the customer conversation."* That's not a threat, it's information. But it signals that this is now a company-level situation, and it tends to focus people.

**If they stay dug in despite all this**, the right move is to name it directly but without heat: *"I hear that we have to make this work. I want to make it work too. The question is what 'this' means — and I think only the customer can tell us if a phased approach gets them there. Can we agree to find that out before we decide anything?"* That's hard to argue with.

The conversation goes sideways if it stays abstract — "Q2 is a commitment" vs. "Q3 is reality." It stays productive if it stays specific: what does the customer need, and is there a version of that we can actually ship?

## Turn 6

**User:**
The "open with the customer" framing is good. I've been going into that conversation with a capacity problem to explain, and you're right that it probably reads as blame even when I'm not intending it that way.

The CEO mention in the afternoon conversation — I want to make sure I use that right. The way you've framed it is neutral, informational. I just don't want it to land as "I went over your head," because VP Sales can be sensitive about that kind of thing.

But I think I know how to read the room on that. If the conversation is going well and we're problem-solving together, I probably don't need to mention it. If they're still dug in after the customer-first framing, then yes, naming it as "the CEO is aware and may be involved" refocuses things.

This has been genuinely useful. I came in feeling like I was stuck in a balance problem with no good answer, and I think what actually happened is I was treating "decide" like "escalate" and trying to avoid both. The clearer frame — brief the CEO, work with Sales as problem-solvers, bring VPE a recommendation — feels a lot more like something I can actually do this week.

**Assistant:**
That read on the CEO mention is exactly right — use it as a tool if you need it, not as a marker of progress.

You've named the core thing well: you weren't stuck on the problem, you were stuck on a framing. "Decide" and "escalate" felt like the same move, so you were avoiding both. Separating them — brief the CEO as *visibility*, bring VPE a *recommendation*, work Sales as *collaborators* — turns three uncomfortable conversations into three manageable ones.

The one thing this week's plan doesn't resolve is the structural problem: Sales made a commitment without Engineering in the room, and that will happen again unless something changes. You're in a good position to raise that after the immediate crisis is handled — not as a complaint, but as "here's a lightweight process change that would have saved us three weeks." That conversation lands better when you've just successfully navigated the situation rather than while you're still in the middle of it.

Good luck this week. If you want to think through how the Raj conversation goes, or work through what a phased proposal actually looks like once you have his numbers, come back and we can dig into it.
