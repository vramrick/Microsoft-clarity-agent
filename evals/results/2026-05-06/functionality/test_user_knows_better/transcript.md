## Turn 1

**User:**
I'm working on merge semantics for a rich-text CRDT — YATA-based ordering with a separate attribute layer for marks. The specific failure mode: when a mark range and a concurrent local insertion straddle the mark boundary, the merge ordering is correct but the insertion ends up attributed to the mark roughly half the time against user intent, depending on which side of the boundary the insertion logically belongs.

I've already looked at three approaches: (a) explicit attach-left/attach-right bits on each mark endpoint, Fuchs-Fuchs style; (b) deriving attachment intent from causal relationships in cursor metadata; (c) accepting the ambiguity and surfacing a UI disambiguation step on divergence. I've read Nicolaescu 2016, the Yjs source, the Automerge rich-text RFC, and a couple of slide decks on the topic.

I have two days before a design review. I want to think through these three options — spec complexity, runtime cost, intelligibility to the team — and find out if there's a fourth worth considering. What's your read?

**Assistant:**
Good, problem captured. Here's my read:

---

**Option (a) is the right answer.** The Automerge rich-text RFC went through exactly this analysis and landed on explicit expand/no-expand semantics per endpoint. Runtime cost is negligible (two bits per mark, one comparison during merge). The spec complexity is manageable and — critically — it maps onto a concept your team can reason about: "does typing at this boundary extend the mark?" For bold/italic/code, yes; for comments and hyperlinks, usually not. That mapping makes it explainable.

**Option (b) is elegant but doesn't actually solve the problem** — it moves it. Cursor positions in YATA don't have YATA identities, so applying causal reasoning to them requires you to re-implement sticky semantics at the cursor layer. If two clients have concurrent insertions at the boundary, you get different causal answers for each, and you're back to the same merge ambiguity one level up. The fundamental issue is that YATA gives you a total order on *characters*, not on *derived positions like cursor locations*. I'd want to understand your cursor metadata design more carefully before ruling this out entirely, but I'd be skeptical.

**Option (c) is giving up.** ~50% divergence is too frequent for a disambiguation UI to be workable. It also violates the core CRDT promise.

**A fourth option worth considering:** define expansion semantics at the *mark type* level rather than per endpoint instance. Bold = always right-sticky. Hyperlinks = closed. Comments = bounded. The stickiness bits live in a mark type registry, not on each mark in the document. This is option (a) with the complexity moved to schema rather than instances — simpler to implement and explain, at the cost of flexibility (you can't have a non-sticky bold range). For most editors, that tradeoff is fine.

---

A few things I'd want to sharpen before your review:

1. **What does "logically belongs" mean in your system?** Your description says misattribution happens when it's ambiguous which side the insertion belongs to. Is this purely a function of insertion position relative to the mark boundary, or does the mark type matter? The answer affects whether per-type or per-instance stickiness is the right granularity.

2. **What's your current mark endpoint representation?** If endpoints are anchored to character IDs in the YATA sequence (as in Yjs `RelativePosition`), option (a) integrates cleanly. If they're something else, the implementation story changes.

3. **Are overlapping marks a concern?** Two marks with different stickiness meeting at the same boundary can produce counterintuitive results. This is solvable but worth calling out at the review.

What does your current endpoint representation look like?

## Turn 2

**User:**
The endpoint representation is RelativePosition-style anchors on character IDs, yes — essentially what Yjs does. So (a) integrates cleanly on that front.

On the fourth option: that's what ProseMirror's mark schema does, and it's not a bad answer for a constrained editor. My hesitation is that we have user-created marks — comments, in particular — where the author's intent about boundary stickiness is genuinely variable. A comment "on this word" should be closed; a comment "starting here" arguably shouldn't be. Pushing that to the type registry loses that. So for our use case I think (a) at the instance level is the right granularity.

Your point about (b) is exactly my concern too. The cursor metadata approach appealed to me because it felt like it was tracking intent closer to the source, but you're right that you end up needing sticky semantics at the cursor layer and you've just deferred the problem. The only scenario where (b) would be cleaner is if you had causal information telling you *which client's insertion happened "first" relative to the boundary intent* — but in a concurrent scenario you don't have that without coordination.

So I'm landing on (a), per-instance, with the type registry as a default provider of the bits for common cases (bold = right-sticky, links = closed, comments = author-specified). That layers the two options rather than choosing between them.

The overlapping marks question is the one I haven't fully worked out. Two marks meeting at a boundary with different stickiness — can you say more about what you mean by counterintuitive? Are you thinking about the ordering of resulting attribute spans, or something at the merge level?

**Assistant:**
Good synthesis — layering type-registry defaults under per-instance bits is clean and handles the comment case well. Worth stating explicitly at the review so the team understands why you need instance-level rather than type-level.

On overlapping marks with conflicting stickiness — it's actually both, but in different ways:

**At the merge level, the problematic case is the "gap."** If Mark A ends closed at C5 and Mark B starts closed at C5, an insertion at C5 is claimed by neither. The character lands in an unformatted gap between two styled regions. Deterministic, correct per-spec, and consistently surprising to users who inserted text "inside" what looked like a styled region. For closed comment marks this is intentional; for adjacent bold+underline it probably isn't. The fix is a convention: never pair two closed endpoints at the same boundary — at least one side should be sticky. But this is a constraint you have to enforce at mark-creation time, not at merge time, so it's a spec concern more than a runtime concern.

**At the serialization level, the issue is span ordering.** When Mark A extends past Mark B's right endpoint (because A is right-sticky and B is closed), your serializer needs to emit something like `<A><B>...</B>x</A>` where `x` is the inserted character. Most span renderers handle this fine, but it requires your attribute-span flattener to correctly handle marks with different extents at the same boundary position. If your flattener assumes marks always nest cleanly, you'll get incorrect output. Worth an explicit test case.

**There's also an editor UX concern** that's separate from the CRDT: when the cursor sits at C5 and the user types, the editor has to decide which mark context the cursor is "in" to render the toolbar state (bold button depressed or not). The stickiness bits tell you the merge outcome, but the cursor's apparent mark membership needs to be derived from the same bits — otherwise the toolbar says "bold" and the typed character comes out plain, which is the most visible form of surprising behavior even if the CRDT is technically correct. This is implementation work beyond the CRDT spec itself.

So: merge-level gap case is real but addressable by a boundary constraint on mark creation; span ordering is an implementation concern for the flattener; cursor-context derivation is editor-layer work. None of these are blockers for choosing (a), but they're worth naming at the review so they don't surface as surprises post-decision.

---

With two days to review, I'd suggest your argument structure goes:

1. State the failure mode concisely (concurrent boundary insertion, ~50% misattribution)
2. Dispose of (b) and (c) in one sentence each — (b) defers the problem, (c) gives up on determinism
3. Present (a) with the type-registry-as-default layering as the design
4. Name the three second-order concerns (gap case, flattener, cursor context) with one-line mitigations each

Want to work through any of those second-order mitigations in more depth, or sharpen the framing for the review itself?

## Turn 3

**User:**
The cursor context point is the sharpest one there — and you're right that it's where the visible failure happens even when the CRDT is correct. The mitigation I'd propose: cursor context derivation should read the stickiness bit of the *enclosing* mark's right endpoint, not just test whether cursor position is inside the mark's character span. If you're at the boundary and the mark is right-sticky, you're "in" it for toolbar purposes. If it's closed, you're not. That's a one-line rule but it has to be stated explicitly or the editor layer will do something ad hoc.

The boundary constraint on mark creation (never pair two closed endpoints) — I want to make sure I'm not assuming this can be enforced locally. In a concurrent system, two clients could each create a mark with a closed right endpoint and a closed left endpoint that both anchor to the same character, without either knowing about the other. So the constraint can't be enforced at creation time; it has to be resolved at merge time or flagged as a structural invariant violation. That's worth being precise about in the spec.

The review structure you laid out is basically what I had in mind. I'll probably fold the cursor-context mitigation into the third second-order concern rather than leaving it as an open implementation question.

This has been useful. I came in with (a) as my likely answer but without a clean argument structure or a clear account of the second-order concerns. I have that now. The layering framing and the gap-case precision were the two things I hadn't worked out fully.

**Assistant:**
Your point on the boundary constraint is exactly right and worth being precise about in the spec. The right framing: it's a *structural invariant* that the merge algorithm cannot enforce, so it needs to be (1) detectable post-merge (scan for adjacent closed endpoints on the same character), and (2) handled by a stated policy — probably a deterministic tiebreak like "lower Lamport timestamp wins the claim" or "mark type priority" — rather than silently producing a gap. If you leave it as an unresolved invariant violation, someone will hit it in production and not understand why a character came out unformatted.Good luck at the review. The argument is tight: one clear failure mode, two eliminated alternatives in a sentence each, one layered design with three named second-order concerns and one-line mitigations. That's a defensible position.
