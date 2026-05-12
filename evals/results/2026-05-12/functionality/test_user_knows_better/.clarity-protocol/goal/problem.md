# Problem

A rich-text CRDT (YATA-style ordering, separate attribute layer for marks) has a mark attribution bug at boundaries. When a mark range and a concurrent local insertion straddle the mark boundary, the merge produces correct ordering but wrong attribution ~50% of the time. The side of the boundary the insert logically belongs to determines the right behavior, but the algorithm doesn't track that intent.

## Success Criteria

- Concurrent insertions at mark boundaries are attributed correctly and deterministically
- The approach is principled enough to defend at a design review in two days
- The solution handles all insertion paths (cursor gestures, programmatic, paste, import)

## Context

The owner has already reviewed: Nicolaescu 2016, Yjs source, Automerge rich-text RFC. Three candidate approaches are on the table; the decision is which to adopt (or whether a fourth approach is superior).
