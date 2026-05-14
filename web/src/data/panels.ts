/**
 * Panel identity and per-panel ephemeral state.
 *
 * "Panel" here means a routable view in the app — chat, history,
 * protocol viewer, packet, packet-status, etc.  Each panel has:
 *
 *   - An identity (:class:`PanelId`), encoding which project and
 *     which kind of panel and any disambiguating params (the
 *     chat session id, the doc path being viewed).
 *   - Ephemeral state slots (draft text, scroll position,
 *     selection, search query) that survive mount/unmount so
 *     navigating away and back doesn't drop the user's
 *     half-finished work.
 *
 * The store underneath is a simple module-level Map keyed by
 * ``(serializedPanelId, slot)`` with a sessionStorage backing.
 * It's small enough that introducing a state library
 * (zustand/jotai/...) doesn't pay back its dependency cost yet.
 * When we grow to many slots or need cross-slot atomic updates,
 * the public API exposed here (``usePanelSlot``, ``getSlot``,
 * ``setSlot``) is small enough to swap underneath without
 * touching callers.
 *
 * Why a discriminated union for ``PanelId`` instead of a generic
 * params bag:
 *   - Type safety per panel type: a "chat" panel always has a
 *     ``sessionId``; a "protocol" panel may have an optional
 *     ``docPath``.  The discriminated union encodes that at the
 *     TypeScript level so a caller can't construct a chat panel
 *     id without a session, and switch statements get exhaustive
 *     checking for free.
 *   - Maps cleanly to the existing react-router routes (one
 *     ``PanelType`` per top-level route), which step 3
 *     ("open in new window") will need to convert PanelIds to
 *     and from URLs.
 *
 * Serialization (used as Map keys, sessionStorage keys, and
 * cross-window drag payloads later) is a flat string of the form
 * ``"{projectId}|{type}[:{disambiguator}]"`` — readable in dev
 * tools, stable across runs.  See ``serializePanelId``.
 *
 * SessionStorage scope notes (unchanged from the drafts iteration):
 *   - sessionStorage is per-window in Tauri webviews.  State
 *     follows the panel within a window across mount/unmount and
 *     reload; it does NOT follow a panel popped out into a new
 *     window.  Cross-window persistence will require a
 *     per-project state file under ``.clarity-protocol/``
 *     (or Tauri app data dir) and is deferred to a later step.
 */

import { useSyncExternalStore } from "react";

/**
 * The set of top-level panel kinds — one per route in
 * :file:`App.tsx`.  Add a new value here when adding a new route;
 * the discriminated union below will then force the call sites to
 * decide what disambiguating params (if any) the new panel needs.
 */
export type PanelType =
  | "chat"
  | "history"
  | "protocol"
  | "packet"
  | "packet-status";

/**
 * The identity of a panel: project + kind + any disambiguating
 * params.  Discriminated by ``type`` so each kind carries exactly
 * the params it needs.
 *
 * - ``chat`` requires ``sessionId`` — different sessions under
 *   the same project are different panels for state purposes
 *   (each has its own draft).
 * - ``protocol`` has an optional ``docPath`` — once we wire up
 *   per-document viewers, the same protocol route hosting two
 *   different docs is two different panels.  Until then, omitting
 *   it means "the protocol tree view, root."
 * - The other panel types have no disambiguator yet; their
 *   identity is fully determined by ``{projectId, type}``.
 *
 * ``projectId`` should be a stable, canonical identifier for the
 * project — typically the absolute resolved path provided by the
 * backend on ``SessionInfo.project_id`` or, as a fallback,
 * ``project_dir``.
 */
export type PanelId =
  | { projectId: string; type: "chat"; sessionId: string }
  | { projectId: string; type: "history" }
  | { projectId: string; type: "protocol"; docPath?: string }
  | { projectId: string; type: "packet" }
  | { projectId: string; type: "packet-status" };

/**
 * Serialized form of a :type:`PanelId` — used as the key for
 * sessionStorage entries, internal Map lookups, and (later)
 * Tauri drag payloads.
 *
 * Format: ``"{projectId}|{type}"`` for unparam'd panels,
 * ``"{projectId}|{type}:{disambiguator}"`` when a disambiguator
 * is present.  Stable across runs, readable in dev tools.
 */
export function serializePanelId(id: PanelId): string {
  switch (id.type) {
    case "chat":
      return `${id.projectId}|chat:${id.sessionId}`;
    case "protocol":
      return id.docPath
        ? `${id.projectId}|protocol:${id.docPath}`
        : `${id.projectId}|protocol`;
    case "history":
    case "packet":
    case "packet-status":
      return `${id.projectId}|${id.type}`;
  }
}

// ---------------------------------------------------------------------------
// Module-level state store
//
// One Map keyed by ``(serializedPanelId, slot)``, mirrored into
// sessionStorage with a ``panel:`` namespace so it shares the
// storage area without colliding with other features.  Values are
// JSON-encoded uniformly — including strings — so the store can
// hold any JSON-serializable type without per-type branches in
// the read/write paths.
// ---------------------------------------------------------------------------

const _SESSION_STORAGE_PREFIX = "panel:";

const slots = new Map<string, unknown>();
const listeners = new Map<string, Set<() => void>>();

function slotKey(serializedPanelId: string, slot: string): string {
  return `${serializedPanelId}@${slot}`;
}

// Hydrate from sessionStorage at module load.  Runs once per
// window lifetime.  Wrapped in try/catch so a busted
// sessionStorage (private-browsing mode quirks, quota errors,
// JSON-decode failures on individual entries) doesn't take the
// whole UI down with it.
try {
  for (let i = 0; i < sessionStorage.length; i++) {
    const k = sessionStorage.key(i);
    if (k && k.startsWith(_SESSION_STORAGE_PREFIX)) {
      const raw = sessionStorage.getItem(k);
      if (raw === null) continue;
      try {
        slots.set(k.slice(_SESSION_STORAGE_PREFIX.length), JSON.parse(raw));
      } catch {
        // Skip individual bad entries — corrupted JSON from a
        // previous version of the store, manual editing, etc.
        // Better than refusing to start.
      }
    }
  }
} catch {
  // sessionStorage entirely unavailable.  In-memory state still
  // works for the current window; reload won't survive.
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

/**
 * Read a panel slot.  Returns ``defaultValue`` when no value has
 * been stored for ``(panelId, slot)`` yet.  Non-reactive — pair
 * with :func:`subscribeSlot` for live updates, or use
 * :func:`usePanelSlot` for the React-hook shape.
 */
export function getSlot<T>(
  panelId: PanelId,
  slot: string,
  defaultValue: T,
): T {
  const k = slotKey(serializePanelId(panelId), slot);
  return slots.has(k) ? (slots.get(k) as T) : defaultValue;
}

/**
 * Write a panel slot.  Triggers any active subscribers and writes
 * the value into sessionStorage (JSON-encoded) so reload survives.
 * A write of a value equal-by-reference to the current value is a
 * no-op — avoids subscriber churn for redundant writes.
 */
export function setSlot<T>(
  panelId: PanelId,
  slot: string,
  value: T,
): void {
  const k = slotKey(serializePanelId(panelId), slot);
  if (slots.get(k) === value) return;
  slots.set(k, value);
  try {
    sessionStorage.setItem(
      _SESSION_STORAGE_PREFIX + k,
      JSON.stringify(value),
    );
  } catch {
    // Quota exceeded or storage unavailable.  In-memory state is
    // still consistent for the current session; only the
    // reload-survives property is lost.  Not user-visible.
  }
  notify(k);
}

/**
 * Subscribe to changes on a panel slot.  Returns an unsubscribe
 * function.  Mostly an implementation primitive for the React
 * hook below; exposed in case non-React code wants to react to
 * state changes (e.g., publishing to a Tauri event later).
 */
export function subscribeSlot(
  panelId: PanelId,
  slot: string,
  fn: () => void,
): () => void {
  return subscribe(slotKey(serializePanelId(panelId), slot), fn);
}

/**
 * React hook: reactive read/write of a panel slot.  ``[value,
 * setValue]`` shape identical to ``useState``, but the value
 * persists across mount/unmount and across window reloads.
 *
 * ``panelId === null`` disables persistence and returns
 * ``[defaultValue, () => {}]``.  Pass null when the upstream
 * identifier isn't yet available (e.g., during the brief window
 * while ``SessionInfo`` is loading) — the hook will start
 * persisting as soon as a real ``PanelId`` is supplied.
 */
export function usePanelSlot<T>(
  panelId: PanelId | null,
  slot: string,
  defaultValue: T,
): [T, (next: T) => void] {
  const serialized = panelId === null ? null : serializePanelId(panelId);
  const key = serialized === null ? null : slotKey(serialized, slot);

  const value = useSyncExternalStore(
    (cb) => {
      if (key === null) return () => {};
      return subscribe(key, cb);
    },
    () => {
      if (key === null) return defaultValue;
      return slots.has(key) ? (slots.get(key) as T) : defaultValue;
    },
  );

  const setValue = (next: T): void => {
    if (panelId === null) return;
    setSlot(panelId, slot, next);
  };

  return [value, setValue];
}

/**
 * Test-only: clear all panel state from both in-memory store and
 * sessionStorage.  Intentionally does NOT notify subscribers —
 * vitest's afterEach ordering can leave hooks still subscribed
 * when this runs, and firing notifications against them would
 * trigger React state updates outside the test's ``act()``
 * boundary (noisy warnings, occasionally flaky assertions).
 * Tests that need post-reset live updates should remount their
 * hooks explicitly via ``renderHook`` after calling this.
 * NOT for production callers.
 */
export function __resetPanelsForTest(): void {
  for (const k of slots.keys()) {
    try {
      sessionStorage.removeItem(_SESSION_STORAGE_PREFIX + k);
    } catch {
      // ignore
    }
  }
  slots.clear();
}
