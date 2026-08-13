"""
test_database.py — Tests for core/database.py functions using temp file SQLite.
"""

import sqlite3
import os

import pytest


# ── initialize_database ───────────────────────────────────────────────────────

class TestInitializeDatabase:
    def test_idempotent(self, tmp_path):
        """Test that initialize_database can be called multiple times without error."""
        import core.database as db_mod
        db_file = str(tmp_path / "idempotent_test.db")
        original_path = db_mod.DB_PATH
        db_mod.DB_PATH = db_file
        try:
            db_mod.initialize_database()
            db_mod.initialize_database()  # Should not raise
        finally:
            db_mod.DB_PATH = original_path


# ── log_query ─────────────────────────────────────────────────────────────────

class TestLogQuery:
    def test_returns_row_id(self):
        from core.database import log_query
        row_id = log_query(
            session_id="test-session",
            user_query="What is CGPA?",
            bot_response="CGPA is cumulative grade point average.",
            tool_used="campus_knowledge_search",
            category="academic",
            response_time_ms=150,
        )
        assert isinstance(row_id, int)
        assert row_id > 0

    def test_stores_all_fields(self):
        from core.database import log_query, get_connection
        row_id = log_query(
            session_id="s1",
            user_query="Hello",
            bot_response="Hi there",
            tool_used="direct_rag",
            category="general",
            response_time_ms=100,
        )
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM query_history WHERE id = ?", (row_id,))
        row = cursor.fetchone()
        conn.close()
        assert row["session_id"] == "s1"
        assert row["user_query"] == "Hello"
        assert row["bot_response"] == "Hi there"
        assert row["tool_used"] == "direct_rag"
        assert row["category"] == "general"
        assert row["response_time_ms"] == 100

    def test_multiple_queries(self):
        from core.database import log_query
        id1 = log_query("s1", "q1", "a1")
        id2 = log_query("s2", "q2", "a2")
        assert id2 > id1


# ── log_feedback ──────────────────────────────────────────────────────────────

class TestLogFeedback:
    def test_stores_feedback(self):
        from core.database import log_query, log_feedback, get_connection
        query_id = log_query("s1", "q1", "a1")
        log_feedback(query_id, rating=1, feedback_text="Great!")

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM feedback WHERE query_id = ?", (query_id,))
        row = cursor.fetchone()
        conn.close()
        assert row is not None
        assert row["rating"] == 1
        assert row["feedback_text"] == "Great!"


# ── get_recent_queries ────────────────────────────────────────────────────────

class TestGetRecentQueries:
    def test_returns_most_recent(self):
        from core.database import log_query, get_recent_queries
        log_query("s1", "first", "a1")
        log_query("s2", "second", "a2")
        log_query("s3", "third", "a3")

        results = get_recent_queries(limit=2)
        assert len(results) == 2
        assert results[0]["user_query"] == "third"
        assert results[1]["user_query"] == "second"

    def test_empty_when_no_data(self):
        from core.database import get_recent_queries
        results = get_recent_queries()
        assert results == []


# ── get_analytics_summary ─────────────────────────────────────────────────────

class TestGetAnalyticsSummary:
    def test_empty_database(self):
        from core.database import get_analytics_summary
        summary = get_analytics_summary()
        assert summary["total_queries"] == 0
        assert summary["today_queries"] == 0
        assert summary["positive_feedback"] == 0
        assert summary["negative_feedback"] == 0

    def test_with_data(self):
        from core.database import log_query, log_feedback, get_analytics_summary
        q1 = log_query("s1", "q1", "a1", category="academic", response_time_ms=100)
        q2 = log_query("s2", "q2", "a2", category="facility", response_time_ms=200)
        log_feedback(q1, rating=1)
        log_feedback(q2, rating=-1)

        summary = get_analytics_summary()
        assert summary["total_queries"] == 2
        assert summary["positive_feedback"] == 1
        assert summary["negative_feedback"] == 1
        assert summary["satisfaction_rate"] == 50.0


# ── get_popular_queries ───────────────────────────────────────────────────────

class TestGetPopularQueries:
    def test_frequency_ordering(self):
        from core.database import log_query, get_popular_queries
        log_query("s1", "What is CGPA?", "a1")
        log_query("s2", "What is CGPA?", "a2")
        log_query("s3", "What is CGPA?", "a3")
        log_query("s4", "Hello", "a4")

        results = get_popular_queries(limit=2)
        assert results[0]["user_query"] == "What is CGPA?"
        assert results[0]["frequency"] == 3


# ── get_cached_response / set_cached_response ────────────────────────────────

class TestCache:
    def test_set_and_get(self):
        from core.database import set_cached_response, get_cached_response
        set_cached_response("What is CGPA?", "CGPA stands for...")
        result = get_cached_response("What is CGPA?")
        assert result == "CGPA stands for..."

    def test_cache_miss(self):
        from core.database import get_cached_response
        result = get_cached_response("nonexistent query xyz")
        assert result is None

    def test_hit_count_increments(self):
        from core.database import set_cached_response, get_cached_response, get_connection
        set_cached_response("test query", "test response")
        get_cached_response("test query")
        get_cached_response("test query")

        conn = get_connection()
        cursor = conn.cursor()
        import hashlib
        h = hashlib.sha256("test query".encode("utf-8")).hexdigest()
        cursor.execute("SELECT hit_count FROM cached_responses WHERE query_hash = ?", (h,))
        row = cursor.fetchone()
        conn.close()
        assert row["hit_count"] == 2

    def test_case_insensitive(self):
        from core.database import set_cached_response, get_cached_response
        set_cached_response("What is CGPA?", "answer")
        result = get_cached_response("what is cgpa?")
        assert result == "answer"
