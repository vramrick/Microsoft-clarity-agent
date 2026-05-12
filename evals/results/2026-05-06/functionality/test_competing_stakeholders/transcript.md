## Turn 1

**User:**
Hey, I need some help thinking through a situation that's been weighing on me. I'm a Director of Engineering and I'm caught between competing priorities — sales made a commitment to a customer that my engineering team says we can't hit without blowing up other things we're already committed to. I'm trying to figure out how to balance all of this without everything catching fire.

**Assistant:**
That's a genuinely tough spot — the classic tension between what sales promises and what engineering can deliver, with real commitments already in flight.

To help you think through this clearly, a few questions:

**What's the commitment?** What did sales promise, and roughly when? Is this a signed contract, a verbal promise, or something in between?

**What's already at stake?** What are the existing commitments that engineering says would get blown up — are those internal (a roadmap, another team's dependency) or external (other customers, a launch date)?

And maybe most importantly: **who knows what right now?** Has this surfaced yet with your leadership, the customer, or is it still mostly between you and your team?

## Turn 2

**User:**
So — VP Sales committed to a large enterprise customer that we'd ship SSO and provisioning features by end of Q2. That's SAML, SCIM, fine-grained roles, audit logging. Worth about $1.2M ARR if it closes. The commitment was verbal but it's now in the customer's procurement timeline, so it's basically real.

My most senior lead, Raj, says Q3 at earliest. His team is already heads-down on a platform migration that my VP of Engineering prioritized last quarter. Slipping the migration means slipping Data Retention and Growth Metering work downstream — those are internal commitments, but real ones.

As for who knows: VP Sales knows there's tension. My VP of Engineering has said "I'll back what you decide" which is... not super helpful. And the CEO hasn't been briefed in any real way. I've been trying to handle it at my layer.

**Assistant:**
This is a lot — and one thing stands out immediately: your VPE's "I'll back what you decide" is a red flag. This is a cross-functional resource conflict involving a $1.2M deal and competing organizational priorities. That's not a Director-layer decision — that's a VP+ conversation that hasn't happened yet.

But before going there, a few things I want to understand better:

**On the scope:** SAML + SCIM + fine-grained roles + audit logging is a lot. Has anyone pressure-tested with the customer what's actually blocking the deal vs. what's nice-to-have? Sometimes "we need all four" actually means "we need SSO to satisfy security review and the rest can follow."

**On the migration:** When you say slipping it creates downstream slippage — how bad is that, really? Is Data Retention a customer-facing commitment with its own deadline, or more of an internal quality/technical debt investment?

**On what you're trying to solve:** Are you looking for help thinking through *what decision to make*, or more *how to navigate the organizational dynamics* around whatever you decide? Because those are related but different problems, and it sounds like the org dynamics piece might actually be the harder one here.

## Turn 3

**User:**
On scope — actually, that's a good question and one I haven't fully pushed on. The contract language apparently has some flexibility around roles specifically. So there's a scenario where we ship SAML for Q2, defer SCIM and fine-grained roles to Q3, and it still satisfies procurement. I haven't validated that with Sales or the customer directly though.

On the migration — Data Retention has some regulatory angle for a couple of existing customers. It's not imminent-crisis-level, but it's not nothing. A 6-8 week slip is probably manageable, but it starts a chain of "we'll get to it" that worries me.

And honestly, both. I need to figure out what the right call is AND how to get there without a war with Sales. But if I'm being honest, I think I also know I'm probably going to have to escalate to the CEO and I've been avoiding it. I don't love escalating.

**Assistant:**
The scoped delivery angle is potentially the most important thing in this whole situation — and the fact that it hasn't been validated yet is where I'd focus first. You might be carrying a lot of weight on a tradeoff that doesn't fully exist.

Here's what I'm hearing as the actual shape of this:

**There might be a viable path no one has confirmed yet.** SAML in Q2, SCIM + roles in Q3 — if procurement accepts that, the platform migration stays intact, Data Retention slips a manageable amount, and the deal closes. But right now that's a hypothesis sitting in your head.

**The thing blocking you isn't the decision — it's that the right conversations haven't happened.** You need Raj to tell you whether SAML-only in Q2 is actually achievable without derailing the migration. You need Sales to find out whether the customer will accept the scoped delivery. And yes, you need the CEO in the loop.

On the escalation piece — I want to push on that a little. You said you know you need to do it and you've been avoiding it. What's the actual fear there? Is it being seen as someone who can't handle their domain? Not wanting to create a Sales vs. Engineering political situation above you? Something else?

That matters, because there's a version of escalating this that isn't "I can't solve this" — it's "I have a plan, here's the tradeoff, I need your sign-off." Those feel very different to a CEO. The second one is what you'd be doing if you go in with the scoped delivery option in hand.

## Turn 4

**User:**
Yeah, I think it's both of those things. I don't want to be the person who kicks problems upstairs when they could be solved at my level. And I'm genuinely worried about creating a Sales vs. Engineering thing — VP Sales is pretty forceful and I'd rather not have that fight in a room with the CEO if I can avoid it.

But you're right that going in with "here's the tradeoff, here's my recommendation, I need sign-off" is different from "help, I can't figure this out." And honestly the CEO is probably going to be annoyed if this surfaces later without warning, especially given the size of the contract.

Okay, so — the scoped delivery option. Let's say I go validate it. Raj confirms SAML-only is doable in Q2. Sales goes back to the customer and they accept it. What am I actually deciding at that point? Because even then, I feel like there are real tradeoffs I'd want the CEO to understand rather than me just solving it quietly.

**Assistant:**
That's exactly the right question — and it shows you're thinking about this the right way.

Even in the "scoped delivery validates" scenario, here's what you'd actually be deciding:

**1. Who owns the Data Retention risk.** A 6-8 week slip with regulatory implications for existing customers — even if manageable — is a risk that should be explicitly accepted by someone with the authority to accept it. If you absorb that quietly and it becomes a problem later, you own it alone.

**2. Whether the Q3 SCIM/roles commitment is real.** Deferring to Q3 creates a new promise. To the customer, to Sales. Is that commitment being made with the same rigor (or lack thereof) as the Q2 one was? Someone needs to make it deliberately, not just as the residue of solving the current problem.

**3. What happens to the process that created this situation.** VP Sales made a verbal commitment without an engineering sign-off loop. If that doesn't get addressed, you'll be back here in six months with a different customer.

So even in the clean scenario, you're not just "solving it quietly" — you're making organizational decisions about risk tolerance and process. Those belong in a room with the CEO, not because you can't handle your domain, but because they're actually above your domain.

The framing I'd suggest: *"I've worked through this and I have a recommendation. But there are two things I need from you: sign-off on accepting the Data Retention slip, and a conversation about how we prevent this pattern with Sales going forward."*

That's not escalating a problem. That's doing your job and asking the CEO to do theirs.

Does that framing feel usable, or is there something about the dynamic with your CEO or VP Sales that makes it more complicated?

## Turn 5

**User:**
That framing actually helps a lot. The "sign-off on the risk" piece especially — I think I was unconsciously treating this like my problem to solve cleanly, when some of it is genuinely above my pay grade.

The VP Sales dynamic is real though. He's going to come into that room pushing hard for the full Q2 commitment and probably framing any scope reduction as Engineering being difficult. I've seen it before. I'm a little worried that if I go to the CEO with a recommendation and Sales pushes back hard in the room, it turns into a negotiation I lose — and then I'm worse off than if I'd tried to align with Sales first before bringing the CEO in.

So maybe the sequencing matters here? Like, do I try to get Sales to co-own the scoped delivery option before I take it to the CEO? Or does that just give him the chance to kill it before it gets there?

**Assistant:**
The sequencing instinct is right — this matters. But I'd reframe the choice slightly.

The risk with pre-aligning Sales is that you're asking him to *agree* to something before the CEO meeting. That gives him veto power. But there's a different conversation you could have with Sales that doesn't carry that risk: instead of "will you co-own this scoped option," ask "will you find out if the customer will accept it."

That's not negotiation — it's information-gathering. And it's genuinely collaborative. You're not proposing scope reduction; you're saying: *"I need to know if this deal can still close with SAML in Q2 and SCIM/roles in Q3, because that's the question that determines what we recommend to the CEO. Can you get me that answer?"*

He can't really say no to that. And if the customer says yes, he's now the one who validated it — which makes it much harder for him to fight it in the room.

**The sequencing I'd actually suggest:**

1. **Raj first** — confirm SAML-only in Q2 is achievable without blowing up the migration. Quick, internal, you control it.
2. **Sales as information-gatherer, not decision-maker** — ask him to validate customer acceptance of scoped delivery. Collaborative framing.
3. **Brief the CEO informally before any formal meeting** — a quick heads-up: "There's a customer commitment situation I'm working through, I'll have a recommendation for you by [date]." This means the CEO isn't blindsided and has time to think. It also subtly signals that you're in control of this.
4. **Formal meeting with full picture** — recommendation, tradeoffs, what you need from them.

The informal CEO heads-up is probably the most underrated move here. It reframes the whole dynamic — you're not escalating a crisis, you're briefing your CEO on something you've already largely solved.

What's your read on your CEO? Is this someone who'd appreciate that heads-up, or someone who'd rather just get the full recommendation when it's ready?

## Turn 6

**User:**
He'd appreciate the heads-up. He doesn't like surprises — especially on anything revenue-adjacent. So yeah, a quick "heads up, here's the situation, I'll have a recommendation by Thursday" is probably exactly right. That's actually relieving to hear framed that way.

Okay. I think I have a clearer picture of what this week looks like. Talk to Raj today or tomorrow, get Sales to go back to the customer on the scoped option, drop the CEO a heads-up note, and come back with a full recommendation once I have the customer answer.

The one thing I'm still sitting with is the process question — the "how do we prevent this with Sales going forward" piece. I know it needs to be part of the CEO conversation, but I'm a little worried about how to raise it without it sounding like I'm throwing VP Sales under the bus. Any thoughts on how to frame that piece?

**Assistant:**
The key move is to make it about the gap, not the person — and to position yourself as proposing a solution, not filing a complaint.

Something like: *"One thing I'd like to use this situation to address is how we handle enterprise feature commitments going forward. We don't currently have a lightweight check-in process between Sales and Engineering before timelines get shared externally. I'd like to propose one."*

Notice what that framing does:
- It doesn't say VP Sales did something wrong — it says there's no process, which is true
- It positions you as solving a company problem, not settling a grievance  
- It gives VP Sales a graceful exit — he wasn't reckless, he was operating in a gap

VP Sales may even welcome it. He's presumably not happy that his $1.2M deal is at risk either. A quick "engineering feasibility check before we put a date in a customer's procurement timeline" protects him too.

The process itself doesn't need to be heavy — probably just a standing agreement that any feature commitment with a specific timeline gets a 24-48 hour engineering read before it leaves the building. Frame it as lightweight and sales-enabling, not a gate or a blocker.

---

You've got a solid plan. To summarize where you've landed:

- **Today/tomorrow:** Talk to Raj — confirm SAML-only Q2 feasibility
- **This week:** Ask Sales to validate scoped delivery with the customer
- **Soon:** Drop the CEO a heads-up note
- **By Thursday:** Full recommendation with tradeoffs and a process proposal

That's a Director handling a hard situation well. What would be most useful to work through next — how to structure the CEO recommendation itself, or something else?

## Turn 7

**User:**
No, I think I actually have what I needed. The CEO recommendation will be easier to structure once I have the answers from Raj and Sales — at that point it's just laying out the options and the tradeoffs, which I can do.

Honestly this was helpful. I came in thinking the problem was "how do I balance everything" and I think the real problem was that I was trying to solve something that was only partly mine to solve. The framing around escalating as someone who has a plan — not someone who needs rescuing — makes this feel a lot more manageable.

Thanks. I've got enough to move on this today.

**Assistant:**
Good luck today. That reframe you landed on — *"partly mine to solve"* — is the one worth holding onto. The action plan is solid and the sequencing is right.

Come back when you have the answers from Raj and Sales if you want help structuring the CEO recommendation.
