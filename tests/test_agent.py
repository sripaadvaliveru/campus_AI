"""
test_agent.py — Tests for pure functions in core/agent.py.
"""

import pytest


# ── _extract_text ─────────────────────────────────────────────────────────────

class TestExtractText:
    def test_plain_string(self):
        from core.agent import _extract_text
        assert _extract_text("hello") == "hello"

    def test_none_returns_empty(self):
        from core.agent import _extract_text
        assert _extract_text(None) == ""

    def test_list_of_text_blocks(self):
        from core.agent import _extract_text
        content = [
            {"type": "text", "text": "hello"},
            {"type": "text", "text": "world"},
        ]
        assert _extract_text(content) == "hello\nworld"

    def test_list_with_string_items(self):
        from core.agent import _extract_text
        content = ["hello", "world"]
        assert _extract_text(content) == "hello\nworld"

    def test_mixed_list(self):
        from core.agent import _extract_text
        content = [
            {"type": "text", "text": "hello"},
            "world",
            {"type": "image", "url": "ignored"},
        ]
        assert _extract_text(content) == "hello\nworld"

    def test_non_text_dict_blocks_ignored(self):
        from core.agent import _extract_text
        content = [{"type": "image", "url": "test.png"}]
        assert _extract_text(content) == ""

    def test_integer_converted_to_string(self):
        from core.agent import _extract_text
        assert _extract_text(42) == "42"

    def test_empty_list(self):
        from core.agent import _extract_text
        assert _extract_text([]) == ""


# ── _retryable_error ──────────────────────────────────────────────────────────

class TestRetryableError:
    def test_429_is_retryable(self):
        from core.agent import _retryable_error
        assert _retryable_error("Error 429: rate limit") is True

    def test_resource_exhausted_is_retryable(self):
        from core.agent import _retryable_error
        assert _retryable_error("RESOURCE_EXHAUSTED") is True

    def test_503_is_retryable(self):
        from core.agent import _retryable_error
        assert _retryable_error("503 Service Unavailable") is True

    def test_unavailable_is_retryable(self):
        from core.agent import _retryable_error
        assert _retryable_error("UNAVAILABLE") is True

    def test_insufficient_quota_not_retryable(self):
        from core.agent import _retryable_error
        assert _retryable_error("insufficient_quota") is False

    def test_random_error_not_retryable(self):
        from core.agent import _retryable_error
        assert _retryable_error("Invalid API key") is False

    def test_empty_string_not_retryable(self):
        from core.agent import _retryable_error
        assert _retryable_error("") is False


# ── categorize_query ──────────────────────────────────────────────────────────

class TestCategorizeQuery:
    def test_academic_category(self):
        from core.agent import categorize_query
        assert categorize_query("What is the CGPA formula?") == "academic"

    def test_facility_category(self):
        from core.agent import categorize_query
        assert categorize_query("Tell me about the library") == "facility"

    def test_placement_category(self):
        from core.agent import categorize_query
        assert categorize_query("What are the placement statistics?") == "placement"

    def test_admission_category(self):
        from core.agent import categorize_query
        assert categorize_query("How to apply for admission?") == "admission"

    def test_clubs_category(self):
        from core.agent import categorize_query
        assert categorize_query("Tell me about the coding club") == "clubs"

    def test_contact_category(self):
        from core.agent import categorize_query
        assert categorize_query("Give me the HOD email") == "contact"

    def test_procedure_category(self):
        from core.agent import categorize_query
        assert categorize_query("How to get bonafide certificate?") == "procedure"

    def test_general_fallback(self):
        from core.agent import categorize_query
        assert categorize_query("Hello there") == "general"

    def test_case_insensitive(self):
        from core.agent import categorize_query
        assert categorize_query("WHAT IS CGPA") == "academic"


# ── CampusChatbot ─────────────────────────────────────────────────────────────

class TestCampusChatbot:
    def test_initial_state(self):
        from core.agent import CampusChatbot
        bot = CampusChatbot()
        assert bot._agent is None
        assert bot._llm is None
        assert bot._histories == {}

    def test_history_per_session(self):
        from core.agent import CampusChatbot
        bot = CampusChatbot()
        h1 = bot._history("session1")
        h2 = bot._history("session2")
        assert h1 is not h2
        assert h1 == []
        assert h2 == []

    def test_history_mutable(self):
        from core.agent import CampusChatbot
        bot = CampusChatbot()
        h = bot._history("session1")
        h.append({"role": "user", "content": "hello"})
        assert len(bot._history("session1")) == 1

    def test_clear_history(self):
        from core.agent import CampusChatbot
        bot = CampusChatbot()
        bot._history("session1").append({"role": "user", "content": "hello"})
        bot.clear_history("session1")
        assert bot._history("session1") == []

    def test_is_ready_false_initially(self):
        from core.agent import CampusChatbot
        bot = CampusChatbot()
        assert bot.is_ready is False
