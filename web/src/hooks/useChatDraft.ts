/**
 * Per-session chat-input draft persistence.
 *
 * Thin typed wrapper around :func:`usePanelSlot` for the specific
 * case of a chat panel's draft text.  Kept as its own hook (rather
 * than asking callers to invoke ``usePanelSlot(panelId, "draft", "")``
 * directly) so:
 *
 *   - The slot name ``"draft"`` stays an implementation detail.
 *     Callers don't need to know it, can't typo it, and we can
 *     rename it later without touching the call sites.
 *   - The caller-facing contract is type-safe: the value is
 *     specifically a string, the default is "", and the panel
 *     type is constrained to ``"chat"`` (other panel kinds have
 *     no chat-draft concept).
 *
 * See ``data/panels.ts`` for the store mechanics, PanelId
 * schema, and the rationale for using a discriminated union +
 * sessionStorage backing.  This file is intentionally short.
 */

import { type PanelId, usePanelSlot } from "../data/panels";

/**
 * Identifier for a chat-draft slot.  A chat-type :type:`PanelId`,
 * which encodes both project and session.  Use the broader
 * :type:`PanelId` directly when you want to pass through generic
 * panel-state hooks; this narrower alias is here so the
 * :class:`MessageInput` prop type can say "chat panel" rather
 * than "any panel."
 */
export type DraftPanelId = Extract<PanelId, { type: "chat" }>;

/**
 * Hook: persistent chat-input draft for ``panelId``.  Behaves
 * like ``useState<string>`` for the caller — ``[value, setValue]``
 * — but the value survives mount/unmount and reload.
 *
 * Pass ``null`` while the upstream session identifier isn't yet
 * available (e.g., during the brief window while ``getSession()``
 * is still loading): the hook returns ``["", () => {}]`` and
 * starts persisting once a real ``DraftPanelId`` is supplied.
 */
export function useChatDraft(
  panelId: DraftPanelId | null,
): [string, (next: string) => void] {
  return usePanelSlot<string>(panelId, "draft", "");
}
