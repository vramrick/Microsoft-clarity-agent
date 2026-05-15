"""
Tests for Claude SDK backend-signaled compaction detection.

Two layers:
* Unit tests for the JSONL summary-extraction helper, with the
  range of message shapes the SDK can produce.
* Backend-level tests that feed synthetic transcript files into
  ``_detect_and_report_compaction`` and verify ``on_compaction``
  fires with the right :class:`CompactionInfo`.

The PreCompact hook itself is exercised at the handler level
(``_on_pre_compact``) since wiring up a real SDK ``query()`` call
would require an LLM session and isn't appropriate for unit tests.
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

import pytest

from clarity_agent.llm.impl.claude_sdk import (
    SdkChatBackend,
    _extract_summary_text,
)
from clarity_agent.llm.types import CompactionInfo


@pytest.fixture
def backend(tmp_path: Path) -> SdkChatBackend:
    """An SdkChatBackend instance for testing.

    Constructs without invoking the underlying SDK (the import
    happens in __init__; if claude_agent_sdk isn't available the
    test is skipped).  Project/clarity dirs point at a tmp path.
    """
    try:
        return SdkChatBackend(project_dir=tmp_path, clarity_agent_dir=tmp_path)
    except ImportError:
        pytest.skip("claude_agent_sdk not installed")


# ---------------------------------------------------------------------------
# _extract_summary_text — message-shape coverage
# ---------------------------------------------------------------------------


class TestExtractSummaryText:
    def test_message_as_plain_string(self):
        entry = {"message": "the summary text"}
        assert _extract_summary_text(entry) == "the summary text"

    def test_message_content_as_string(self):
        entry = {"message": {"role": "user", "content": "the summary text"}}
        assert _extract_summary_text(entry) == "the summary text"

    def test_message_content_as_list_of_text_blocks(self):
        # The Anthropic API content-block shape — the SDK passes
        # these through verbatim into the JSONL.
        entry = {"message": {"content": [
            {"type": "text", "text": "first paragraph"},
            {"type": "text", "text": "second paragraph"},
        ]}}
        assert _extract_summary_text(entry) == "first paragraph\nsecond paragraph"

    def test_message_content_mixed_blocks_skips_non_text(self):
        # Defensive: if a non-text block sneaks in (image block,
        # something exotic), we don't crash — just skip it.
        entry = {"message": {"content": [
            {"type": "text", "text": "useful content"},
            {"type": "image", "source": {"data": "..."}},
            {"type": "text", "text": "more useful content"},
        ]}}
        result = _extract_summary_text(entry)
        assert "useful content" in result
        assert "more useful content" in result
        assert "image" not in result

    def test_empty_message_returns_empty_string(self):
        assert _extract_summary_text({"message": ""}) == ""
        assert _extract_summary_text({"message": None}) == ""
        assert _extract_summary_text({}) == ""

    def test_strips_surrounding_whitespace(self):
        # SDK might pad summaries with newlines; we want the clean text.
        entry = {"message": "\n\n  the summary  \n\n"}
        assert _extract_summary_text(entry) == "the summary"


# ---------------------------------------------------------------------------
# _detect_and_report_compaction — JSONL → on_compaction signal
# ---------------------------------------------------------------------------


def _write_transcript(path: Path, entries: list[dict[str, Any]]) -> None:
    """Write a list of entries as JSONL to the given path.

    Mirrors the SDK's session transcript format: one JSON object
    per line, with the fields the SDK's own parser expects
    (``type``, ``uuid``, ``parentUuid``, ``message``, etc.).
    """
    path.write_text(
        "\n".join(json.dumps(e) for e in entries) + "\n", encoding="utf-8",
    )


class TestDetectAndReportCompaction:
    def test_no_pending_path_is_noop(self, backend, tmp_path):
        # Nothing has signaled compaction → no-op.  Callback never fires.
        fired: list[CompactionInfo] = []
        backend.on_compaction = fired.append
        backend._detect_and_report_compaction()
        assert fired == []

    def test_missing_transcript_file_is_noop(self, backend, tmp_path):
        # Path was set by the hook but the file doesn't exist
        # (shouldn't happen in normal flow, but be defensive).
        backend._pending_compact_transcript_path = tmp_path / "missing.jsonl"
        fired: list[CompactionInfo] = []
        backend.on_compaction = fired.append
        backend._detect_and_report_compaction()
        assert fired == []

    def test_fires_on_compact_summary_entry(self, backend, tmp_path):
        # The base case: one isCompactSummary entry → one
        # on_compaction call carrying that summary.
        path = tmp_path / "session.jsonl"
        _write_transcript(path, [
            {"type": "user", "uuid": "u1", "message": {"content": "hello"}},
            {
                "type": "user",
                "uuid": "compact-1",
                "isCompactSummary": True,
                "message": {"content": "summary of earlier conversation"},
            },
        ])
        backend._pending_compact_transcript_path = path
        fired: list[CompactionInfo] = []
        backend.on_compaction = fired.append

        backend._detect_and_report_compaction()

        assert len(fired) == 1
        assert fired[0].summary == "summary of earlier conversation"
        # source_turn_count defaults to None — Transcript will derive
        # it from the 70/30 split.
        assert fired[0].source_turn_count is None

    def test_already_seen_uuids_arent_fired_again(self, backend, tmp_path):
        # Idempotence: if _detect runs twice (e.g., the user does
        # several queries before the orchestrator drains the pending
        # info), the same isCompactSummary entry isn't fired
        # repeatedly.
        path = tmp_path / "session.jsonl"
        _write_transcript(path, [
            {
                "type": "user",
                "uuid": "compact-1",
                "isCompactSummary": True,
                "message": {"content": "summary"},
            },
        ])
        backend._pending_compact_transcript_path = path
        fired: list[CompactionInfo] = []
        backend.on_compaction = fired.append

        backend._detect_and_report_compaction()
        # Re-set the pending path (simulating a second PreCompact)
        # and run again — but the same uuid is in seen.
        backend._pending_compact_transcript_path = path
        backend._detect_and_report_compaction()

        assert len(fired) == 1  # only fired the first time

    def test_multiple_new_summaries_each_fire(self, backend, tmp_path):
        # If the SDK has compacted multiple times since we last
        # looked, each new isCompactSummary fires its own
        # on_compaction event.
        path = tmp_path / "session.jsonl"
        _write_transcript(path, [
            {
                "type": "user",
                "uuid": "compact-1",
                "isCompactSummary": True,
                "message": {"content": "first summary"},
            },
            {"type": "assistant", "uuid": "a1", "message": {"content": "..."}},
            {
                "type": "user",
                "uuid": "compact-2",
                "isCompactSummary": True,
                "message": {"content": "second summary"},
            },
        ])
        backend._pending_compact_transcript_path = path
        fired: list[CompactionInfo] = []
        backend.on_compaction = fired.append

        backend._detect_and_report_compaction()

        assert len(fired) == 2
        assert fired[0].summary == "first summary"
        assert fired[1].summary == "second summary"

    def test_non_compact_entries_ignored(self, backend, tmp_path):
        # Regular user/assistant entries shouldn't fire anything.
        path = tmp_path / "session.jsonl"
        _write_transcript(path, [
            {"type": "user", "uuid": "u1", "message": {"content": "hello"}},
            {"type": "assistant", "uuid": "a1", "message": {"content": "hi"}},
            {"type": "user", "uuid": "u2", "message": {"content": "bye"}},
        ])
        backend._pending_compact_transcript_path = path
        fired: list[CompactionInfo] = []
        backend.on_compaction = fired.append

        backend._detect_and_report_compaction()

        assert fired == []

    def test_malformed_lines_skipped(self, backend, tmp_path):
        # Bad JSON lines in the transcript (shouldn't happen but
        # let's be defensive) don't abort the read.
        path = tmp_path / "session.jsonl"
        good_entry = {
            "type": "user",
            "uuid": "compact-1",
            "isCompactSummary": True,
            "message": {"content": "the summary"},
        }
        path.write_text(
            "{this is not valid json\n"
            + json.dumps(good_entry) + "\n",
            encoding="utf-8",
        )
        backend._pending_compact_transcript_path = path
        fired: list[CompactionInfo] = []
        backend.on_compaction = fired.append

        backend._detect_and_report_compaction()

        assert len(fired) == 1
        assert fired[0].summary == "the summary"

    def test_no_callback_registered_is_safe(self, backend, tmp_path):
        # If nobody's listening, we just skip silently — no crash.
        path = tmp_path / "session.jsonl"
        _write_transcript(path, [
            {
                "type": "user", "uuid": "compact-1",
                "isCompactSummary": True,
                "message": {"content": "summary"},
            },
        ])
        backend._pending_compact_transcript_path = path
        backend.on_compaction = None
        # No assertion needed — should just not raise.
        backend._detect_and_report_compaction()


# ---------------------------------------------------------------------------
# PreCompact hook handler
# ---------------------------------------------------------------------------


class TestPreCompactHandler:
    """The handler the SDK calls when it's about to compact a session.

    We don't drive the real SDK here — just call the handler with
    the input shapes it would receive.  The handler's job is small:
    capture transcript_path on a PreCompact event, no-op everything
    else, always return an empty dict so the SDK proceeds.
    """

    def test_captures_transcript_path_on_precompact(self, backend, tmp_path):
        transcript_path = tmp_path / "session.jsonl"
        result = asyncio.run(backend._on_pre_compact(
            {
                "hook_event_name": "PreCompact",
                "transcript_path": str(transcript_path),
                "session_id": "test-session",
                "cwd": str(tmp_path),
                "trigger": "auto",
                "custom_instructions": None,
            },
            None,
            {"signal": None},
        ))
        assert backend._pending_compact_transcript_path == transcript_path
        # Empty output → SDK proceeds normally.
        assert result == {}

    def test_ignores_non_precompact_events(self, backend, tmp_path):
        # The SDK might call our handler for hooks other than
        # PreCompact if we accidentally register it more broadly.
        # Defensive: only act on PreCompact.
        backend._pending_compact_transcript_path = None
        result = asyncio.run(backend._on_pre_compact(
            {
                "hook_event_name": "PostToolUse",
                "transcript_path": str(tmp_path / "session.jsonl"),
                "session_id": "test-session",
                "cwd": str(tmp_path),
                "tool_name": "Read",
                "tool_input": {},
                "tool_response": None,
                "tool_use_id": "tool-1",
            },
            None,
            {"signal": None},
        ))
        assert backend._pending_compact_transcript_path is None
        assert result == {}

    def test_missing_transcript_path_doesnt_explode(self, backend):
        # If the input is malformed (no transcript_path), we
        # gracefully no-op rather than crashing the SDK's hook
        # dispatch.
        result = asyncio.run(backend._on_pre_compact(
            {"hook_event_name": "PreCompact"},
            None,
            {"signal": None},
        ))
        assert backend._pending_compact_transcript_path is None
        assert result == {}
