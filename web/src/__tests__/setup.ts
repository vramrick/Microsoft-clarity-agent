import "@testing-library/jest-dom/vitest";

import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

// Auto-unmount every rendered component after each test.  Without
// this, hooks from earlier tests remain subscribed to module-level
// stores (e.g., ``useChatDraft``'s drafts map); a later test that
// mutates the store fires those stale subscribers outside an
// ``act()`` boundary, producing noisy "update to TestComponent not
// wrapped in act" warnings.  ``@testing-library/jest`` auto-runs
// cleanup; in vitest it has to be wired here.
afterEach(() => {
  cleanup();
});

// Polyfill crypto.randomUUID for jsdom (used by chatReducer)
if (!globalThis.crypto?.randomUUID) {
  let counter = 0;
  Object.defineProperty(globalThis, "crypto", {
    value: {
      ...globalThis.crypto,
      randomUUID: () => `test-uuid-${++counter}`,
    },
  });
}
