## Turn 1

**User:**
I'm stuck on a mark attribution problem in my rich-text CRDT and I have a design review in two days.

The setup: YATA-style ordering with a separate attribute layer for marks. The failure mode is well-defined — when a mark range and a concurrent local insertion straddle the mark boundary, the merge gives correct ordering but wrong attribution ~50% of the time. The side of the boundary the insert logically belongs to determines the right behavior, but the algorithm doesn't track that intent.

I've narrowed it down to three options: (a) explicit attach-left/attach-right bits on mark endpoints à la Fuchs-Fuchs, (b) derive the attachment intent from causal relationships in the cursor metadata, (c) accept the ambiguity and surface a UI disambiguation step on divergence. I've read Nicolaescu 2016, the Yjs source, the Automerge rich-text RFC. I'm not looking for background — I want to think through the tradeoffs on those three, and whether there's a fourth worth considering.

**Assistant:**
Good — this is exactly what decision-guidance is for. Let me engage with the substance directly.

---

**The core question:** Should attachment intent be *explicit in the data model*, *inferred from causal structure*, or *delegated to the user*?

Here's my read on the three options:

**Option (a) — explicit attach-left/attach-right bits**  
This is the Peritext answer, and the Automerge RFC converged on it for the same reason you're hitting: there's no in-band signal that reliably encodes intent. Explicit bits are boring but correct. Every case is deterministic and auditable. The cost is that the mark creator has to express intent — but that's the right place for it; the editor (or user action that created the mark) does know whether bold should expand or a comment anchor should be sticky. The main friction is if you have existing marks in the wild you'd need to migrate.

**Option (b) — derive from causal/cursor metadata**  
Clever, but I'd push back on this one. The causal graph tells you *sequence*, not *intent*. A cursor sitting just past a mark boundary is a weak proxy for "the user meant to type inside the mark." It breaks silently for programmatic insertions, pastes, import paths, and any operation that didn't originate from a cursor gesture. You'd trade a clean 50% failure rate for a murkier, context-dependent failure rate — which is usually a worse trade because it's harder to reason about, test, and explain at a design review. It also creates a coupling between the cursor layer and the attribution layer that's fragile as the codebase evolves.

**Option (c) — UI disambiguation on divergence**  
Appropriate only if the mark boundary ambiguity is rare and the marks carry high semantic weight (e.g., legal annotations). For structural marks like bold/italic, asking the user to resolve a merge conflict is an experience failure. The frequency you're describing (concurrent boundary straddling at ~50%) makes this unusable as a primary mechanism.

---

**A fourth worth considering: schema-level affinity defaults**

Rather than requiring every mark instance to carry bits, define `expandLeft`/`expandRight` at the *mark type* level in the schema. Bold/italic default expand-both. Comments/links default expand-neither. Programmatic or unusual cases can override per-instance.

This is what ProseMirror's `inclusive` does, and it's not just a convenience — it encodes the semantic difference between *character-level formatting* (which should track the writing gesture) and *span annotations* (which should stay put). Most of your marks likely fall cleanly into one of these two buckets.

This isn't an alternative to (a) — it's a complement. Implement explicit bits per (a), default them from the schema. Now 90%+ of marks are correct without any caller attention, and edge cases are expressible.

---

**My read for your design review:**

Go with **(a) + schema defaults**. The explicit-bits approach is the one reviewers who've read the same literature will recognize as principled. You can defend it clearly: "There's no reliable in-band signal for attachment intent; we encode it at mark creation time, defaulting by type." That's a clean story.

If the API break is the actual concern — can you say more about the migration surface? Existing marks in storage, or an interface contract with editor plugins?

---

Let me save this context while we keep talking.

## Turn 2

**User:**
The schema-level defaults framing is useful — I'd been thinking of it as a UX convenience layer, not as part of the attribution semantics. Treating `expandLeft`/`expandRight` as schema-level defaults with per-instance override changes the API ergonomics substantially. The ProseMirror `inclusive` comparison is the right one; my hesitation was that `inclusive` is a single bit and doesn't distinguish boundary direction, but if we're already going explicit we can do both.

On your migration question: the harder surface is the editor plugin interface, not storage. We have a plugin API that lets teams define custom mark types. Those plugins hand us mark operations with no attachment metadata because historically we didn't have it. So the migration question is really "what's the default behavior for marks created by a plugin that doesn't know about attachment bits yet?" If we default to expand-both, we're wrong for comment/link-type marks. If we default to expand-neither, we're wrong for formatting marks. The schema-level type default solves this cleanly — a plugin that defines a mark type also defines the expansion semantics for that type, and instances inherit unless overridden. That actually makes the migration story better than I'd been modeling it.

One thing I want to pressure-test on (b): you said the causal graph tells you sequence, not intent. I agree for programmatic insertions. But for the specific case of a cursor gesture — where the cursor position at time of insertion IS causally linked to the character before or after the boundary — is there a version of (b) that works, even if only for that subset? Or is the argument that partial correctness is worse than consistent explicit bits because it creates a two-tier system?

**Assistant:**
The partial-correctness question is sharp. Let me work through it directly.

**Does a cursor-gesture version of (b) exist?**

Yes, but it has a load-bearing assumption. For cursor-inference to work, your YATA cursor metadata needs to distinguish "cursor is to the right of C" from "cursor is to the left of D" — where C is the last character of the mark and D is the first character outside it. These are the same logical position, but they're different cursor states. If the representation makes that distinction, the insertion's left-neighbor vs. right-neighbor in YATA tells you which side the user was on, and you can infer attachment.

The problem is that "the same logical position" case is *exactly the boundary case you're trying to fix*. Whether your YATA cursor representation already distinguishes those two states depends on implementation, but if it did, you probably wouldn't have the 50% failure rate in the first place — you'd already be using that signal.

**The two-tier argument is actually stronger than I initially stated:**

The deeper problem with partial-(b) isn't just complexity. It's that your mark's expansion behavior becomes a function of *how content was inserted*, not *what the mark is*. That means:

- A developer using your plugin API cannot predict their mark's behavior. They define a type; the expansion depends on insertion path.  
- `insert(pos, text)` from an undo replay and `insert(pos, text)` from a cursor gesture produce different attribution — from the same operation, at the same position, in the same document state.
- Testing requires you to exercise both paths for every mark type combination.

With (a)+schema defaults, the attribution decision is made once (at mark type definition time), is testable in isolation, and doesn't vary with insertion path. That's a much tighter invariant.

**Here's the sharpest framing:**

If you implement schema defaults as part of (a), causal inference from cursor position becomes a way to *sometimes override the type default with what the user literally did*. That's a marginal correctness improvement on top of an already-correct system, in exchange for significant coupling between the cursor layer and the attribution layer. The type default already handles the common case correctly. The cursor-inference path buys you correctness on a narrow slice — interactive insertions exactly at a boundary where the cursor metadata is unambiguous — while adding a maintenance surface that will outlive the context in which it made sense.

It's not that (b) is never right. It's that partial-(b) layered on top of (a)+schema-defaults doesn't pull its weight.

---

**Where I'd land for the design review:**

The migration insight you just articulated is actually your cleanest argument: plugins define mark types, mark types carry expansion semantics, instances inherit. That's a coherent model with a clear extension point. A plugin that doesn't know about attachment bits yet is just a plugin that hasn't defined its type's schema — and you can give that a sensible default (expand-both for untyped marks, since that's the safer failure mode for formatting and the worst case is a link that expands too far, which is recoverable).

The design review story becomes: "We had a boundary attribution bug. The right fix is to make attachment intent explicit at the type level, which we already needed for plugin ergonomics. Here's the schema change, here's the migration path, here's what plugins need to update."

Want to formalize the options and record the decision now, or keep pressure-testing?

## Turn 3

**User:**
The insertion-path-dependent behavior argument landed. That's the framing I needed — "same operation, same position, same document state, different attribution" is exactly the kind of invariant violation that will cause pain two years from now when someone's debugging a mystery bug and the original cursor-inference rationale is long gone.

One pushback on the untyped default: you said expand-both is the "safer failure mode" for untyped marks because a link that expands too far is recoverable. I'd actually flip that. An annotation or comment that silently captures text it shouldn't is a trust problem, especially if we have any comment or suggestion marks that users treat as definitive. Expand-neither for untyped feels safer to me — if formatting breaks it's immediately visible, if an annotation expands incorrectly it might not be noticed. The recoverable failure mode is "the bold didn't extend," not "the comment claim grew."

But that's a policy call we can make at the schema level, which is exactly the point — you've convinced me the schema-default approach gives us the right place to make it.

I think I have what I need for the review. The decision is (a) + schema-level type defaults, with per-instance override, explicit migration path for existing plugins, and expand-neither as the conservative untyped default. The story is clean and I can defend it against anyone who's read the same literature.

No need to formalize it in your system — I've got it. This was useful.

**Assistant:**
Your flip on the untyped default is right — I was too focused on the formatting case. "Silent annotation expansion" is a trust failure; "bold didn't extend" is a visible nuisance. Expand-neither is the correct conservative default.

Good luck with the review.
