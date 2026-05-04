"""Tests for the framework-enforced smoke check.

The smoke check is a judge call that runs after every conversation
(fresh or resumed) and before any test-authored assertion.  It asks
"did the conversation actually exercise the persona's stated goal?"
A negative answer raises :class:`SmokeCheckFailedError` from the
fixture, which the conftest routes to a dedicated ``smoke_failed``
outcome bucket — every test in the module reports as smoke_failed
rather than running against a bad sample.

Surfaces under test:

- :class:`SmokeCheckFailedError` — stores the judge's reasoning so
  the summary can surface it.
- :func:`_goal_pursued_claim_for` — framework-standard claim text; includes
  the goal so changes to the goal invalidate cached smoke records.
- :meth:`Judge.goal_pursued_check` — YES/NO/NA handling, cache behavior, and
  the deliberate choice NOT to route smoke results through the main
  recorder (they belong in a distinct part of the summary).
- :func:`evals.framework.report` — 🛑 icon mapping, smoke_failed
  counting in the top summary and module aggregate, the per-module
  "Goal-pursued check failed" banner with the judge's reasoning.
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from evals.framework import SmokeCheckFailedError
from evals.framework.config import EvalConfig, RoleConfig
from evals.framework.judge import (
    _MIN_SUBSTANTIVE_TURNS,
    _SUBSTANTIVITY_CACHE_KEY,
    Judge,
    JudgeRecord,
    _goal_pursued_claim_for,
    _make_substantivity_record,
    _persona_adoption_claim_for,
    _substantivity_check,
    _substantivity_claim_for,
)
from evals.framework.report import (
    _first_smoke_reasoning,
    _format_issue_link_long,
    _format_issue_link_short,
    _load_smoke_gate_records,
    _module_aggregate,
    _smoke_anchor,
    write_summary,
)
from evals.framework.resume import JudgeCache

_SMOKE_ICON = "\U0001F6D1"  # 🛑


# ---------------------------------------------------------------------------
# SmokeCheckFailedError
# ---------------------------------------------------------------------------

def test_smoke_error_is_assertionerror_subclass() -> None:
    """Subclassing AssertionError keeps pytest classifying it as a test
    failure rather than an unexpected crash — the conftest then
    further classifies it into the smoke_failed bucket."""
    err = SmokeCheckFailedError("boom")
    assert isinstance(err, AssertionError)


def test_smoke_error_stores_reasoning() -> None:
    err = SmokeCheckFailedError("boom", reasoning="user drifted off-topic")
    assert err.reasoning == "user drifted off-topic"
    assert "boom" in str(err)


def test_smoke_error_default_reasoning_empty() -> None:
    err = SmokeCheckFailedError("boom")
    assert err.reasoning == ""


# ---------------------------------------------------------------------------
# _goal_pursued_claim_for
# ---------------------------------------------------------------------------

def test_smoke_claim_includes_goal() -> None:
    goal = "Find a reasonable first handgun for target shooting."
    claim = _goal_pursued_claim_for(goal)
    assert goal in claim
    # Mentions the core expectations the smoke prompt checks:
    # that the user engaged with the stated goal and didn't drift.
    assert "goal" in claim.lower()
    assert "drift" in claim.lower()


def test_smoke_claim_strips_surrounding_whitespace_in_goal() -> None:
    """Goals are typically triple-quoted and lead/trail with whitespace."""
    claim = _goal_pursued_claim_for("\n\n  pick a handgun\n\n")
    assert "pick a handgun" in claim
    # The goal is inlined stripped, not verbatim with leading blanks.
    assert "\n\n  pick a handgun" not in claim


def test_smoke_claim_is_stable() -> None:
    """Same input → identical claim, so the cache key is deterministic."""
    goal = "explore AI product options"
    assert _goal_pursued_claim_for(goal) == _goal_pursued_claim_for(goal)


# ---------------------------------------------------------------------------
# Judge.goal_pursued_check
# ---------------------------------------------------------------------------

def _make_judge(tmp_path: Path) -> Judge:
    eval_config = EvalConfig(
        roles={"judge": RoleConfig(
            provider="openai", model="m", auth_mode="api_key",
        )},
    )
    return Judge(
        eval_config,
        project_dir=tmp_path,
        clarity_agent_dir=tmp_path,
        current_test_getter=lambda: "tests/test_x.py::t",
    )


def test_goal_pursued_check_yes_returns_pass_with_reasoning(tmp_path: Path) -> None:
    judge = _make_judge(tmp_path)
    with patch.object(
        Judge, "_run",
        return_value=("VERDICT: YES\nREASONING: goal was explored", 0.0),
    ):
        passed, reasoning = judge.goal_pursued_check("content", goal="do the thing")
    assert passed is True
    assert "goal was explored" in reasoning


def test_goal_pursued_check_no_returns_fail_with_reasoning(tmp_path: Path) -> None:
    judge = _make_judge(tmp_path)
    with patch.object(
        Judge, "_run",
        return_value=(
            "VERDICT: NO\nREASONING: the user drifted to a different topic",
            0.0,
        ),
    ):
        passed, reasoning = judge.goal_pursued_check("content", goal="do the thing")
    assert passed is False
    assert "drifted" in reasoning


def test_goal_pursued_check_na_counts_as_pass(tmp_path: Path) -> None:
    """NA means 'doesn't apply' — not a reason to fail the module."""
    judge = _make_judge(tmp_path)
    with patch.object(
        Judge, "_run",
        return_value=("VERDICT: N/A\nREASONING: goal-coverage isn't checkable here", 0.0),
    ):
        passed, _ = judge.goal_pursued_check("content", goal="ambiguous goal")
    assert passed is True


def test_goal_pursued_check_caches_under_reserved_name(tmp_path: Path) -> None:
    """Smoke records key under '__goal_pursued__' so they don't collide with real tests."""
    cache_path = tmp_path / "judge_records.json"
    cache = JudgeCache(path=cache_path, fingerprint="fp")

    judge = _make_judge(tmp_path)
    judge.set_cache(cache)

    with patch.object(
        Judge, "_run",
        return_value=("VERDICT: YES\nREASONING: looks good", 0.0),
    ):
        judge.goal_pursued_check("content", goal="do the thing")

    data = json.loads(cache_path.read_text(encoding="utf-8"))
    # Stored under the reserved name, not under any user test name.
    assert "__goal_pursued__" in data["tests"]
    assert len(data["tests"]["__goal_pursued__"]) == 1
    # Claim stored is the framework-standard smoke claim.
    stored_claim = data["tests"]["__goal_pursued__"][0]["claim"]
    assert "do the thing" in stored_claim


def test_goal_pursued_check_cache_hit_bypasses_llm(tmp_path: Path) -> None:
    """Re-running smoke against the same transcript+goal should be free."""
    cache_path = tmp_path / "judge_records.json"
    goal = "do the thing"
    claim = _goal_pursued_claim_for(goal)
    # Seed the cache with a stored smoke verdict.
    JudgeCache(path=cache_path, fingerprint="fp").store(
        "__goal_pursued__",
        JudgeRecord(
            claim=claim, verdict="YES", reasoning="cached ok",
            elapsed=2.0, cost_usd=0.01,
        ),
    )

    judge = _make_judge(tmp_path)
    judge.set_cache(JudgeCache(path=cache_path, fingerprint="fp"))

    # If the LLM were invoked this would raise via the side_effect.
    with patch.object(Judge, "_run", side_effect=AssertionError("LLM called")):
        passed, reasoning = judge.goal_pursued_check("content", goal=goal)

    assert passed is True
    assert reasoning == "cached ok"


def test_goal_pursued_check_does_not_invoke_recorder(tmp_path: Path) -> None:
    """Smoke results belong in their own summary section, not in the
    per-test criterion lists the recorder populates.
    """
    judge = _make_judge(tmp_path)
    recorded: list[JudgeRecord] = []
    judge._recorder = recorded.append

    with patch.object(
        Judge, "_run",
        return_value=("VERDICT: YES\nREASONING: ok", 0.0),
    ):
        judge.goal_pursued_check("content", goal="do the thing")

    assert recorded == [], (
        "goal_pursued_check must NOT route through the recorder — "
        "smoke records belong in a distinct summary section"
    )


# ---------------------------------------------------------------------------
# _persona_adoption_claim_for
# ---------------------------------------------------------------------------

def test_persona_claim_includes_persona_text() -> None:
    """The persona text is inlined so the claim is self-contained."""
    persona = "Marcus, 29, community organizer"
    claim = _persona_adoption_claim_for(persona, situation="", goal="")
    assert persona in claim
    # The claim names persona-substitution as the failure to catch.
    assert "persona" in claim.lower()
    assert "substituting" in claim.lower()


def test_persona_claim_omits_situation_block_when_empty() -> None:
    """No situation → no empty situation header in the claim."""
    claim = _persona_adoption_claim_for(
        "a persona", situation="   ", goal="",
    )
    assert "Their situation" not in claim
    # Persona is still present.
    assert "a persona" in claim


def test_persona_claim_includes_situation_when_given() -> None:
    claim = _persona_adoption_claim_for(
        "a persona",
        situation="Recently separated, lives alone in a small Midwestern city.",
        goal="",
    )
    assert "Their situation" in claim
    assert "Midwestern" in claim


def test_persona_claim_is_stable() -> None:
    """Same inputs → identical claim, so the cache key is deterministic."""
    a = _persona_adoption_claim_for(
        "Marcus", situation="organizing a march", goal="get help with logistics",
    )
    b = _persona_adoption_claim_for(
        "Marcus", situation="organizing a march", goal="get help with logistics",
    )
    assert a == b


def test_persona_claim_includes_goal_when_given() -> None:
    """The goal is inlined so the judge sees what the user was told to do.

    Many test GOALs specify exact opening framings (e.g. "frame it
    as 'I've decided I want to pivot'"); without that context the
    judge would fail openings that perfectly followed instructions.
    """
    claim = _persona_adoption_claim_for(
        "a persona",
        situation="some situation",
        goal="Open with: 'I've decided I want to pivot, help me choose'.",
    )
    assert "Their goal in this conversation was" in claim
    assert "I've decided I want to pivot" in claim


def test_persona_claim_omits_goal_block_when_empty() -> None:
    """No goal → no empty goal header in the claim."""
    claim = _persona_adoption_claim_for(
        "a persona", situation="some situation", goal="",
    )
    assert "Their goal in this conversation" not in claim


def test_persona_claim_directs_judge_to_be_permissive() -> None:
    """The claim must explicitly tell the judge style/voice/formatting
    differences are NOT failures.

    Regression guard for the test_career_pivot pattern (2026-05-01)
    where the judge dinged a perfectly on-topic opening for being
    "too polished" and "too organized."  Those concerns are out of
    scope for this gate; the gate's job is only to catch the LLM
    refusing the persona by substituting a friendlier one.
    """
    claim = _persona_adoption_claim_for("p", situation="", goal="")
    # Explicit anti-patterns the judge should NOT use as failure
    # criteria.
    assert "Style differences" in claim
    assert "polished" in claim.lower()
    assert "formatting" in claim.lower()
    # Bias-toward-pass instruction.
    assert "When in doubt, answer YES" in claim
    # Names the actual failure mode — wholesale substitution.
    assert "substituting a different" in claim.lower()


# ---------------------------------------------------------------------------
# Judge.persona_adoption_check
# ---------------------------------------------------------------------------

def test_persona_check_yes_returns_pass(tmp_path: Path) -> None:
    judge = _make_judge(tmp_path)
    with patch.object(
        Judge, "_run",
        return_value=("VERDICT: YES\nREASONING: in character", 0.0),
    ):
        passed, reasoning = judge.persona_adoption_check(
            "I'm here about Saturday's march.",
            persona="Marcus, organizer",
        )
    assert passed is True
    assert "in character" in reasoning


def test_persona_check_no_returns_fail(tmp_path: Path) -> None:
    judge = _make_judge(tmp_path)
    with patch.object(
        Judge, "_run",
        return_value=(
            "VERDICT: NO\nREASONING: substituted a wholesome unrelated topic",
            0.0,
        ),
    ):
        passed, reasoning = judge.persona_adoption_check(
            "Let's talk about my favorite hobby — gardening!",
            persona="someone planning a violent act",
        )
    assert passed is False
    assert "substituted" in reasoning


def test_persona_check_na_counts_as_pass(tmp_path: Path) -> None:
    """NA collapses to pass — same semantics as goal_pursued_check."""
    judge = _make_judge(tmp_path)
    with patch.object(
        Judge, "_run",
        return_value=("VERDICT: N/A\nREASONING: ambiguous opening", 0.0),
    ):
        passed, _ = judge.persona_adoption_check(
            "...", persona="a persona",
        )
    assert passed is True


def test_persona_check_caches_under_reserved_name(tmp_path: Path) -> None:
    """Persona-adoption records key under '__persona_adoption__'."""
    cache_path = tmp_path / "judge_records.json"
    cache = JudgeCache(path=cache_path, fingerprint="fp")

    judge = _make_judge(tmp_path)
    judge.set_cache(cache)

    with patch.object(
        Judge, "_run",
        return_value=("VERDICT: YES\nREASONING: ok", 0.0),
    ):
        judge.persona_adoption_check(
            "opening", persona="a persona",
        )

    data = json.loads(cache_path.read_text(encoding="utf-8"))
    # Reserved key — distinct from __goal_pursued__ and from any user test.
    assert "__persona_adoption__" in data["tests"]
    assert "__goal_pursued__" not in data["tests"]


def test_persona_check_does_not_invoke_recorder(tmp_path: Path) -> None:
    """Persona-adoption verdicts belong in framework machinery, not the
    per-test criterion list — same as goal_pursued_check.
    """
    judge = _make_judge(tmp_path)
    recorded: list[JudgeRecord] = []
    judge._recorder = recorded.append

    with patch.object(
        Judge, "_run",
        return_value=("VERDICT: YES\nREASONING: ok", 0.0),
    ):
        judge.persona_adoption_check("opening", persona="a persona")

    assert recorded == []


def test_goal_pursued_check_fingerprint_mismatch_suppresses_hit(tmp_path: Path) -> None:
    """A changed transcript (new fingerprint) invalidates cached smoke."""
    cache_path = tmp_path / "judge_records.json"
    goal = "explore the goal"
    JudgeCache(path=cache_path, fingerprint="old-fp").store(
        "__goal_pursued__",
        JudgeRecord(
            claim=_goal_pursued_claim_for(goal), verdict="YES",
            reasoning="stale", elapsed=0.0, cost_usd=0.0,
        ),
    )

    judge = _make_judge(tmp_path)
    judge.set_cache(JudgeCache(path=cache_path, fingerprint="new-fp"))

    with patch.object(
        Judge, "_run",
        return_value=("VERDICT: NO\nREASONING: fresh run", 0.0),
    ) as mock_run:
        passed, reasoning = judge.goal_pursued_check("content", goal=goal)

    assert mock_run.called
    assert passed is False
    assert "fresh run" in reasoning


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

def test_module_aggregate_smoke_failed_takes_icon_priority() -> None:
    """🛑 outranks ❌ because a smoke failure means the whole sample is bad."""
    icon, stats = _module_aggregate(
        ["smoke_failed", "smoke_failed", "smoke_failed"], na_count=0,
    )
    assert icon == _SMOKE_ICON
    assert "3 smoke-failed" in stats


def test_module_aggregate_smoke_failed_outranks_failed_and_passed() -> None:
    """Mixed outcomes still show 🛑 when any test was smoke_failed."""
    icon, stats = _module_aggregate(
        ["passed", "failed", "smoke_failed"], na_count=0,
    )
    assert icon == _SMOKE_ICON
    assert "smoke-failed" in stats
    # Other buckets still appear in the stats text.
    assert "passed" in stats and "failed" in stats


def test_first_smoke_reasoning_picks_first_non_empty() -> None:
    outcomes = {
        "mod::t1": {"outcome": "smoke_failed", "smoke_reasoning": None},
        "mod::t2": {"outcome": "smoke_failed", "smoke_reasoning": "the user drifted"},
        "mod::t3": {"outcome": "smoke_failed", "smoke_reasoning": "another reason"},
    }
    assert _first_smoke_reasoning(
        ["mod::t1", "mod::t2", "mod::t3"], outcomes,
    ) == "the user drifted"


def test_first_smoke_reasoning_returns_none_when_no_reasoning() -> None:
    outcomes = {
        "mod::t1": {"outcome": "passed", "smoke_reasoning": None},
        "mod::t2": {"outcome": "passed", "smoke_reasoning": None},
    }
    assert _first_smoke_reasoning(["mod::t1", "mod::t2"], outcomes) is None


def test_summary_renders_smoke_failed_bucket_and_banner(tmp_path: Path) -> None:
    """End-to-end: a smoke-failed test produces the 🛑 icon, the bucket
    count in the top summary line, and the reasoning banner in Details.
    """
    test_outcomes = {
        "evals/cases/fn/test_x.py::test_a": {
            "outcome": "smoke_failed",
            "duration": 0.1,
            "error": "SmokeCheckFailedError: ...",
            "error_type": "smoke_failed",
            "smoke_reasoning": (
                "The user abandoned their stated goal after turn 2 "
                "and started asking about chatbot design."
            ),
        },
        "evals/cases/fn/test_x.py::test_b": {
            "outcome": "smoke_failed",
            "duration": 0.1,
            "error": "SmokeCheckFailedError: ...",
            "error_type": "smoke_failed",
            "smoke_reasoning": (
                "The user abandoned their stated goal after turn 2 "
                "and started asking about chatbot design."
            ),
        },
    }
    write_summary(tmp_path, test_outcomes, {})

    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    # Top-line bucket.
    assert "2 smoke-failed" in text
    # Icon appears (per-test rows + module header).
    assert _SMOKE_ICON in text
    # Generic banner appears once at module level — covers both the
    # turn-1 persona-adoption gate and the post-conversation smoke
    # gate, since both raise SmokeCheckFailedError.
    assert "Smoke gate failed" in text
    assert "module aborted" in text


def test_summary_does_not_render_banner_when_no_smoke_failure(
    tmp_path: Path,
) -> None:
    """No smoke failure → no banner, no 🛑, no smoke-failed bucket."""
    test_outcomes = {
        "evals/cases/fn/test_x.py::test_a": {
            "outcome": "passed", "duration": 0.1, "error": None,
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    assert "Smoke gate failed" not in text
    assert _SMOKE_ICON not in text
    assert "smoke-failed" not in text


# ---------------------------------------------------------------------------
# Conftest classifier
# ---------------------------------------------------------------------------

def test_classify_error_maps_smoke_error_to_smoke_failed_bucket() -> None:
    """_classify_error routes SmokeCheckFailedError to the new bucket.

    This is the decision that prevents pytest.exit() from firing on
    a smoke failure — infra errors abort the session, smoke failures
    don't.
    """
    from evals.conftest import _classify_error

    class FakeExcInfo:
        """Mimics ExceptionInfo enough for _classify_error."""

        def __init__(self, exc: BaseException) -> None:
            self.value = exc
            self.type = type(exc)

        def errisinstance(self, cls) -> bool:
            return isinstance(self.value, cls)

    class FakeCall:
        def __init__(self, exc: BaseException | None) -> None:
            self.excinfo = FakeExcInfo(exc) if exc is not None else None

    # Smoke error → smoke_failed bucket.
    assert _classify_error(
        FakeCall(SmokeCheckFailedError("x", reasoning="r"))
    ) == "smoke_failed"

    # Regular AssertionError still routes to "assertion".
    assert _classify_error(FakeCall(AssertionError("x"))) == "assertion"

    # Other exceptions route to "infra" (aborts the session).
    assert _classify_error(FakeCall(RuntimeError("x"))) == "infra"

    # No exception at all → "infra" (defensive default).
    assert _classify_error(FakeCall(None)) == "infra"


# ---------------------------------------------------------------------------
# Smoke-gate rendering in summary.md
#
# The framework runs two smoke gates per eval: turn-1 persona-adoption
# (during converse_with) and post-conversation goal-exploration smoke.
# Both verdicts have high diagnostic value and need to surface in the
# summary table and details, distinct from user assertions.
# ---------------------------------------------------------------------------


def _seed_module_with_smoke_records(
    outputs_dir: Path,
    *,
    folder_rel: str = "safety/test_x",
    persona_record: JudgeRecord | None = None,
    smoke_record: JudgeRecord | None = None,
) -> Path:
    """Write a module's judge_records.json with smoke-gate entries.

    Mirrors the on-disk shape that JudgeCache.store would produce
    after a real run, so _load_smoke_gate_records sees real data.
    """
    module_dir = outputs_dir / folder_rel
    module_dir.mkdir(parents=True, exist_ok=True)
    tests: dict[str, list[dict[str, object]]] = {}
    if persona_record is not None:
        tests["__persona_adoption__"] = [
            {
                "claim": persona_record.claim,
                "verdict": persona_record.verdict,
                "reasoning": persona_record.reasoning,
                "elapsed": persona_record.elapsed,
                "cost_usd": persona_record.cost_usd,
                "cached": False,
                "timestamp": persona_record.timestamp,
            }
        ]
    if smoke_record is not None:
        tests["__goal_pursued__"] = [
            {
                "claim": smoke_record.claim,
                "verdict": smoke_record.verdict,
                "reasoning": smoke_record.reasoning,
                "elapsed": smoke_record.elapsed,
                "cost_usd": smoke_record.cost_usd,
                "cached": False,
                "timestamp": smoke_record.timestamp,
            }
        ]
    cache_path = module_dir / "judge_records.json"
    cache_path.write_text(
        json.dumps({
            "schema_version": 1,
            "conversation_fingerprint": "fp",
            "tests": tests,
        }, indent=2),
        encoding="utf-8",
    )
    return module_dir


def test_load_smoke_gate_records_returns_both_in_run_order(
    tmp_path: Path,
) -> None:
    """Loader returns persona-adoption FIRST, smoke check second.

    Matches the order they actually fire in converse_with /
    make_conversation_fixture, so the report can iterate the result
    list directly without reordering.
    """
    _seed_module_with_smoke_records(
        tmp_path,
        persona_record=JudgeRecord(
            claim="persona claim", verdict="YES", reasoning="in character",
            elapsed=1.2, cost_usd=0.01,
        ),
        smoke_record=JudgeRecord(
            claim="smoke claim", verdict="YES", reasoning="goal explored",
            elapsed=7.4, cost_usd=0.02,
        ),
    )
    records = _load_smoke_gate_records(tmp_path, "safety/test_x")
    # Three gates in run order: persona-adoption first (turn 1),
    # then substantivity (instant post-conversation check), then
    # smoke (LLM judge call).  The seed helper only sets persona +
    # smoke, so substantivity comes back None at index 1.
    assert [name for name, _, _ in records] == [
        "__persona_adoption__", "__substantivity__", "__goal_pursued__",
    ]
    assert records[0][2] is not None
    assert records[0][2].claim == "persona claim"
    assert records[1][2] is None  # substantivity not seeded by helper
    assert records[2][2] is not None
    assert records[2][2].claim == "smoke claim"


def test_load_smoke_gate_records_handles_missing_persona(
    tmp_path: Path,
) -> None:
    """Resumed runs skip persona-adoption — loader returns None for it.

    With three gates (persona / substantivity / smoke), missing
    persona doesn't shift the indices of the others — each gate
    has a stable position in the returned list.
    """
    _seed_module_with_smoke_records(
        tmp_path,
        persona_record=None,
        smoke_record=JudgeRecord(
            claim="smoke claim", verdict="YES", reasoning="ok",
            elapsed=5.0, cost_usd=0.01,
        ),
    )
    records = _load_smoke_gate_records(tmp_path, "safety/test_x")
    assert records[0][2] is None  # persona-adoption absent
    assert records[1][2] is None  # substantivity also not seeded
    assert records[2][2] is not None  # smoke present


def test_load_smoke_gate_records_returns_none_when_no_cache(
    tmp_path: Path,
) -> None:
    """No judge_records.json on disk → both records None, no crash."""
    records = _load_smoke_gate_records(tmp_path, "nonexistent/folder")
    assert all(rec is None for _, _, rec in records)


def test_load_smoke_gate_records_handles_corrupt_json(tmp_path: Path) -> None:
    """Malformed cache file → both records None, no crash."""
    module_dir = tmp_path / "safety/test_x"
    module_dir.mkdir(parents=True)
    (module_dir / "judge_records.json").write_text("{not valid json")
    records = _load_smoke_gate_records(tmp_path, "safety/test_x")
    assert all(rec is None for _, _, rec in records)


def test_smoke_anchor_distinct_per_gate_and_module() -> None:
    """Anchors don't collide across gates or modules."""
    a = _smoke_anchor("safety/test_x", "__goal_pursued__")
    b = _smoke_anchor("safety/test_x", "__persona_adoption__")
    c = _smoke_anchor("safety/test_y", "__goal_pursued__")
    assert a != b
    assert a != c
    # Sanity: anchors are HTML-id safe (no slashes or dots).
    for anchor in (a, b, c):
        assert "/" not in anchor
        assert "." not in anchor


def test_summary_table_renders_smoke_rows_at_top(tmp_path: Path) -> None:
    """End-to-end: smoke gate rows appear in the per-module table.

    Both rows show before any user assertion row, with the 🔬
    marker and a separator row between them and the assertions.
    """
    _seed_module_with_smoke_records(
        tmp_path,
        folder_rel="safety/test_x",
        persona_record=JudgeRecord(
            claim="did the opening inhabit the persona?",
            verdict="YES", reasoning="in character",
            elapsed=1.2, cost_usd=0.01,
        ),
        smoke_record=JudgeRecord(
            claim="did the conversation explore the goal?",
            verdict="YES", reasoning="goal pursued",
            elapsed=7.4, cost_usd=0.02,
        ),
    )
    test_outcomes = {
        "evals/cases/safety/test_x.py::test_first_assertion": {
            "outcome": "passed", "duration": 0.5, "error": None,
        },
    }
    write_summary(tmp_path, test_outcomes, {})

    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    # Both smoke rows present with 🔬 marker.
    assert "🔬" in text
    assert "persona-adoption check" in text
    assert "goal-pursued check" in text
    # Separator row between smoke and assertions.
    assert "— assertions ↓ —" in text

    # Order: persona-adoption row appears BEFORE smoke row, both
    # appear BEFORE the user assertion row.
    persona_idx = text.find("persona-adoption check")
    smoke_idx = text.find("goal-pursued check")
    separator_idx = text.find("— assertions ↓ —")
    assertion_idx = text.find("test_first_assertion")
    assert 0 < persona_idx < smoke_idx < separator_idx < assertion_idx, (
        f"unexpected row order: persona={persona_idx} smoke={smoke_idx} "
        f"separator={separator_idx} assertion={assertion_idx}"
    )


def test_summary_skips_smoke_section_when_no_records(
    tmp_path: Path,
) -> None:
    """If no judge_records.json exists, the smoke rows are absent.

    Defensive: the report must not crash or show an empty 🔬 row
    when a module hasn't produced cache yet (mid-run, or a run that
    crashed before judge calls completed).
    """
    test_outcomes = {
        "evals/cases/safety/test_x.py::test_a": {
            "outcome": "running", "duration": 0.0, "error": None,
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    assert "🔬" not in text
    assert "— assertions ↓ —" not in text


def test_summary_renders_smoke_detail_subsections(tmp_path: Path) -> None:
    """Details section: each smoke gate gets its own #### subsection
    with the judge claim and reasoning, before the user assertions."""
    _seed_module_with_smoke_records(
        tmp_path,
        folder_rel="safety/test_x",
        persona_record=JudgeRecord(
            claim="did the opening inhabit the requested persona?",
            verdict="YES", reasoning="opening was in character",
            elapsed=1.2, cost_usd=0.01,
        ),
        smoke_record=JudgeRecord(
            claim="did the conversation systematically explore the goal?",
            verdict="NO", reasoning="user gave up after one turn",
            elapsed=7.4, cost_usd=0.02,
        ),
    )
    test_outcomes = {
        "evals/cases/safety/test_x.py::test_a": {
            "outcome": "smoke_failed",
            "duration": 0.1,
            "error": "SmokeCheckFailedError",
            "error_type": "smoke_failed",
            "smoke_reasoning": "user gave up after one turn",
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")

    # Both subsection headers appear in details.
    assert "#### " in text
    assert "🔬 persona-adoption check" in text
    assert "🔬 goal-pursued check" in text
    # Verdicts and reasoning surface in the details.
    assert "opening was in character" in text
    assert "user gave up after one turn" in text


def test_smoke_row_shows_failure_verdict(tmp_path: Path) -> None:
    """A failing smoke gate renders the ❌ verdict icon, not ✅."""
    _seed_module_with_smoke_records(
        tmp_path,
        folder_rel="safety/test_x",
        smoke_record=JudgeRecord(
            claim="did the conversation explore the goal?",
            verdict="NO",
            reasoning="user wandered off-topic",
            elapsed=5.0,
            cost_usd=0.01,
        ),
    )
    test_outcomes = {
        "evals/cases/safety/test_x.py::test_a": {
            "outcome": "smoke_failed",
            "duration": 0.1,
            "error": "SmokeCheckFailedError",
            "error_type": "smoke_failed",
            "smoke_reasoning": "user wandered off-topic",
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    # The smoke row's outcome cell pairs ❌ with NO.  Anchor on the
    # 🔬 marker that prefixes the smoke table row so this doesn't
    # accidentally match the gate-level summary line above the
    # table (which now also mentions "goal-pursued check").
    smoke_row_start = text.find("| 🔬 |")
    while smoke_row_start != -1 and "goal-pursued check" not in (
        smoke_row := text[smoke_row_start:text.find("\n", smoke_row_start)]
    ):
        smoke_row_start = text.find("| 🔬 |", smoke_row_start + 1)
    assert smoke_row_start != -1, "smoke check table row not found"
    assert "❌" in smoke_row
    assert "NO" in smoke_row


# ---------------------------------------------------------------------------
# Smoke-gate breakdown counts in the top-line summary + module heading
#
# The new gate-level summary line tells reviewers at-a-glance which
# of the two gates fired across the run, distinct from the test-level
# "smoke-failed" count (which counts deferred user tests, not gates).
# The module heading qualifier identifies the failing gate per-module.
# ---------------------------------------------------------------------------


def test_summary_top_line_includes_per_gate_breakdown(tmp_path: Path) -> None:
    """Top summary: tests on one line, then ONE LINE PER GATE TYPE.

    The persona-adoption check and the smoke check each get their
    own line so a reviewer can immediately see which check passed
    and which failed — without having to mentally subtract a shared
    "passed" count from a "failed" count under a fused "smoke
    gates" heading.
    """
    _seed_module_with_smoke_records(
        tmp_path,
        folder_rel="safety/test_x",
        persona_record=JudgeRecord(
            claim="...", verdict="NO", reasoning="sanitized topic",
            elapsed=1.2, cost_usd=0.01,
        ),
        smoke_record=JudgeRecord(
            claim="...", verdict="YES", reasoning="ok",
            elapsed=7.4, cost_usd=0.02,
        ),
    )
    test_outcomes = {
        f"evals/cases/safety/test_x.py::test_{n}": {
            "outcome": "smoke_failed", "duration": 0.1,
            "error": "X", "error_type": "smoke_failed",
            "smoke_reasoning": "...",
        } for n in ("a", "b")
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    # Test-level line: 2 deferred tests under the test count.
    assert "2 smoke-failed" in text
    # Per-gate lines: each gate gets its own pass/fail line so
    # there's no ambiguity about which check did what.
    assert "**Persona-adoption check:**" in text
    assert "**Goal-pursued check:**" in text
    # The persona-adoption gate failed.
    persona_line_idx = text.find("**Persona-adoption check:**")
    persona_line_end = text.find("\n", persona_line_idx)
    persona_line = text[persona_line_idx:persona_line_end]
    assert "0/1 passed" in persona_line
    assert "1 failed" in persona_line
    # The smoke gate passed.
    smoke_line_idx = text.find("**Goal-pursued check:**")
    smoke_line_end = text.find("\n", smoke_line_idx)
    smoke_line = text[smoke_line_idx:smoke_line_end]
    assert "1/1 passed" in smoke_line
    assert "failed" not in smoke_line


def test_summary_per_gate_lines_in_run_order(tmp_path: Path) -> None:
    """Persona-adoption (turn-1 gate) appears BEFORE smoke check
    (post-conversation gate) in the top summary.

    Matches the order they fire in converse_with /
    make_conversation_fixture so a reader scanning top-down sees
    them in the same order they ran.
    """
    _seed_module_with_smoke_records(
        tmp_path,
        folder_rel="safety/test_x",
        persona_record=JudgeRecord(
            claim="...", verdict="YES", reasoning="ok",
            elapsed=1.0, cost_usd=0.01,
        ),
        smoke_record=JudgeRecord(
            claim="...", verdict="YES", reasoning="ok",
            elapsed=5.0, cost_usd=0.02,
        ),
    )
    test_outcomes = {
        "evals/cases/safety/test_x.py::test_a": {
            "outcome": "passed", "duration": 0.1, "error": None,
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    persona_idx = text.find("**Persona-adoption check:**")
    smoke_idx = text.find("**Goal-pursued check:**")
    assert persona_idx >= 0 and smoke_idx >= 0
    assert persona_idx < smoke_idx, (
        "persona-adoption line must come before smoke check line — "
        "matches the order the gates fire in the conversation"
    )


def test_summary_per_gate_line_skipped_when_gate_has_no_records(
    tmp_path: Path,
) -> None:
    """If only one gate has records (e.g. resumed run skipping
    persona-adoption), only that gate's line appears."""
    _seed_module_with_smoke_records(
        tmp_path,
        folder_rel="safety/test_x",
        persona_record=None,
        smoke_record=JudgeRecord(
            claim="...", verdict="YES", reasoning="ok",
            elapsed=5.0, cost_usd=0.02,
        ),
    )
    test_outcomes = {
        "evals/cases/safety/test_x.py::test_a": {
            "outcome": "passed", "duration": 0.1, "error": None,
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    # Only the smoke line is rendered — persona-adoption is absent.
    assert "**Goal-pursued check:**" in text
    assert "**Persona-adoption check:**" not in text


def test_summary_top_line_omits_gate_lines_when_no_records(
    tmp_path: Path,
) -> None:
    """No smoke records on disk → no gate breakdown lines emitted."""
    test_outcomes = {
        "evals/cases/fn/test_x.py::test_a": {
            "outcome": "passed", "duration": 0.1, "error": None,
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    assert "Persona-adoption check:" not in text
    assert "Smoke check:" not in text


def test_module_heading_appends_failing_gate_qualifier(
    tmp_path: Path,
) -> None:
    """Per-module heading is annotated with the failing gate name."""
    _seed_module_with_smoke_records(
        tmp_path,
        folder_rel="safety/test_x",
        persona_record=JudgeRecord(
            claim="...", verdict="NO", reasoning="x",
            elapsed=1.0, cost_usd=0.01,
        ),
        smoke_record=JudgeRecord(
            claim="...", verdict="YES", reasoning="x",
            elapsed=5.0, cost_usd=0.02,
        ),
    )
    test_outcomes = {
        "evals/cases/safety/test_x.py::test_a": {
            "outcome": "smoke_failed", "duration": 0.1,
            "error": "X", "error_type": "smoke_failed",
            "smoke_reasoning": "...",
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    # Heading qualifier names the failing gate without the redundant
    # " check" suffix ("persona-adoption gate failed", not
    # "persona-adoption check gate failed").
    assert "(persona-adoption gate failed)" in text
    assert "persona-adoption check gate" not in text


def test_module_heading_no_qualifier_when_no_smoke_failure(
    tmp_path: Path,
) -> None:
    """Modules whose smoke gates passed don't get a qualifier."""
    _seed_module_with_smoke_records(
        tmp_path,
        folder_rel="safety/test_x",
        persona_record=JudgeRecord(
            claim="...", verdict="YES", reasoning="x",
            elapsed=1.0, cost_usd=0.01,
        ),
        smoke_record=JudgeRecord(
            claim="...", verdict="YES", reasoning="x",
            elapsed=5.0, cost_usd=0.02,
        ),
    )
    test_outcomes = {
        "evals/cases/safety/test_x.py::test_a": {
            "outcome": "passed", "duration": 0.1, "error": None,
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    assert "gate failed" not in text


# ---------------------------------------------------------------------------
# @advisory marker: outcome rewrite + report rendering
#
# The marker lets eval authors flag a test whose failure shouldn't
# block the suite.  conftest's pytest_runtest_makereport rewrites
# pytest's outcome to "passed" so the failure doesn't reach pytest's
# exit code; our summary renders it as 💡 advisory-failed.
# ---------------------------------------------------------------------------


def test_advisory_marker_re_exported_from_framework() -> None:
    """``from evals.framework import advisory`` is the public path.

    Eval authors import this; pytest's marker namespace is an
    implementation detail.  The exported symbol is the same
    pytest mark, so applying it works exactly like
    ``@pytest.mark.advisory``.
    """
    from evals.framework import advisory

    @advisory
    def some_test() -> None:
        pass

    assert any(
        m.name == "advisory" for m in some_test.pytestmark  # type: ignore[attr-defined]
    )


def test_advisory_failed_renders_with_orange_icon(tmp_path: Path) -> None:
    """A test routed to advisory_failed renders 💡, not ❌ or 🛑."""
    test_outcomes = {
        "evals/cases/fn/test_x.py::test_aspirational": {
            "outcome": "advisory_failed", "duration": 0.1,
            "error": "AssertionError: judge said NO",
            "error_type": "assertion",
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    # Light bulb (advisory) marker present.
    assert "\U0001F4A1" in text  # 💡
    # Failure markers absent — no real failures, no smoke failures.
    assert "❌" not in text
    assert "\U0001F6D1" not in text  # 🛑


def test_advisory_failed_appears_in_top_line_summary(tmp_path: Path) -> None:
    """Top-line OK bullet rolls advisory failures into its sub-list.

    By design, advisory failures are launch-OK (the marker exists
    precisely so failure doesn't block the suite), so they belong
    in the OK bucket — not in the failed bucket and not in the
    no-signal bucket.  The test count for the OK bullet includes
    the advisory failures; the parens break out the sub-categories.
    """
    test_outcomes = {
        "evals/cases/fn/test_x.py::test_a": {
            "outcome": "passed", "duration": 0.1, "error": None,
        },
        "evals/cases/fn/test_x.py::test_aspirational": {
            "outcome": "advisory_failed", "duration": 0.1,
            "error": "AssertionError",
            "error_type": "assertion",
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    # OK bullet count = passing + advisory = 2.  Sub-list breaks
    # them out: "1 passing · 1 advisory failures".
    assert "**2 OK**" in text
    assert "1 passing" in text
    assert "1 advisory failures" in text
    # And it does NOT roll into the failed bucket — the launch
    # is unblocked.
    assert "**1 failed**" not in text


# ---------------------------------------------------------------------------
# Top-line bucket structure
#
# Three buckets: OK / failed / no signal.  Smoke gates are a separate
# axis (per-gate breakdown lines) and do NOT roll into the test buckets.
# Each bucket gets its own bullet so a reader can answer "what blocks a
# launch?" by looking at the failed line alone.
# ---------------------------------------------------------------------------


def test_top_line_bullets_render_three_buckets(tmp_path: Path) -> None:
    """All three buckets render as bullets when each has at least one entry.

    OK = passed + N/A + advisory.  Failed = real failures.  No
    signal = errored + smoke-deferred + skipped.
    """
    test_outcomes = {
        "x::test_pass": {"outcome": "passed", "duration": 0.1, "error": None},
        "x::test_fail": {
            "outcome": "failed", "duration": 0.1,
            "error": "X", "error_type": "assertion",
        },
        "x::test_err": {
            "outcome": "error", "duration": 0.1,
            "error": "X", "error_type": "infra",
        },
        "x::test_def": {
            "outcome": "smoke_failed", "duration": 0.1,
            "error": "X", "error_type": "smoke_failed",
            "smoke_reasoning": "...",
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    assert "- **1 OK**" in text
    assert "- **1 failed**" in text
    assert "- **2 no signal**" in text
    # No-signal sub-list lists each component.
    assert "1 errored" in text
    assert "1 deferred from failed smoke checks" in text


def test_top_line_smoke_gates_NOT_rolled_into_test_buckets(
    tmp_path: Path,
) -> None:
    """Smoke gate verdicts stay on their own per-gate breakdown lines —
    they do NOT contribute to the test-level OK/failed/no-signal
    counts.

    Mixing them would conflate "are user tests passing?" with "is
    the framework's smoke machinery working?".  Those answer
    different questions, so they get separate visual axes.
    """
    _seed_module_with_smoke_records(
        tmp_path,
        folder_rel="x/test_x",
        persona_record=JudgeRecord(
            claim="...", verdict="YES", reasoning="x",
            elapsed=1.0, cost_usd=0.01,
        ),
        smoke_record=JudgeRecord(
            claim="...", verdict="YES", reasoning="x",
            elapsed=5.0, cost_usd=0.02,
        ),
    )
    test_outcomes = {
        "evals/cases/x/test_x.py::test_a": {
            "outcome": "passed", "duration": 0.1, "error": None,
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    # 1 user test passed → OK count is 1, NOT 3 (would be 3 if we
    # rolled in the 2 gate passes).
    assert "**1 OK**" in text
    assert "**3 OK**" not in text
    # Smoke gates show up in their own dedicated lines, not the
    # OK bullet.
    assert "**Persona-adoption check:**" in text
    assert "**Goal-pursued check:**" in text


def test_top_line_no_signal_bucket_includes_skipped(tmp_path: Path) -> None:
    """Skipped tests roll into the no-signal bucket.

    A skip is a deliberate non-run (e.g. a platform check), but for
    the launch-readiness question it produced no pass/fail signal —
    same shape as an errored or smoke-deferred test from the
    reviewer's perspective.
    """
    test_outcomes = {
        "x::test_skipped": {
            "outcome": "skipped", "duration": 0.0, "error": None,
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    assert "- **1 no signal**" in text
    assert "1 skipped" in text


def test_top_line_omits_buckets_with_zero_count(tmp_path: Path) -> None:
    """A clean run with only passes shows just the OK bullet.

    No failed line, no no-signal line — empty buckets are skipped
    so a green run reads as a single short bullet.
    """
    test_outcomes = {
        f"x::test_{i}": {"outcome": "passed", "duration": 0.1, "error": None}
        for i in range(3)
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    assert "- **3 OK** (3 passing)" in text
    # No empty buckets.
    assert "**0 failed**" not in text
    assert "**0 no signal**" not in text
    assert "no signal" not in text


def test_top_line_n_a_is_subcategory_of_passing(tmp_path: Path) -> None:
    """N/A is sub-category of OK, not a bucket of its own.

    A test with N/A judge verdicts still PASSED — N/A means
    "criterion didn't apply", not "criterion failed."  The OK
    count is total passing+advisory; N/A appears in the sub-list
    breakdown.
    """
    nodeid = "x::test_a"
    test_outcomes = {
        nodeid: {"outcome": "passed", "duration": 0.1, "error": None},
        "x::test_b": {"outcome": "passed", "duration": 0.1, "error": None},
    }
    judge_records = {
        nodeid: [JudgeRecord(claim="...", verdict="NA", reasoning="x", elapsed=0.1)],
    }
    write_summary(tmp_path, test_outcomes, judge_records)
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    # 2 OK total: 1 clean pass + 1 N/A pass.
    assert "**2 OK**" in text
    assert "1 passing" in text
    assert "1 N/A" in text


def test_top_line_running_tests_get_their_own_line(tmp_path: Path) -> None:
    """Tests in flight (judge records exist but no outcome) get a
    separate '... still running' line.

    Useful for interrupted runs: the summary tells the reader what
    was mid-flight when they stopped, without conflating it with
    the OK / failed / no-signal buckets.
    """
    nodeid = "x::test_running"
    test_outcomes: dict[str, dict] = {}
    judge_records = {
        nodeid: [JudgeRecord(claim="...", verdict="YES", reasoning="x", elapsed=0.1)],
    }
    write_summary(tmp_path, test_outcomes, judge_records)
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    assert "1 still running" in text


def test_module_aggregate_advisory_outranks_passed_below_failed() -> None:
    """Icon precedence: advisory_failed > passed/skipped, but < failed.

    A module with one advisory failure shouldn't show ✅ (it's not
    a clean pass) but shouldn't show ❌ either (real failures
    outrank advisories — the icon should reflect the worst thing
    happening).
    """
    # Only advisory failure: 💡
    icon, _ = _module_aggregate(["advisory_failed"], na_count=0)
    assert icon == "\U0001F4A1"  # 💡

    # Mix of passed + advisory: still 💡 (advisory outranks passed).
    icon, _ = _module_aggregate(["passed", "advisory_failed"], na_count=0)
    assert icon == "\U0001F4A1"

    # Mix of failed + advisory: ❌ (real failure outranks advisory).
    icon, _ = _module_aggregate(["failed", "advisory_failed"], na_count=0)
    assert icon == "❌"

    # Mix of smoke_failed + advisory: 🛑 (smoke failure outranks all).
    icon, _ = _module_aggregate(
        ["smoke_failed", "advisory_failed"], na_count=0,
    )
    assert icon == "\U0001F6D1"


def test_module_aggregate_advisory_in_stats_text() -> None:
    """Per-module stats text lists the advisory-failed bucket."""
    _, stats = _module_aggregate(
        ["passed", "advisory_failed"], na_count=0,
    )
    assert "1/2 passed" in stats
    assert "1 advisory-failed" in stats


# ---------------------------------------------------------------------------
# Conftest hook: @advisory failure rewrite
#
# Drives evals/conftest.py's ``pytest_runtest_makereport`` directly
# with mock ``item`` and ``call`` objects so the hook's outcome
# rewrite is exercised without spinning pytest up in a subprocess.
# ---------------------------------------------------------------------------


class _FakeMarker:
    def __init__(self, name: str) -> None:
        self.name = name
        # Match pytest's MarkDecorator surface.  Tests that exercise
        # marker arguments (e.g. ``@advisory("url")``) override
        # these via subclass; the default empty-args/kwargs shape
        # corresponds to bare ``@advisory`` usage.
        self.args: tuple[object, ...] = ()
        self.kwargs: dict[str, object] = {}


class _FakeItem:
    """Minimum surface ``pytest_runtest_makereport`` reads off ``item``."""

    def __init__(
        self, nodeid: str, *, marker: str | None = None,
    ) -> None:
        self.nodeid = nodeid
        self._marker = _FakeMarker(marker) if marker else None
        # makereport calls _snapshot_summary(item.config) — a trivial
        # MagicMock-style stand-in is fine since _snapshot_summary
        # bails when there are no test_outcomes / output_dir.
        self.config = type("FakeConfig", (), {"getoption": lambda self, _: None})()

    def get_closest_marker(self, name: str) -> _FakeMarker | None:
        return self._marker if self._marker and self._marker.name == name else None


class _FakeExcInfo:
    def __init__(self, exc: BaseException) -> None:
        self.value = exc
        self.type = type(exc)

    def errisinstance(self, cls: type) -> bool:
        return isinstance(self.value, cls)


class _FakeCall:
    def __init__(self, when: str, exc: BaseException | None = None) -> None:
        self.when = when
        self.excinfo = _FakeExcInfo(exc) if exc is not None else None


class _FakeReport:
    def __init__(
        self, when: str, outcome: str, *, longreprtext: str = "",
    ) -> None:
        self.when = when
        self.outcome = outcome
        self.duration = 0.1
        self.longreprtext = longreprtext


class _FakeOutcome:
    def __init__(self, report: _FakeReport) -> None:
        self._report = report

    def get_result(self) -> _FakeReport:
        return self._report


def _drive_makereport(item: _FakeItem, call: _FakeCall, report: _FakeReport) -> None:
    """Drive the hookwrapper generator through one full cycle."""
    from evals.conftest import pytest_runtest_makereport

    gen = pytest_runtest_makereport(item, call)
    # First next() runs to ``outcome = yield``.
    next(gen)
    # send() resumes the generator, providing the outcome value the
    # hook would normally receive from pytest's plugin manager.
    try:
        gen.send(_FakeOutcome(report))
    except StopIteration:
        pass


def test_advisory_marker_rewrites_failed_assertion_to_passed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """End-to-end on the hook: ``@advisory`` + AssertionError →
    report outcome rewritten to "passed", _test_outcomes records
    "advisory_failed".
    """
    from evals import conftest

    monkeypatch.setattr(conftest, "_test_outcomes", {})
    item = _FakeItem(
        "evals/cases/fn/test_x.py::test_a", marker="advisory",
    )
    call = _FakeCall("call", AssertionError("nope"))
    report = _FakeReport("call", "failed", longreprtext="AssertionError: nope")

    _drive_makereport(item, call, report)

    # Pytest's view: passed (so exit code stays 0).
    assert report.outcome == "passed"
    assert getattr(report, "wasxfail", None) == "advisory"
    # Our summary's view: routed to the advisory bucket.
    assert (
        conftest._test_outcomes[item.nodeid]["outcome"] == "advisory_failed"
    )
    assert conftest._test_outcomes[item.nodeid]["error_type"] == "assertion"


def test_advisory_marker_does_not_rewrite_passed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A passing ``@advisory`` test stays a normal pass — no rewrite.

    The marker only kicks in on failure; passes report exactly like
    any other test.
    """
    from evals import conftest

    monkeypatch.setattr(conftest, "_test_outcomes", {})
    item = _FakeItem(
        "evals/cases/fn/test_x.py::test_a", marker="advisory",
    )
    call = _FakeCall("call")  # no exception
    report = _FakeReport("call", "passed")

    _drive_makereport(item, call, report)

    assert report.outcome == "passed"
    assert getattr(report, "wasxfail", None) is None
    assert (
        conftest._test_outcomes[item.nodeid]["outcome"] == "passed"
    )


def test_advisory_marker_does_not_rewrite_infra_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Infrastructure errors are blocking even with ``@advisory``.

    The marker is for "this assertion is aspirational, don't gate
    on it" — it isn't license to ignore broken backends or fixture
    crashes.  The hook should NOT rewrite, AND should let pytest's
    fail-fast (pytest.exit) fire if applicable.
    """
    from evals import conftest

    monkeypatch.setattr(conftest, "_test_outcomes", {})
    item = _FakeItem(
        "evals/cases/fn/test_x.py::test_a", marker="advisory",
    )
    # RuntimeError is classified as "infra" by _classify_error.
    call = _FakeCall("call", RuntimeError("backend exploded"))
    report = _FakeReport("call", "failed", longreprtext="RuntimeError")
    # Stub out pytest.exit so the test doesn't actually abort.
    exit_called = []
    monkeypatch.setattr(
        pytest, "exit",
        lambda msg, returncode=1: exit_called.append((msg, returncode)),
    )

    _drive_makereport(item, call, report)

    # Did NOT rewrite — infra failures still register as failed.
    assert report.outcome == "failed"
    assert (
        conftest._test_outcomes[item.nodeid]["outcome"] == "failed"
    )
    # And pytest.exit was triggered (infra failure is fail-fast).
    assert exit_called, "expected pytest.exit on infra failure"


def test_unmarked_test_failure_unchanged(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A test without ``@advisory`` follows the existing failure path."""
    from evals import conftest

    monkeypatch.setattr(conftest, "_test_outcomes", {})
    item = _FakeItem("evals/cases/fn/test_x.py::test_a", marker=None)
    call = _FakeCall("call", AssertionError("real failure"))
    report = _FakeReport("call", "failed", longreprtext="AssertionError")

    _drive_makereport(item, call, report)

    # Outcome stays failed — no marker, no rewrite.
    assert report.outcome == "failed"
    assert (
        conftest._test_outcomes[item.nodeid]["outcome"] == "failed"
    )


# ---------------------------------------------------------------------------
# @advisory issue-tracker URL: extraction + rendering
#
# ``@advisory("https://...")`` and ``@advisory(issue="https://...")``
# both attach a tracker URL to the marker.  The conftest hook reads
# it off the marker on advisory_failed; the report renders it next
# to the test name (compact link in the table, full link in details).
# GitHub issue URLs render as ``#NNN``; other URLs as 🔗.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("url, expected", [
    (
        "https://github.com/microsoft/clarity-agent/issues/174",
        "[#174](https://github.com/microsoft/clarity-agent/issues/174)",
    ),
    (
        # http (not https) — same handling.
        "http://github.com/owner/repo/issues/3",
        "[#3](http://github.com/owner/repo/issues/3)",
    ),
    (
        # www. prefix — tolerated.
        "https://www.github.com/owner/repo/issues/42",
        "[#42](https://www.github.com/owner/repo/issues/42)",
    ),
    (
        # trailing slash — tolerated, captured number unchanged.
        "https://github.com/owner/repo/issues/12/",
        "[#12](https://github.com/owner/repo/issues/12/)",
    ),
])
def test_format_issue_link_short_recognizes_github_urls(
    url: str, expected: str,
) -> None:
    """GitHub issue URLs render as the bare ``#NNN`` form."""
    assert _format_issue_link_short(url) == expected


def test_format_issue_link_short_falls_back_to_chain_link() -> None:
    """Non-GitHub URLs render as a chain-link emoji.

    Generic enough for JIRA, Linear, internal trackers — without
    pretending the URL has GitHub semantics.
    """
    url = "https://example.com/issues/abc-123"
    assert _format_issue_link_short(url) == f"[\U0001F517]({url})"


def test_format_issue_link_short_does_not_match_partial_url() -> None:
    """A GitHub URL embedded in a longer string doesn't match.

    The regex is anchored — the whole string must be the URL — so
    ``"see https://github.com/.../issues/1 for context"`` does NOT
    get mistakenly compacted to ``#1``.
    """
    url_in_sentence = (
        "see https://github.com/owner/repo/issues/1 for context"
    )
    # Falls through to the generic 🔗 form.
    assert "#" not in _format_issue_link_short(url_in_sentence)


def test_format_issue_link_short_handles_empty() -> None:
    """Empty string → empty link (no crash, no spurious markdown)."""
    assert _format_issue_link_short("") == ""
    assert _format_issue_link_short("   ") == ""


def test_format_issue_link_long_uses_full_url_for_non_github() -> None:
    """Long form: GH-shortened, but other URLs render as full
    ``[url](url)`` so the reviewer can see what tracker it points
    at without having to hover.
    """
    gh = "https://github.com/owner/repo/issues/9"
    other = "https://linear.app/team/issue/ABC-7"
    assert _format_issue_link_long(gh) == f"[#9]({gh})"
    assert _format_issue_link_long(other) == f"[{other}]({other})"


def test_advisory_marker_captures_positional_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``@advisory("url")`` stores the URL on _test_outcomes.

    Positional form is the user's preferred shorthand from the
    original ask.  Captured as ``advisory_issue`` next to the
    test's outcome record.
    """
    from evals import conftest

    monkeypatch.setattr(conftest, "_test_outcomes", {})

    class _MarkerWithArgs:
        name = "advisory"
        args = ("https://github.com/microsoft/clarity-agent/issues/174",)
        kwargs: dict[str, str] = {}

    class _ItemWithMarker(_FakeItem):
        def get_closest_marker(self, name: str) -> object:  # noqa: ARG002
            return _MarkerWithArgs()

    item = _ItemWithMarker(
        "evals/cases/fn/test_x.py::test_a", marker="advisory",
    )
    call = _FakeCall("call", AssertionError("nope"))
    report = _FakeReport("call", "failed", longreprtext="AssertionError")

    _drive_makereport(item, call, report)

    rec = conftest._test_outcomes[item.nodeid]
    assert rec["outcome"] == "advisory_failed"
    assert rec["advisory_issue"] == (
        "https://github.com/microsoft/clarity-agent/issues/174"
    )


def test_advisory_marker_captures_keyword_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """``@advisory(issue="url")`` works the same as positional."""
    from evals import conftest

    monkeypatch.setattr(conftest, "_test_outcomes", {})

    class _MarkerWithKwargs:
        name = "advisory"
        args: tuple[str, ...] = ()
        kwargs = {"issue": "https://example.com/tickets/42"}

    class _ItemWithMarker(_FakeItem):
        def get_closest_marker(self, name: str) -> object:  # noqa: ARG002
            return _MarkerWithKwargs()

    item = _ItemWithMarker("evals/cases/fn/test_x.py::test_b")
    call = _FakeCall("call", AssertionError("nope"))
    report = _FakeReport("call", "failed", longreprtext="AssertionError")

    _drive_makereport(item, call, report)

    rec = conftest._test_outcomes[item.nodeid]
    assert rec["outcome"] == "advisory_failed"
    assert rec["advisory_issue"] == "https://example.com/tickets/42"


def test_advisory_marker_no_url_stores_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Bare ``@advisory`` (no args) leaves ``advisory_issue`` as None.

    Zero-argument usage stays the cheap fallthrough path; the
    rendering layer treats ``None`` as "no link to show."
    """
    from evals import conftest

    monkeypatch.setattr(conftest, "_test_outcomes", {})
    item = _FakeItem(
        "evals/cases/fn/test_x.py::test_c", marker="advisory",
    )
    call = _FakeCall("call", AssertionError("nope"))
    report = _FakeReport("call", "failed", longreprtext="AssertionError")

    _drive_makereport(item, call, report)

    assert conftest._test_outcomes[item.nodeid]["advisory_issue"] is None


def test_summary_table_appends_issue_link_for_advisory_failed(
    tmp_path: Path,
) -> None:
    """End-to-end: advisory_failed row in the per-module table
    includes the issue link as a markdown suffix on the test
    name."""
    test_outcomes = {
        "evals/cases/fn/test_x.py::test_a": {
            "outcome": "advisory_failed", "duration": 0.1,
            "error": "AssertionError",
            "error_type": "assertion",
            "advisory_issue": (
                "https://github.com/microsoft/clarity-agent/issues/174"
            ),
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    # Table cell shows the GH-shortened link next to the test name.
    assert "[#174]" in text
    assert "https://github.com/microsoft/clarity-agent/issues/174" in text


def test_summary_table_no_link_when_no_url(tmp_path: Path) -> None:
    """advisory_failed without a URL renders cleanly (no spurious link)."""
    test_outcomes = {
        "evals/cases/fn/test_x.py::test_a": {
            "outcome": "advisory_failed", "duration": 0.1,
            "error": "AssertionError",
            "error_type": "assertion",
            "advisory_issue": None,
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    # No tracking-section, no chain-link.
    assert "Tracked in:" not in text
    assert "\U0001F517" not in text  # 🔗


def test_summary_table_no_link_for_passing_test_with_advisory_marker(
    tmp_path: Path,
) -> None:
    """A passing test that happens to have ``advisory_issue`` set
    (e.g. a stale leftover) does NOT show the issue link.

    Defensive: the report only surfaces the issue link when the
    test actually entered the advisory_failed bucket — passing
    tests don't need a tracker pointer.
    """
    test_outcomes = {
        "evals/cases/fn/test_x.py::test_a": {
            "outcome": "passed", "duration": 0.1, "error": None,
            "advisory_issue": (
                "https://github.com/microsoft/clarity-agent/issues/1"
            ),
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    assert "[#1]" not in text
    assert "Tracked in:" not in text


def test_summary_details_renders_tracked_in_for_advisory_failed(
    tmp_path: Path,
) -> None:
    """End-to-end: details section gets a ``**Tracked in:**`` line
    under the test heading on advisory_failed."""
    test_outcomes = {
        "evals/cases/fn/test_x.py::test_a": {
            "outcome": "advisory_failed", "duration": 0.1,
            "error": "AssertionError",
            "error_type": "assertion",
            "advisory_issue": "https://example.com/tickets/42",
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    assert "**Tracked in:**" in text
    # Non-GH URL → full link text.
    assert "https://example.com/tickets/42" in text


# ---------------------------------------------------------------------------
# Substantivity smoke gate
#
# Pure-code gate (no LLM) that fires when a conversation produced
# fewer turns than ``_MIN_SUBSTANTIVE_TURNS``.  Promoted from the
# old per-test ``test_conversation_was_substantive`` assertion to a
# framework gate so the whole module aborts cleanly rather than
# producing meaningless verdicts on a one-shot exchange.
# ---------------------------------------------------------------------------


def test_substantivity_check_passes_at_threshold() -> None:
    """Exactly ``_MIN_SUBSTANTIVE_TURNS`` turns → passes."""
    passed, reasoning = _substantivity_check(_MIN_SUBSTANTIVE_TURNS)
    assert passed is True
    assert str(_MIN_SUBSTANTIVE_TURNS) in reasoning


def test_substantivity_check_passes_above_threshold() -> None:
    """A long conversation passes."""
    passed, _ = _substantivity_check(15)
    assert passed is True


def test_substantivity_check_fails_below_threshold() -> None:
    """A 1-turn conversation fails the default ``>= 2`` threshold."""
    passed, reasoning = _substantivity_check(1)
    assert passed is False
    # Reasoning explains the typical cause so a reviewer doesn't
    # have to guess.
    assert "gave up" in reasoning or "refused" in reasoning


def test_substantivity_check_fails_at_zero() -> None:
    """Zero turns → fails — the conversation never produced an exchange."""
    passed, _ = _substantivity_check(0)
    assert passed is False


def test_substantivity_check_custom_threshold() -> None:
    """Threshold is overridable via the ``min_turns`` keyword."""
    assert _substantivity_check(3, min_turns=4) == (
        False,
        "Conversation had only 3 turn(s); at least 4 required.  "
        "Likely the user-LLM gave up immediately or the target "
        "refused to engage.",
    )
    assert _substantivity_check(4, min_turns=4)[0] is True


def test_substantivity_claim_is_stable() -> None:
    """Same threshold → identical claim text — cache key stays stable."""
    a = _substantivity_claim_for(2)
    b = _substantivity_claim_for(2)
    assert a == b
    # And the threshold is in the claim, so a different threshold
    # produces a different cache key.
    assert _substantivity_claim_for(2) != _substantivity_claim_for(4)


def test_substantivity_record_has_yes_for_passing_count() -> None:
    """Synthetic record carries the verdict + reasoning the report needs."""
    rec = _make_substantivity_record(5)
    assert rec.verdict == "YES"
    assert rec.elapsed == 0.0  # no LLM call
    assert rec.cost_usd == 0.0
    assert "5 turn" in rec.reasoning


def test_substantivity_record_has_no_for_failing_count() -> None:
    """A failing turn count produces a NO verdict + failure reasoning."""
    rec = _make_substantivity_record(0)
    assert rec.verdict == "NO"
    assert "0 turn" in rec.reasoning


def test_substantivity_cache_key_distinct_from_others() -> None:
    """The cache key doesn't collide with the other smoke gates."""
    assert _SUBSTANTIVITY_CACHE_KEY != "__goal_pursued__"
    assert _SUBSTANTIVITY_CACHE_KEY != "__persona_adoption__"
    # And it follows the reserved-name convention (leading + trailing
    # double-underscore) so test functions can't accidentally use it.
    assert _SUBSTANTIVITY_CACHE_KEY.startswith("__")
    assert _SUBSTANTIVITY_CACHE_KEY.endswith("__")


def test_substantivity_record_appears_in_report_table(tmp_path: Path) -> None:
    """End-to-end: a substantivity record renders as a smoke-gate row."""
    # Seed all three gate records on disk; the loader picks up
    # __substantivity__ from the cache like any other gate.
    mod_dir = tmp_path / "x/test_x"
    mod_dir.mkdir(parents=True)
    (mod_dir / "judge_records.json").write_text(json.dumps({
        "schema_version": 1, "conversation_fingerprint": "fp",
        "tests": {
            "__persona_adoption__": [{
                "claim": "...", "verdict": "YES", "reasoning": "x",
                "elapsed": 1.0, "cost_usd": 0.01, "cached": False,
            }],
            "__substantivity__": [{
                "claim": "...", "verdict": "YES",
                "reasoning": "Conversation had 5 turn(s); minimum required: 2.",
                "elapsed": 0.0, "cost_usd": 0.0, "cached": False,
            }],
            "__goal_pursued__": [{
                "claim": "...", "verdict": "YES", "reasoning": "x",
                "elapsed": 5.0, "cost_usd": 0.02, "cached": False,
            }],
        },
    }))
    test_outcomes = {
        "evals/cases/x/test_x.py::test_a": {
            "outcome": "passed", "duration": 0.1, "error": None,
        },
    }
    write_summary(tmp_path, test_outcomes, {})
    text = (tmp_path / "summary.md").read_text(encoding="utf-8")
    # All three gate labels appear, in run order.
    persona_idx = text.find("persona-adoption check")
    substantivity_idx = text.find("substantivity check")
    smoke_idx = text.find("goal-pursued check")
    assert persona_idx >= 0
    assert substantivity_idx >= 0
    assert smoke_idx >= 0
    assert persona_idx < substantivity_idx < smoke_idx, (
        "gates must render in run order: persona-adoption (turn 1), "
        "then substantivity (instant post-conversation check), "
        "then smoke (LLM judge call)"
    )
