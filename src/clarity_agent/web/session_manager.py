"""
Async bridge between the synchronous ClaritySession and the FastAPI WebSocket.

:class:`WebSessionAdapter` wraps a :class:`ClaritySession` and its backend,
running blocking ``chat()`` calls in a thread-pool executor while forwarding
tool-use events to an :class:`asyncio.Queue` that the WebSocket handler drains.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from functools import partial
from pathlib import Path
from typing import Any

from clarity_agent.app_paths import protocol_dir as _protocol_dir
from clarity_agent.llm import ChatBackend, LLMConfig
from clarity_agent.llm.types import TokenUsage, ToolHandler
from clarity_agent.session import ClaritySession
from clarity_agent.transcript import ChapterStarted
from clarity_agent.web.session_state import (
    clear_session_state,
    load_session_state,
    save_session_state,
)


class WebSessionAdapter:
    """Adapts ClaritySession for asynchronous web use.

    Runs synchronous ``backend.chat()`` in a single-worker thread pool.
    Tool-use events are pushed onto an :pyclass:`asyncio.Queue` so the
    WebSocket handler can stream them to the client in real time.
    """

    def __init__(
        self,
        project_dir: Path,
        clarity_agent_dir: Path,
        llm_config: LLMConfig,
        *,
        llm_session_id: str | None = None,
    ) -> None:
        self.project_dir = project_dir
        self.clarity_agent_dir = clarity_agent_dir
        self.llm_config = llm_config
        self._initial_llm_session_id = llm_session_id
        self.current_process: str | None = None
        self.model_override: str | None = None
        self.active_model: str = llm_config.tiers["default"]
        self.active_tier: str = "default"

        self._executor = ThreadPoolExecutor(max_workers=1)
        self._event_queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        self._backend: ChatBackend | None = None
        self._session: ClaritySession | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._tools: list[dict[str, Any]] | None = None
        self._tool_handler: ToolHandler | None = None
        # Warnings accumulated during a chat turn (written from executor thread,
        # read from the event loop after run_in_executor completes — safe because
        # the single-worker executor serializes all writes before we read).
        self._pending_warnings: list[str] = []
        # Transcript context to inject on the first chat call when no session
        # could be resumed.  Set during start(), consumed on first chat().
        self._transcript_context: str | None = None
        # Set to True when the user clicks Stop.  The drain loop checks this
        # and stops forwarding events; the backend thread finishes on its own.
        self._cancelled = False
        # Partial text accumulated from events before cancellation.
        self._partial_text: list[str] = []
        # Most recent ``input_tokens`` value from the backend's
        # ``on_usage`` callback.  The post-turn compaction check
        # compares this against the model's context window — if the
        # backend isn't compacting internally and this approaches
        # the wall, we fire our own compaction.  Int assignment is
        # atomic in CPython so no lock needed despite the executor-
        # thread writes.
        self._latest_input_tokens: int = 0
        # Set when the backend has signaled it performed its own
        # compaction (e.g., SDK PreCompact + transcript inspection).
        # Drained by the post-turn check, which records the
        # provider's summary in our transcript and rolls our chapter.
        # Phase 2 v1: no backend currently sets this; the
        # threshold-based fallback is what actually triggers
        # compaction.
        self._pending_backend_compaction: Any | None = None

    def _setup_feedback_tools(self) -> None:
        """Set up the feedback tool as baseline for all chat calls."""
        from clarity_agent.ai_actions.feedback import (
            create_feedback_handler,
            create_feedback_tools,
        )

        self._feedback_tools = create_feedback_tools()
        self._feedback_handler = create_feedback_handler(
            self.project_dir,
            provider=self.llm_config.provider,
            model=self.llm_config.tiers.get("default"),
            active_model=self.active_model,
            active_tier=self.active_tier,
            on_tool_use=self._backend.on_tool_use if self._backend else None,
        )
        # Install as baseline tools.
        self._tools = list(self._feedback_tools)
        self._tool_handler = self._feedback_handler

    async def start(self) -> None:
        """Initialize backend and session."""
        self._loop = asyncio.get_running_loop()

        backend = self.llm_config.create_chat_backend(
            project_dir=self.project_dir,
            clarity_agent_dir=self.clarity_agent_dir,
        )
        backend.connect()
        self._backend = backend

        # Restore a previously persisted SDK session ID so the backend
        # resumes the conversation instead of starting fresh.
        session_id = self._initial_llm_session_id or load_session_state(
            self.project_dir,
        )
        if session_id:
            backend.llm_session_id = session_id

        # Snapshot whether the transcript already had any chapters
        # BEFORE ClaritySession's construction appends its header
        # event — that's how we tell "fresh project, nothing to
        # inject" apart from "existing project with prior
        # conversation, rebuild context from it."
        from clarity_agent.transcript import Transcript
        self._project_transcript = Transcript(self.project_dir)
        transcript_was_empty = self._project_transcript.is_empty

        self._session = ClaritySession(
            self.project_dir,
            self.clarity_agent_dir,
            backend,
            self.llm_config,
            transcript=self._project_transcript,
        )
        self._session.__enter__()

        # Bridge backend callbacks to the WebSocket event queue.
        # ClaritySession sets backend.on_tool_call (structured) for
        # transcript persistence; we set on_tool_use (flattened) for
        # the UI's real-time display.  The two callbacks fire in
        # parallel — no chaining needed since they have different
        # signatures and different consumers.
        backend.on_tool_use = self._on_tool_use
        backend.on_text_delta = self._on_text_delta
        backend.on_cost = self._on_cost
        backend.on_usage = self._on_usage
        backend.on_warning = self._on_warning
        backend.on_status = self._on_status
        backend.on_compaction = self._on_backend_compaction

        # Context-restore path: when the SDK has no session to resume
        # AND there's prior conversation in the transcript, synthesize
        # a prior conversation context out of that transcript and prepend
        # it to the system prompt on the first chat call (see :meth:`chat`).
        # When the transcript was empty before this session attached,
        # there's nothing meaningful to inject (the just-written
        # ChapterStarted is just a header), so we skip.
        if not backend.llm_session_id and not transcript_was_empty:
            self._transcript_context = self._project_transcript.context_summary()
        else:
            self._transcript_context = None

        # Install the feedback tool so it's available in all chat calls.
        self._setup_feedback_tools()

    @property
    def llm_session_id(self) -> str | None:
        """Return the backend's SDK session ID, if any."""
        if self._backend is not None:
            return self._backend.llm_session_id
        return self._initial_llm_session_id

    def start_new_chapter(self) -> int:
        """Roll over the conversation thread to a new chapter.

        The current chapter becomes a read-only archive; the backend's
        SDK session is cleared so the next user message starts a
        brand-new conversation with no carried-over context.  The
        previously-loaded context-restore blob (if any) is discarded
        for the same reason — the user has explicitly asked for a
        clean slate.

        Returns the new chapter number.  The new chapter is seeded
        with a :class:`ChapterStarted` event so it's never "empty"
        from the consumer's perspective.

        Idempotent in the sense that calling repeatedly produces
        further new chapters; not idempotent in the sense that each
        call genuinely rolls over (consequence: the UI should gate
        this behind a confirmation dialog).
        """
        backend_name = (
            type(self._backend).__name__ if self._backend is not None else "unknown"
        )
        new_chapter = self._project_transcript.start_new_chapter()
        self._project_transcript.write(ChapterStarted(
            timestamp=datetime.now(timezone.utc),
            project_dir=str(self.project_dir),
            backend=backend_name,
        ))

        # Reset the SDK session so the next turn starts fresh.  Clear
        # the persisted state too — otherwise the next process start
        # would resume the now-archived conversation.
        if self._backend is not None:
            self._backend.llm_session_id = None
        clear_session_state(self.project_dir)

        # Drop any pending context-restore blob the start() path may
        # have loaded — it would inject prior-chapter content into
        # the brand-new chapter's first message, undoing the rollover.
        self._transcript_context = None

        return new_chapter

    def _on_tool_use(self, tool_name: str, detail: str) -> None:
        """Synchronous callback invoked from the executor thread.

        Bridges to the asyncio event loop using ``call_soon_threadsafe``.
        """
        if self._loop is None:
            return
        self._loop.call_soon_threadsafe(
            self._event_queue.put_nowait,
            {"type": "tool_use", "tool": tool_name, "detail": detail},
        )

    def _on_text_delta(self, text: str) -> None:
        """Synchronous callback for streaming text chunks from the executor thread."""
        if self._loop is None or self._cancelled:
            return
        self._loop.call_soon_threadsafe(
            self._event_queue.put_nowait,
            {"type": "text_delta", "content": text},
        )

    def _on_cost(self, cost_usd: float) -> None:
        """Synchronous callback for cost events from the executor thread."""
        if self._loop is None:
            return
        self._loop.call_soon_threadsafe(
            self._event_queue.put_nowait,
            {"type": "cost", "cost_usd": cost_usd},
        )

    def _on_status(self, phase: str) -> None:
        """Synchronous callback for coalesced status updates.

        Ephemeral: the frontend should display the latest phase
        transiently (overwriting the previous one), not append to
        chat history.
        """
        if self._loop is None or self._cancelled:
            return
        self._loop.call_soon_threadsafe(
            self._event_queue.put_nowait,
            {"type": "status", "phase": phase},
        )

    def _on_usage(self, usage: TokenUsage) -> None:
        """Synchronous callback for token usage events from the executor thread.

        Also captures ``input_tokens`` as the running context-size
        signal for the compaction trigger.  The latest value is what
        the model just processed on this turn — if it's approaching
        the window, compaction fires after the turn completes.
        """
        # Capture before the queue dispatch so a post-turn read sees
        # the freshest value.  Int assignment is atomic in CPython.
        self._latest_input_tokens = usage.input_tokens
        if self._loop is None:
            return
        self._loop.call_soon_threadsafe(
            self._event_queue.put_nowait,
            {
                "type": "usage",
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
            },
        )

    def _on_backend_compaction(self, info: Any) -> None:
        """Backend-signaled compaction callback.

        Fires from the executor thread when the backend has performed
        its own context-management compaction.  We stash the info;
        the post-turn check in :meth:`chat` consumes it and rolls
        our chapter — that way the rollover happens on the asyncio
        loop with the rest of the transcript writes serialized
        through the writer's lock.
        """
        self._pending_backend_compaction = info

    # Fraction of the model's context window at which we force
    # compaction even if the provider hasn't signaled it.
    # Deliberately high (85%): when the backend is auto-compacting
    # internally, the live ``input_tokens`` count stays well under
    # this threshold, so we stay cold.  We only fire as the safety
    # net when no compaction is happening anywhere.
    _COMPACTION_THRESHOLD_FRACTION: float = 0.85

    # Fraction of message events to fold into the summary (keep the
    # remaining tail verbatim in the new chapter).  70/30 split
    # preserves recent context — usually what the model needs most
    # — while still shrinking the chapter substantially.
    _COMPACTION_SUMMARIZE_FRACTION: float = 0.70

    async def _maybe_compact_after_turn(self) -> None:
        """Post-turn compaction check.  Thin orchestration around
        :class:`Transcript` and the backend.

        The decision logic (thresholds), the chapter mechanics
        (split/roll/copy-tail), and the summarizer composition all
        live in :class:`Transcript`.  This method's job is the
        session-lifecycle work that the transcript layer
        deliberately doesn't know about: getting the threshold from
        the backend, running the summarizer on the executor thread,
        signaling the UI before and after, and resetting the
        backend's SDK session.

        Priority:
        1. Backend signaled compaction during the turn →
           :meth:`Transcript.external_compaction_occurred` records
           the provider's summary; no LLM call from us.
        2. Threshold-driven path →
           :meth:`Transcript.compact_with_summarizer` calls back
           into our summarizer (the executor-bridge below) iff the
           thresholds are exceeded.

        Called from :meth:`chat` after the response event has been
        emitted so the user sees their answer before any
        compaction-related UI activity.
        """
        if self._backend is None or self._project_transcript is None:
            return

        info = self._pending_backend_compaction
        if info is not None:
            self._pending_backend_compaction = None
            await self._signal_compacting()
            result = self._project_transcript.external_compaction_occurred(
                summary=info.summary,
                source_turn_count=info.source_turn_count,
                summarize_fraction=self._COMPACTION_SUMMARIZE_FRACTION,
            )
            await self._post_compaction_cleanup(result, via_backend=True)
            return

        threshold = int(
            self._COMPACTION_THRESHOLD_FRACTION
            * self._backend.context_window_for(self.active_model),
        )
        # Short-circuit if neither trigger is over — avoids the
        # status-event noise on every turn.  The transcript also
        # checks internally, but emitting the "compacting" phase
        # only to find nothing to do would flicker the UI.
        if not self._project_transcript.should_compact(
            threshold_tokens=threshold,
            input_tokens=self._latest_input_tokens,
        ):
            return

        await self._signal_compacting()
        # The actual summarization LLM call runs on the executor
        # (it's a slow blocking call); ``compact_with_summarizer``
        # invokes our injected ``summarize_fn`` while doing the
        # split + rollover.
        result = await self._loop.run_in_executor(  # type: ignore[union-attr]
            self._executor,
            partial(
                self._project_transcript.compact_with_summarizer,
                threshold_tokens=threshold,
                input_tokens=self._latest_input_tokens,
                summarize_fn=self._summarize_events_sync,
                summarize_fraction=self._COMPACTION_SUMMARIZE_FRACTION,
            ),
        )
        if result is None:
            # Shouldn't happen given the should_compact guard above,
            # but be defensive — the transcript re-checks internally.
            return
        await self._post_compaction_cleanup(result, via_backend=False)

    async def _signal_compacting(self) -> None:
        """Surface the in-progress status to the UI before slow work."""
        await self._event_queue.put({
            "type": "status",
            "phase": "Summarizing earlier conversation",
        })

    async def _post_compaction_cleanup(
        self, result: Any, *, via_backend: bool,
    ) -> None:
        """Session-lifecycle work that runs after the transcript has
        finished its mechanics: backend SDK session reset, token
        counter reset, UI completion signal.
        """
        backend = self._backend
        if backend is not None:
            backend.llm_session_id = None
        clear_session_state(self.project_dir)
        self._latest_input_tokens = 0
        await self._event_queue.put({
            "type": "compaction_complete",
            "via_backend": via_backend,
            "source_chapter": result.source_chapter,
            "source_turn_count": result.source_turn_count,
        })

    def _summarize_events_sync(self, events: list) -> str:
        """Bridge from ``Transcript.compact_with_summarizer`` to the
        backend's chat path.

        Runs on the executor thread.  Suppresses backend streaming
        callbacks for the duration so the summarization call
        doesn't bleed into the user-facing chat stream or write
        transcript events of its own.
        """
        from clarity_agent.transcript._summarize import summarize_chapter
        backend = self._backend
        assert backend is not None
        saved = self._suppress_streaming_callbacks()
        try:
            return summarize_chapter(
                events,
                summarize_fn=lambda prompt: backend.chat(
                    prompt, system_prompt=None, model=None,
                ),
            )
        finally:
            self._restore_streaming_callbacks(saved)

    def _suppress_streaming_callbacks(self) -> dict[str, Any]:
        """Null out streaming + bookkeeping callbacks; return the saved set.

        Paired with :meth:`_restore_streaming_callbacks`.  The summary
        LLM call shouldn't fire UI events or write transcript ToolUse
        records, and shouldn't corrupt the running ``input_tokens``
        counter with summarization usage — so all those callbacks
        are temporarily disconnected.
        """
        backend = self._backend
        assert backend is not None
        saved = {
            "on_text_delta": backend.on_text_delta,
            "on_tool_use": backend.on_tool_use,
            "on_tool_call": backend.on_tool_call,
            "on_status": backend.on_status,
            "on_usage": backend.on_usage,
            "on_cost": backend.on_cost,
            "on_warning": backend.on_warning,
        }
        backend.on_text_delta = None
        backend.on_tool_use = None
        backend.on_tool_call = None
        backend.on_status = None
        backend.on_usage = None
        backend.on_cost = None
        backend.on_warning = None
        return saved

    def _restore_streaming_callbacks(self, saved: dict[str, Any]) -> None:
        """Re-attach the callbacks suppressed by :meth:`_suppress_streaming_callbacks`."""
        backend = self._backend
        if backend is None:
            return
        for name, value in saved.items():
            setattr(backend, name, value)

    def _on_warning(self, message: str) -> None:
        """Synchronous callback for non-fatal backend warnings from the executor thread.

        Appends to ``_pending_warnings`` rather than the event queue directly,
        because the warning fires before ``chat()`` queues the ``response``
        event.  The main loop flushes pending warnings into the queue (before
        the response event) once ``run_in_executor`` completes.
        """
        self._pending_warnings.append(message)

    def _resolve_model(self, process_name: str | None = None) -> str:
        """Resolve the model to use for the next chat call.

        If a manual override is set, use that.  Otherwise resolve from the
        config for the given process.  The returned value may be a tier name
        or model string; the backend's ``resolve_model()`` handles both.
        """
        if self.model_override:
            return self.model_override
        if process_name:
            return self.llm_config.resolve(process_name)
        return self.llm_config.tiers["default"]

    def _update_active_model(
        self, model_override: str | None, process_name: str | None = None,
    ) -> None:
        """Update active_model and active_tier tracking fields."""
        backend = self._backend
        if model_override:
            # Resolve tier names to concrete models for display
            if backend:
                self.active_model = backend.resolve_model(model_override)
            else:
                self.active_model = model_override
            # Determine the tier name
            tiers = self.llm_config.tiers
            self.active_tier = next(
                (k for k, v in tiers.items() if v == model_override),
                model_override if model_override in ("deep", "fast", "default") else "custom",
            )
        elif process_name:
            self.active_tier = self.llm_config.resolve_tier(process_name)
            resolved = self.llm_config.resolve(process_name)
            if backend:
                self.active_model = backend.resolve_model(resolved)
            else:
                self.active_model = resolved
        else:
            self.active_tier = "default"
            self.active_model = self.llm_config.tiers["default"]

    def cancel(self) -> None:
        """Signal that the current turn should be stopped.

        The in-flight backend call continues (we can't interrupt a thread),
        but the drain loop stops forwarding events and a partial response
        is synthesized from whatever text has been received so far.
        """
        self._cancelled = True

    async def chat(self, message: str, system_prompt: str | None = None) -> str:
        """Send a chat message, running the blocking call in a thread."""
        assert self._session is not None
        self._cancelled = False
        self._partial_text.clear()

        # On the first call, inject transcript context if we have it.
        if self._transcript_context is not None:
            ctx = self._transcript_context
            self._transcript_context = None  # consume — only inject once
            # Signal the UI so the user sees why startup takes longer.
            await self._event_queue.put({
                "type": "tool_use",
                "tool": "context_restore",
                "detail": "Re-reading prior session transcripts",
            })
            if system_prompt:
                system_prompt = f"{ctx}\n\n{system_prompt}"
            else:
                system_prompt = ctx

        model = self._resolve_model(self.current_process)
        self._update_active_model(model, self.current_process)

        func = partial(
            self._session.chat, message, system_prompt, model=model,
            tools=self._tools, tool_handler=self._tool_handler,
        )
        response = await self._loop.run_in_executor(  # type: ignore[union-attr]
            self._executor, func,
        )

        # Persist the session ID so the next app launch can resume.
        save_session_state(self.project_dir, self.llm_session_id)

        # Flush any non-fatal warnings accumulated during the turn.  These are
        # queued before the response event so _drain_events() sees them first.
        for warn_msg in self._pending_warnings:
            await self._event_queue.put({"type": "warning", "message": warn_msg})
        self._pending_warnings.clear()

        await self._event_queue.put({"type": "response", "content": response})

        # Check post-turn whether compaction should fire.  Runs after
        # the response event so the user sees the answer first, then
        # the "Summarizing earlier conversation…" status if needed.
        # See :meth:`_maybe_compact_after_turn` for the priority logic.
        await self._maybe_compact_after_turn()

        return response

    async def start_process(self, process_name: str) -> str:
        """Begin a process (loads guide, sends initial message).

        Does NOT enter an interactive loop — the web frontend replaces
        the loop by sending individual ``chat`` messages.
        """
        assert self._session is not None
        self._cancelled = False
        self._partial_text.clear()

        process_content = self._session.load_process(process_name)
        prev_process = self.current_process
        self.current_process = process_name

        # Emit model_changed when switching processes or on first process start
        old_model = self.active_model
        model = self._resolve_model(process_name)
        self._update_active_model(model, process_name)
        if self.active_model != old_model or prev_process is None:
            await self._event_queue.put({
                "type": "model_changed",
                "tier": self.active_tier,
                "model": self.active_model,
                "auto": self.model_override is None,
            })

        # Reset to baseline feedback tools; process-specific tools are
        # merged below.
        self._setup_feedback_tools()
        specialists: list[Any] = []

        # For failure-brainstorming, add tools so the AI can record
        # findings with controlled formatting.
        if process_name == "failure-brainstorming":
            from clarity_agent.ai_actions.brainstorm import (
                create_brainstorm_handler,
                create_brainstorm_tools,
            )
            from clarity_agent.protocol.thinker_registry import select_thinkers

            all_thinkers = select_thinkers(
                self.clarity_agent_dir,
                _protocol_dir(self.project_dir),
                mode="deep",
            )
            specialists = [t for t in all_thinkers if t.name != "general-thinker"]

            brainstorm_tools = create_brainstorm_tools(specialists or None)
            brainstorm_handler = create_brainstorm_handler(
                _protocol_dir(self.project_dir),
                self.clarity_agent_dir,
                on_tool_use=self._backend.on_tool_use if self._backend else None,
            )

            # Merge brainstorm tools with baseline feedback tools.
            assert self._tools is not None  # set by _setup_feedback_tools above
            self._tools.extend(brainstorm_tools)
            feedback_handler = self._feedback_handler

            def _combined_handler(tc: Any) -> str:
                if tc.name == "send_feedback":
                    return feedback_handler(tc)
                return brainstorm_handler(tc)

            self._tool_handler = _combined_handler

        behaviors: str = self._session.load_behaviors()
        behaviors_block: str = f"{behaviors}\n\n" if behaviors else ""

        system_prompt: str = (
            f"{behaviors_block}"
            f"You are running the {process_name} process. "
            f"Here is the process guide:\n\n{process_content}\n\n"
            f"Follow this process step by step.\n\n"
            f"The clarity-agent directory (containing process guides and "
            f"thinker definitions) is: {self.clarity_agent_dir}\n"
            f"Process guides: {self.clarity_agent_dir / 'processes'}/\n"
            f"Thinker guides: {self.clarity_agent_dir / 'thinkers'}/"
        )

        status_report = self._session.get_packet_status_report()
        if status_report:
            system_prompt += (
                f"\n\nThe following packet status analysis was performed by checking "
                f"content hashes against the document dependency graph. Use this "
                f"to inform your assessment:\n\n{status_report}"
            )

        # For failure-brainstorming, append methodology and specialist info.
        if process_name == "failure-brainstorming":
            from clarity_agent.ai_actions.brainstorm import (
                format_available_thinkers as _fmt_thinkers,
            )

            methodology_path = (
                self.clarity_agent_dir / "processes" / "failure-reasoning-guidelines.md"
            )
            if methodology_path.exists():
                system_prompt += (
                    f"\n\n## Failure Reasoning Methodology\n\n"
                    f"{methodology_path.read_text()}"
                )
            if specialists:
                system_prompt += f"\n\n{_fmt_thinkers(specialists)}"

        initial_message: str = f"Let's run the {process_name} process."

        return await self.chat(
            initial_message,
            system_prompt=system_prompt,
        )

    async def get_events(self) -> AsyncIterator[dict[str, Any]]:
        """Async generator yielding events from the queue.

        Yields tool_use events as they arrive, then yields the final
        response event and returns.
        """
        while True:
            event = await self._event_queue.get()
            yield event
            if event.get("type") == "response":
                break

    async def stop(self) -> None:
        """Clean up resources."""
        if self._session is not None:
            self._session.__exit__(None, None, None)
            self._session = None
        if self._backend is not None:
            self._backend.disconnect()
            self._backend = None
        self._executor.shutdown(wait=False)
