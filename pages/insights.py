"""
insights.py — Analytics and usage statistics page.
Extracted from app.py lines 2462-2628.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from core.config import COLLEGE_MAP


def render():
    """Render the Insights (Analytics) page."""
    active_college_id = st.session_state.get("selected_college") or "general"
    active_c = COLLEGE_MAP.get(active_college_id, {})

    st.markdown(f"""
    <div class="campus-header" style="background-color: #0F172A !important; background-image: radial-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px) !important; background-size: 24px 24px !important; color: #F8FAFC !important; border-color: #1E293B !important; padding: 2.25rem !important; border-radius: 16px !important; box-shadow: 0 10px 30px rgba(0,0,0,0.2) !important;">
        <div class="section-label-badge">
            <span class="section-label-dot"></span>
            <span class="section-label-text">{active_c.get('short','CampusAI')}</span>
        </div>
        <h1 style="font-size:2.0rem;font-weight:400;font-family:'Calistoga',serif !important;color:#FFFFFF !important;margin:0 0 0.75rem 0;letter-spacing:-0.01em;">System Analytics & Usage</h1>
        <p style="color:#94A3B8 !important;margin:0;">Usage statistics, popular queries, and performance metrics for CampusAI.</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        from core.database import get_analytics_summary, get_recent_queries, get_popular_queries
        stats = get_analytics_summary()
        recent = get_recent_queries(limit=10)
        popular = get_popular_queries(limit=8)
    except Exception as e:
        st.error(f"Analytics unavailable: {e}")
        st.stop()

    # Summary Metrics
    c1, c2, c3, c4, c5 = st.columns(5)
    metrics = [
        (c1, stats.get("total_queries", 0), "Total Queries", "\U0001f4ac"),
        (c2, stats.get("today_queries", 0), "Today", "\U0001f4c5"),
        (c3, stats.get("positive_feedback", 0), "\U0001f44d Helpful", "\u2705"),
        (c4, stats.get("negative_feedback", 0), "\U0001f44e Not Helpful", "\u274c"),
        (c5, f"{stats.get('satisfaction_rate', 0)}%", "Satisfaction", "\u2b50"),
    ]
    for col, val, label, icon in metrics:
        col.markdown(f"""
        <div class="metric-card">
            <div style="font-size:1.2rem">{icon}</div>
            <div class="metric-value" style="font-size:1.5rem">{val}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts
    col_left, col_right = st.columns(2)

    dark_mode = st.session_state.get("dark_mode", False)
    plotly_template = "plotly_dark" if dark_mode else "plotly_white"
    plotly_text = "#f0f4ff" if dark_mode else "#475569"
    plotly_grid = "rgba(255,255,255,0.08)" if dark_mode else "#f1f5f9"

    with col_left:
        st.markdown('<div class="section-title">QUERIES PER DAY (LAST 7 DAYS)</div>', unsafe_allow_html=True)
        daily = stats.get("daily_counts", [])
        if daily:
            df_daily = pd.DataFrame(daily)
            fig = px.bar(df_daily, x="day", y="count", color_discrete_sequence=["#6366f1"], template=plotly_template)
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
                font=dict(color=plotly_text, family="Outfit"), xaxis_title="", yaxis_title="Queries",
            )
            fig.update_xaxes(showgrid=False, color=plotly_text, linecolor=plotly_grid)
            fig.update_yaxes(showgrid=True, gridcolor=plotly_grid, color=plotly_text, linecolor=plotly_grid)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No query data yet. Start chatting to see analytics!")

    with col_right:
        st.markdown('<div class="section-title">QUERIES BY CATEGORY</div>', unsafe_allow_html=True)
        top_cats = stats.get("top_categories", [])
        if top_cats:
            df_cats = pd.DataFrame(top_cats)
            colors = ["#6366f1", "#8b5cf6", "#06b6d4", "#10b981", "#f59e0b"]
            fig2 = px.pie(df_cats, names="category", values="count", color_discrete_sequence=colors, template=plotly_template, hole=0.45)
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10),
                font=dict(color=plotly_text, family="Outfit"),
                legend=dict(font=dict(color=plotly_text)),
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No category data yet.")

    # Popular & Recent Queries
    st.divider()
    col_pop, col_recent = st.columns(2)

    with col_pop:
        st.markdown('<div class="section-title">POPULAR QUERIES</div>', unsafe_allow_html=True)
        if popular:
            for i, pq in enumerate(popular):
                freq = pq.get("frequency", 1)
                query_text = pq.get("user_query", "")[:60]
                bar_width = int((freq / max(p.get("frequency", 1) for p in popular)) * 100)
                st.markdown(f"""
                <div style="margin-bottom:0.75rem">
                    <div style="display:flex;justify-content:space-between;margin-bottom:0.2rem">
                        <span style="font-size:0.85rem;color:var(--text-primary)">{i+1}. {query_text}</span>
                        <span style="font-size:0.75rem;color:var(--accent);font-weight:600">{freq}x</span>
                    </div>
                    <div style="background:var(--border);height:6px;border-radius:3px !important;overflow:hidden;">
                        <div style="background:var(--accent);width:{bar_width}%;height:100%;border-radius:3px !important;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No popular queries yet.")

    with col_recent:
        st.markdown('<div class="section-title">RECENT QUERIES</div>', unsafe_allow_html=True)
        if recent:
            for q in recent[:8]:
                timestamp = (q.get("timestamp") or "")[:16].replace("T", " ")
                category = q.get("category", "general")
                badge_class = {
                    "academic": "badge-academic", "facility": "badge-sports",
                    "placement": "badge-placement", "clubs": "badge-cultural",
                    "contact": "badge-exam",
                }.get(category, "badge-academic")

                st.markdown(f"""
                <div class="contact-card" style="margin-bottom:0.5rem">
                    <div style="display:flex;align-items:center;gap:0.5rem;flex-wrap:wrap">
                        <span style="font-size:0.85rem;color:var(--text-primary)">{q.get('user_query','')[:60]}{('...' if len(q.get('user_query','')) > 60 else '')}</span>
                        <span class="event-badge {badge_class}">{category}</span>
                    </div>
                    <div style="font-size:0.72rem;color:var(--text-muted);margin-top:0.3rem">{timestamp}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recent queries. Start chatting!")

    # Performance footer
    st.divider()
    avg_rt = stats.get("avg_response_time_ms", 0)
    st.markdown(f"""
    <div style="text-align:center;padding:1.25rem;color:var(--text-secondary);font-size:0.85rem;
                background:var(--bg-surface);border:2px solid var(--border)">
        \u26a1 Avg Response: <strong style="color:var(--accent)">{int(avg_rt)}ms</strong> &nbsp;\u00b7&nbsp;
        \U0001f916 Model: <strong style="color:var(--accent)">gpt-4o-mini</strong> &nbsp;\u00b7&nbsp;
        \U0001f4be Session: <strong style="color:var(--accent);font-family:'JetBrains Mono',monospace">{st.session_state.session_id[:8]}...</strong>
    </div>
    """, unsafe_allow_html=True)
