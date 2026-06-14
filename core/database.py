"""
database.py — SQLite database for logging queries, feedback, and analytics.
"""

import sqlite3
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

_DEFAULT_DB = str(Path(__file__).parent.parent / "campus.db")
DB_PATH = os.getenv("DB_PATH", _DEFAULT_DB)


def get_connection() -> sqlite3.Connection:
    """Get a SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database() -> None:
    """Create all required tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS query_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            user_query TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            tool_used TEXT,
            category TEXT,
            timestamp TEXT NOT NULL,
            response_time_ms INTEGER
        );

        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_id INTEGER REFERENCES query_history(id),
            rating INTEGER CHECK(rating IN (1, -1)),
            feedback_text TEXT,
            timestamp TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            total_queries INTEGER DEFAULT 0,
            positive_feedback INTEGER DEFAULT 0,
            negative_feedback INTEGER DEFAULT 0,
            top_categories TEXT,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS cached_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_hash TEXT UNIQUE NOT NULL,
            query TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TEXT NOT NULL,
            hit_count INTEGER DEFAULT 0
        );
    """)

    conn.commit()
    conn.close()
    logger.info("Database initialized successfully.")


def log_query(
    session_id: str,
    user_query: str,
    bot_response: str,
    tool_used: str = "",
    category: str = "general",
    response_time_ms: int = 0
) -> int:
    """Log a query-response pair to the database. Returns the inserted row ID."""
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO query_history
            (session_id, user_query, bot_response, tool_used, category, timestamp, response_time_ms)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (session_id, user_query, bot_response, tool_used, category, timestamp, response_time_ms))

    row_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return row_id


def log_feedback(query_id: int, rating: int, feedback_text: str = "") -> None:
    """Log user feedback (1 = thumbs up, -1 = thumbs down) for a query."""
    conn = get_connection()
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO feedback (query_id, rating, feedback_text, timestamp)
        VALUES (?, ?, ?, ?)
    """, (query_id, rating, feedback_text, timestamp))

    conn.commit()
    conn.close()


def get_recent_queries(limit: int = 20) -> List[Dict[str, Any]]:
    """Return the most recent queries."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, user_query, bot_response, category, timestamp, response_time_ms
        FROM query_history
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))

    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_analytics_summary() -> Dict[str, Any]:
    """Return analytics summary for the dashboard."""
    conn = get_connection()
    cursor = conn.cursor()

    # Total queries
    cursor.execute("SELECT COUNT(*) as total FROM query_history")
    total = cursor.fetchone()["total"]

    # Queries today
    today = datetime.now().date().isoformat()
    cursor.execute("SELECT COUNT(*) as today FROM query_history WHERE DATE(timestamp) = ?", (today,))
    today_count = cursor.fetchone()["today"]

    # Feedback stats
    cursor.execute("SELECT rating, COUNT(*) as cnt FROM feedback GROUP BY rating")
    feedback_rows = cursor.fetchall()
    positive = sum(r["cnt"] for r in feedback_rows if r["rating"] == 1)
    negative = sum(r["cnt"] for r in feedback_rows if r["rating"] == -1)

    # Top categories
    cursor.execute("""
        SELECT category, COUNT(*) as cnt
        FROM query_history
        GROUP BY category
        ORDER BY cnt DESC
        LIMIT 5
    """)
    top_categories = [{"category": r["category"], "count": r["cnt"]} for r in cursor.fetchall()]

    # Queries by day (last 7 days)
    cursor.execute("""
        SELECT DATE(timestamp) as day, COUNT(*) as cnt
        FROM query_history
        WHERE DATE(timestamp) >= DATE('now', '-7 days')
        GROUP BY day
        ORDER BY day
    """)
    daily_counts = [{"day": r["day"], "count": r["cnt"]} for r in cursor.fetchall()]

    # Average response time
    cursor.execute("SELECT AVG(response_time_ms) as avg_rt FROM query_history WHERE response_time_ms > 0")
    avg_rt_row = cursor.fetchone()
    avg_rt = round(avg_rt_row["avg_rt"] or 0, 0)

    conn.close()

    return {
        "total_queries": total,
        "today_queries": today_count,
        "positive_feedback": positive,
        "negative_feedback": negative,
        "satisfaction_rate": round((positive / max(positive + negative, 1)) * 100, 1),
        "top_categories": top_categories,
        "daily_counts": daily_counts,
        "avg_response_time_ms": avg_rt,
    }


def get_popular_queries(limit: int = 10) -> List[Dict[str, Any]]:
    """Return most common query keywords."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_query, COUNT(*) as frequency
        FROM query_history
        GROUP BY LOWER(TRIM(user_query))
        ORDER BY frequency DESC
        LIMIT ?
    """, (limit,))

    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows
