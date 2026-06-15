"""
agent.py -- LangGraph ReAct agent powered by Google Gemini.
Uses LangGraph prebuilt create_react_agent (LangChain compatible).
"""

import os
import logging
from typing import List, Dict, Tuple, Optional
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-lite")
MAX_HISTORY  = int(os.getenv("MAX_HISTORY", "10"))
MAX_RETRIES  = 3
BASE_DELAY   = 5

SYSTEM_PROMPT = """You are CampusAI, a knowledgeable and friendly Universal Campus Information Assistant for Indian colleges and universities.

You help students, freshers, faculty, and visitors with:
- Academic regulations (attendance, exams, CGPA, grading, backlogs, CBCS)
- Campus facilities (library, hostel, canteen, sports, medical center, labs)
- Administrative procedures (admissions, fees, certificates, scholarships)
- Events and calendar (cultural fests, technical fests, sports meets, holidays)
- Clubs and activities (technical, cultural, sports, NSS, NCC, student council)
- Contact directory (faculty, HODs, deans, placement cell, wardens)
- Placement and career guidance (campus drives, internships, higher studies)
- College types (Engineering, Medical, Arts & Science, Management, Law, etc.)

Guidelines:
- Keep responses concise, direct, and token-efficient.
- DO NOT manually write or print source filenames in your response; a separate programmatic post-processor will automatically add them at the bottom. Focus solely on answering the question accurately.
- Be accurate and specific with concrete details (timings, percentages, procedures).
- Use Indian academic terminology (CGPA, arrear, bonafide certificate, lateral entry).
- Always guide the user on what to do next.
- Cover ALL Indian college types, not just one institution.
- Use bullet points and bold text for clarity.
- Be friendly and empathetic — like a helpful senior student.
- For institution-specific queries, advise checking the college's official website.

"""


def create_agent(tools: Optional[list] = None):
    """Create a LangGraph ReAct agent with Gemini and campus tools."""
    from langgraph.prebuilt import create_react_agent
    from langchain_groq import ChatGroq

    if tools is None:
        from core.tools import get_all_tools
        tools = get_all_tools()

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.0,
        request_timeout=30,   # fail fast instead of hanging forever
    )

    # Support both old ('prompt') and new ('state_modifier') LangGraph API
    try:
        agent = create_react_agent(
            model=llm,
            tools=tools,
            state_modifier=SYSTEM_PROMPT,
        )
    except TypeError:
        agent = create_react_agent(
            model=llm,
            tools=tools,
            prompt=SYSTEM_PROMPT,
        )

    return agent


def _extract_text(content) -> str:
    """
    Gemini 2.5 Flash returns content as either:
      - A plain string, or
      - A list of dicts: [{'type': 'text', 'text': '...', 'extras': {...}}, ...]
    This helper normalises both into a plain string.
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif isinstance(block, str):
                parts.append(block)
        return "\n".join(parts).strip()
    return str(content)


class CampusChatbot:
    """High-level chatbot wrapper with conversation history."""

    def __init__(self):
        self._agent = None
        self._tools = None
        self.conversation_history: List[Dict[str, str]] = []

    def _ensure_initialized(self):
        if self._agent is None:
            logger.info("Initializing CampusAI agent (LangGraph + Gemini)...")
            from core.tools import get_all_tools
            self._tools = get_all_tools()
            self._agent = create_agent(self._tools)
            logger.info("CampusAI agent ready.")

    def chat(self, user_message: str, session_id: str = "default") -> Tuple[str, str, int]:
        """Process a user message. Returns (response, tool_used, response_time_ms)."""
        import time
        from langchain_core.messages import HumanMessage, AIMessage

        self._ensure_initialized()
        start_time = time.time()

        # Build LangGraph message list (includes history)
        messages = []
        for msg in self.conversation_history[-6:]:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
        messages.append(HumanMessage(content=user_message))

        response = ""
        tool_used = ""
        last_error = None

        for attempt in range(MAX_RETRIES):
            try:
                result = self._agent.invoke({"messages": messages})

                # Extract final AI response
                all_messages = result.get("messages", [])

                for msg in reversed(all_messages):
                    if hasattr(msg, "content") and msg.content and msg.__class__.__name__ == "AIMessage":
                        response = _extract_text(msg.content)
                        break

                # Extract tool name from ToolMessages
                for msg in all_messages:
                    if msg.__class__.__name__ == "ToolMessage":
                        tool_used = getattr(msg, "name", "")
                        break

                # Algorithmic source citation extraction
                sources = set()
                import re
                
                # Mapping of raw files to premium verified publication names
                SOURCE_NAME_MAP = {
                    "iiith.json": "IIIT Hyderabad Placement Report & Admissions Brochure 2025",
                    "iith.json": "IIT Hyderabad Placement Report & Student Handbook 2025",
                    "strategic_report.md": "IIIT-H Academic & Strategic Report",
                    "other_institutions.json": "NALSAR & NIMS Institutional Placement Records 2025",
                    "nirf_rankings.json": "NIRF Submission 2025",
                    "facilities.json": "Campus Infrastructure & Facilities Guide",
                    "general_info.json": "Universal Academic Regulations Guide",
                    "clubs_activities.json": "Student Clubs & Activity Charter",
                    "procedures.json": "Administrative Procedures Manual",
                    "college_types.json": "UGC College Classification Guidelines",
                    "directory.csv": "Verified Faculty & Staff Directory",
                    "academic_calendar.json": "Official Academic Calendar 2025-26"
                }

                for msg in all_messages:
                    if msg.__class__.__name__ == "ToolMessage" and msg.content:
                        content_str = str(msg.content)
                        found = re.findall(r'\[Source:\s*([^\]]+)\]', content_str)
                        for f in found:
                            clean_name = f.strip().lower()
                            if clean_name in SOURCE_NAME_MAP:
                                clean_name = SOURCE_NAME_MAP[clean_name]
                            else:
                                # Fallback cleaning if not mapped
                                clean_name = f.strip().replace('.pdf', '').replace('.txt', '').replace('.json', '').replace('.csv', '').replace('.md', '').replace('_', ' ').replace('-', ' ').title()
                            sources.add(clean_name)
                        
                        # Fallback for structured tools
                        t_name = getattr(msg, "name", "")
                        if t_name == "get_campus_events":
                            sources.add("Official Academic Calendar 2025-26")
                        elif t_name == "search_contacts":
                            sources.add("Verified Faculty & Staff Directory")
                        elif t_name == "get_facility_info":
                            sources.add("Campus Facilities Guide")
                        elif t_name == "get_clubs_activities":
                            sources.add("Student Activity & Clubs Charter")

                # Clean up any LLM-generated sources sections first
                response = re.sub(r'\n+(?:\*\*|)?Sources?(?:\*\*|)?:\s*.*$', '', response, flags=re.IGNORECASE | re.DOTALL)
                
                # Append formatted verified sources list
                if sources:
                    sources_list = "\n".join(f"• {s}" for s in sorted(sources))
                    response += f"\n\nSource:\n{sources_list}"

                last_error = None
                break  # Success — exit retry loop

            except Exception as e:
                last_error = e
                err_str = str(e)

                # Detect quota / overload errors and retry
                is_retryable = (
                    "429" in err_str or
                    "RESOURCE_EXHAUSTED" in err_str or
                    "503" in err_str or
                    "UNAVAILABLE" in err_str
                )

                if is_retryable and attempt < MAX_RETRIES - 1:
                    wait_sec = BASE_DELAY * (2 ** attempt)  # 5s, 10s, 20s
                    logger.warning(f"API error (attempt {attempt+1}/{MAX_RETRIES}): {err_str[:80]} — retrying in {wait_sec}s")
                    time.sleep(wait_sec)
                    continue
                else:
                    logger.error(f"Agent error: {e}", exc_info=True)
                    break

        if last_error:
            err_str = str(last_error)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                response = (
                    "⚠️ **API Quota Reached** — The API daily limit has been hit.\n\n"
                    "**How to fix:**\n"
                    "1. Wait a few minutes and try again (limits reset frequently)\n"
                    "2. Check your AI provider's dashboard for quota limits.\n"
                )
            elif "503" in err_str or "UNAVAILABLE" in err_str:
                response = (
                    "⚠️ **Service Unavailable** — The AI service is currently overloaded.\n"
                    "Please wait a moment and try again."
                )
            elif "tool_use_failed" in err_str and "failed_generation" in err_str:
                import re
                match = re.search(r"'failed_generation': '(\{.*?\})'", err_str)
                if match:
                    try:
                        import json
                        raw_json = match.group(1).replace("\\\"", "\"").replace("\\'", "'")
                        args = json.loads(raw_json)
                        if "institution" in args and "topic" in args:
                            from core.tools import InstitutionDataTool
                            fallback_res = InstitutionDataTool()._run(institution=args["institution"], topic=args["topic"])
                        elif "query" in args:
                            from core.tools import CampusKnowledgeTool
                            fallback_res = CampusKnowledgeTool()._run(query=args["query"])
                        else:
                            fallback_res = f"Data could not be formatted properly. Raw arguments: {args}"
                        
                        response = f"*(Note: The AI experienced a tool formatting glitch, so I fetched the data manually for you.)*\n\n{fallback_res}"
                        tool_used = "manual_fallback"
                    except Exception as parse_e:
                        response = f"⚠️ **Tool Formatting Error** — The AI failed to format the tool request properly, and the fallback parser also failed. Please rephrase your question."
            else:
                response = f"⚠️ **Error**: {err_str[:200]}\n\nPlease check your API key in `.env` and try again."
            tool_used = "error"

        response_time_ms = int((time.time() - start_time) * 1000)

        # Update history
        self.conversation_history.append({"role": "user",      "content": user_message})
        self.conversation_history.append({"role": "assistant",  "content": response})
        if len(self.conversation_history) > MAX_HISTORY * 2:
            self.conversation_history = self.conversation_history[-(MAX_HISTORY * 2):]

        return response, tool_used, response_time_ms

    def clear_history(self):
        self.conversation_history = []

    @property
    def is_ready(self) -> bool:
        return self._agent is not None


def categorize_query(query: str) -> str:
    """Categorize a user query for analytics."""
    q = query.lower()
    categories = {
        "academic":   ["exam", "cgpa", "attendance", "grade", "backlog", "arrear",
                       "result", "internal", "semester", "credit", "gpa"],
        "facility":   ["library", "hostel", "canteen", "sports", "medical", "lab",
                       "wifi", "transport", "bus", "bank", "atm"],
        "placement":  ["placement", "job", "recruit", "internship", "company",
                       "package", "salary", "career", "drive"],
        "admission":  ["admission", "fee", "document", "join", "enroll",
                       "apply", "scholarship", "neet", "jee", "clat"],
        "clubs":      ["club", "fest", "event", "nss", "ncc", "cultural",
                       "technical", "society", "committee"],
        "contact":    ["contact", "email", "phone", "hod", "dean", "warden",
                       "librarian", "faculty", "professor"],
        "procedure":  ["certificate", "bonafide", "tc", "migration",
                       "no dues", "leave", "application", "form"],
    }
    for category, keywords in categories.items():
        if any(kw in q for kw in keywords):
            return category
    return "general"
