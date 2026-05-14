/**
 * Per-session draft persistence for the chat input.
 *
 * The chat input's draft text used to live in component-local
 * ``useState`` inside ``MessageInput``.  That meant: any time the
 * component unmounted — navigating to documents, swapping panels,
 * a route change — the half-typed message went away.  Users
 * reading a document while drafting a related question would lose
 * their thought.
 *
 * This hook lifts the draft into a module-scoped store keyed by
 * a stable ``DraftKey``, with a sessionStorage backing so a reload
 * survives too.  Behaves identically to ``useState`` from the
 * caller's perspective — ``const [value, setValue] = useChatDraft(key)``.
 *
 * Key design:
 *   - The key encodes BOTH project and session, so opening the
 *     same session id under a different project doesn't collide,
 *     AND the same project's chat doesn't leak between sessions.
 *     Multi-project support (not yet built) will not require any
 *     migration here — the key already carries the project.
 *   - ``null`` is a valid argument (e.g., while ``SessionInfo`` is
 *     still loading from ``getSession()``).  In that mode the
 *     hook falls back to ephemeral component-local state — no
 *     persistence, no cross-mount survival.  This matches the
 *     pre-fix behavior during the brief loading window and avoids
 *     a flicker where the input would refuse to render until the
 *     session id resolves.
 *
 * Why ``useSyncExternalStore`` + a module-level ``Map`` instead of
 * a state library:
 *   - Smallest possible surface for the first iteration — no new
 *     dependency, ~50 lines of code, easy to reason about.
 *   - When the broader panel-state store (panel registry, scroll
 *     position, selection) lands, we can either grow this pattern
 *     or migrate to a real state library at that time — either
 *     way, the callers' API (``useChatDraft``) doesn't change.
 *
 * SessionStorage scope:
 *   - sessionStorage is per-tab/per-window in browsers and per-
 *     window in Tauri webviews.  Drafts persist across reload and
 *     navigation within the same window; they do NOT follow a
 *     panel across pop-out-to-new-window.  That tradeoff is fine
 *     for the first iteration and is explicitly the scope we
 *     agreed on.  Cross-window draft survival comes later, via
 *     a per-project state file under the project's
 *     ``.clarity-protocol/`` (or Tauri app data dir).
 */

import { useSyncExternalStore } from "react";

/**
 * Identifier for a chat-draft slot.  Encodes BOTH project and
 * session because the panel-state schema we're building toward
 * is keyed by ``{projectId, type, params}`` — drafts are a
 * per-session ephemeral state under a particular project.
 *
 * ``projectId`` should be a stable, canonical identifier for the
 * project (typically the absolute resolved path).  ``sessionId``
 * is the per-session identifier from ``SessionInfo.session_id``.
 */
export interface DraftKey {
  projectId: string;
  sessionId: string;
}

/** Internal serialization used for both Map keys and sessionStorage keys. */
function serializeKey(key: DraftKey): string {
  return `chatDraft:${key.projectId}|${key.sessionId}`;
}

// Module-level state.  Lives across mount/unmount because it's
// bound to the module, not to any component.  Hot-module-reload
// in dev will reset this — fine, dev quirk.
const drafts = new Map<string, string>();
const listeners = new Map<string, Set<() => void>>();

// Hydrate from sessionStorage at module load.  Runs once per
// window lifetime.  Wrapped in try/catch so a busted sessionStorage
// (private-browsing mode quirks, quota errors, etc.) doesn't take
// the chat panel down with it.
try {
  for (let i = 0; i < sessionStorage.length; i++) {
    const k = sessionStorage.key(i);
    if (k && k.startsWith("chatDraft:")) {
      drafts.set(k, sessionStorage.getItem(k) ?? "");
    }
  }
} catch {
  // sessionStorage unavailable; drafts will be in-memory only
  // for this session.  Not worth surfacing — the user gets the
  // pre-fix experience (lose-on-mount).
}

function notify(key: string): void {
  listeners.get(key)?.forEach((fn) => fn());
}

function subscribe(key: string, fn: () => void): () => void {
  let set = listeners.get(key);
  if (!set) {
    set = new Set();
    listeners.set(key, set);
  }
  set.add(fn);
  return () => {
    const s = listeners.get(key);
    if (s) {
      s.delete(fn);
      if (s.size === 0) listeners.delete(key);
    }
  };
}

function getSnapshot(key: string): string {
  return drafts.get(key) ?? "";
}

function setDraft(key: string, value: string): void {
  if (drafts.get(key) === value) return;  // no-op, avoids re-render churn
  drafts.set(key, value);
  try {
    sessionStorage.setItem(key, value);
  } catch {
    // Quota exceeded or storage unavailable.  In-memory state is
    // still consistent so the current session works; only the
    // reload-survives property is lost.  Not user-visible.
  }
  notify(key);
}

/**
 * Test-only: clear all drafts from both in-memory store and
 * sessionStorage.  Exported so unit tests can isolate runs without
 * leaking state between tests.  NOT for production callers.
 */
export function __resetDraftsForTest(): void {
  for (const key of drafts.keys()) {
    try {
      sessionStorage.removeItem(key);
    } catch {
      // ignore
    }
  }
  drafts.clear();
  // Notify any active subscribers so they re-render to the empty
  // state.  Iterate via a snapshot because notify can mutate
  // listeners when subscribers cleanup.
  for (const key of Array.from(listeners.keys())) {
    notify(key);
  }
}

/**
 * Hook: persistent chat-input draft for ``key``.
 *
 * ``key === null`` disables persistence (the hook falls back to
 * ephemeral component-local state via the empty-string snapshot).
 * Pass null when the upstream session identifier isn't yet
 * available — the hook will start persisting as soon as a real
 * key is provided.
 */
export function useChatDraft(
  key: DraftKey | null,
): [string, (next: string) => void] {
  const serialized = key === null ? null : serializeKey(key);

  // ``useSyncExternalStore`` requires stable subscribe/getSnapshot
  // closures for the lifetime of a given subscription.  The
  // ``serialized`` value is what changes, so we close over it; React
  // re-subscribes whenever it changes (correct behavior — a different
  // draft slot needs different subscribers).  When ``serialized`` is
  // null, both functions degenerate to no-ops returning "".
  const value = useSyncExternalStore(
    (cb) => {
      if (serialized === null) return () => {};
      return subscribe(serialized, cb);
    },
    () => (serialized === null ? "" : getSnapshot(serialized)),
  );

  const setValue = (next: string): void => {
    if (serialized === null) return;
    setDraft(serialized, next);
  };

  return [value, setValue];
}
