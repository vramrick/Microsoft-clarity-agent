import { useCallback, useEffect, useRef } from "react";
import { type DraftKey, useChatDraft } from "../hooks/useChatDraft";

interface MessageInputProps {
  onSend: (text: string) => void;
  disabled?: boolean;
  placeholder?: string;
  /**
   * Identifier that scopes the draft text persisted across
   * mount/unmount.  When non-null, the in-progress message is
   * stored under this key in a session-scoped store; navigating
   * away and back restores it.  When ``null``, the input falls
   * back to ephemeral state (typically because the upstream
   * session id hasn't loaded yet).  See ``useChatDraft`` for the
   * full key design.
   */
  draftKey?: DraftKey | null;
}

export default function MessageInput({
  onSend,
  disabled,
  placeholder,
  draftKey,
}: MessageInputProps) {
  const [value, setValue] = useChatDraft(draftKey ?? null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = useCallback(() => {
    const text = value.trim();
    if (!text || disabled) return;
    onSend(text);
    setValue("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.focus();
    }
  }, [value, disabled, onSend, setValue]);

  const handleKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSubmit();
      }
    },
    [handleSubmit],
  );

  useEffect(() => {
    if (!disabled) {
      textareaRef.current?.focus();
    }
  }, [disabled]);

  const handleInput = useCallback(() => {
    const el = textareaRef.current;
    if (el) {
      el.style.height = "auto";
      el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
    }
  }, []);

  // Auto-resize on programmatic value changes too — when a draft
  // is restored from persistence on mount, or when ``draftKey``
  // changes to a slot that already has stored content, the value
  // updates without firing ``onInput``.  Without this effect the
  // textarea stays at its default single-line height while
  // displaying a multi-line restored draft.
  useEffect(() => {
    handleInput();
  }, [value, handleInput]);

  return (
    <div className="border-t border-border bg-surface/80 backdrop-blur-sm">
      <div className="max-w-3xl mx-auto flex gap-3 items-end p-4">
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          onInput={handleInput}
          disabled={disabled}
          placeholder={placeholder ?? "Type a message... (Enter to send, Shift+Enter for newline)"}
          rows={1}
          className="flex-1 resize-none rounded-xl border border-border-strong bg-surface
            px-4 py-2.5 chat-text text-body leading-relaxed
            placeholder:text-body-faint
            focus:outline-none focus:ring-2 focus:ring-accent/30 focus:border-accent/50
            disabled:bg-disabled-surface disabled:text-disabled-text
            transition-all duration-200"
        />
        <button
          onClick={handleSubmit}
          disabled={disabled || !value.trim()}
          aria-label="Send message"
          className="flex items-center justify-center w-10 h-10 bg-accent text-white rounded-xl
            shadow-md shadow-shadow-accent/10
            hover:bg-accent-hover hover:shadow-lg hover:shadow-shadow-accent/15
            active:scale-[0.98]
            disabled:bg-disabled disabled:shadow-none disabled:cursor-not-allowed
            transition-all duration-200 shrink-0"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
          </svg>
        </button>
      </div>
    </div>
  );
}
