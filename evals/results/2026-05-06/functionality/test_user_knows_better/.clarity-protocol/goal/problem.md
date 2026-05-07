# Problem Statement

YATA-based rich-text CRDT with a separate attribute layer for marks. When a mark range and a concurrent local insertion straddle the mark boundary, the YATA ordering resolves correctly, but the insertion ends up attributed to the mark roughly 50% of the time against user intent — depending on which side of the boundary the insertion logically belongs.

Three candidate approaches have been evaluated:
- (a) Explicit attach-left/attach-right bits per mark endpoint (Fuchs-Fuchs style)
- (b) Deriving attachment intent from causal relationships in cursor metadata
- (c) Accepting ambiguity and surfacing UI disambiguation on divergence

Design review is in two days. Need to evaluate spec complexity, runtime cost, and team intelligibility — and determine whether a fourth option is worth considering.

## Decision

Option (a): per-instance attach-left/attach-right bits on mark endpoints, with a type registry providing defaults (bold = right-sticky, links = closed, comments = author-specified). Type registry and per-instance bits are layered, not alternatives.

Options (b) and (c) eliminated: (b) defers the problem to cursor metadata layer without resolving it; (c) gives up on determinism.

## Second-Order Concerns (with mitigations)

**Gap case**: Two concurrent marks with closed endpoints anchored to the same character leave a formatting gap. Cannot be prevented at creation time in a concurrent system. Requires post-merge detection and a stated tiebreak policy (e.g., lower Lamport timestamp wins the boundary claim).

**Span flattener**: Serializer must handle marks with different extents at the same boundary position — A extending past B's closed endpoint. Requires explicit test cases; cannot assume clean nesting.

**Cursor context**: Editor must derive toolbar state from the stickiness bit of the enclosing mark's right endpoint, not just from whether cursor position falls inside the character span. Rule: at a boundary, cursor is "in" the mark iff the mark's endpoint is right-sticky.

## Why This Matters

Concurrent boundary insertions are not edge cases in collaborative rich-text editing — they happen constantly as users type. A ~50% misattribution rate is a user-visible bug that undermines trust in the CRDT's correctness.

## Success Criteria

A chosen approach that is: deterministic (no ambiguity in merge output), implementable within the YATA framework without major protocol changes, intelligible to the team, and defensible at the design review.
