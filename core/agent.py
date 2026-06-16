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


from typing import Tuple, Any

def create_llm_and_agent(tools: Optional[list] = None) -> Tuple[Any, Any]:
    """Create the LLM instance and the LangGraph agent."""
    from langgraph.prebuilt import create_react_agent

    if tools is None:
        from core.tools import get_all_tools
        tools = get_all_tools()

    # Determine provider
    provider = os.getenv("LLM_PROVIDER", "").lower().strip()
    google_key = os.getenv("GOOGLE_API_KEY", "").strip()
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()

    # Determine default provider if not configured
    if not provider:
        if google_key and google_key != "your_google_gemini_api_key_here":
            provider = "gemini"
        elif openai_key and openai_key != "your_openai_api_key_here":
            provider = "openai"
        else:
            provider = "gemini" # Fallback default

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        logger.info("Initializing Agent with OpenAI (gpt-4o-mini)")
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            api_key=openai_key,
            temperature=0.0,
            request_timeout=15,   # fail fast instead of hanging forever
        )
    else:
        from langchain_google_genai import ChatGoogleGenerativeAI
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        logger.info(f"Initializing Agent with Google GenAI ({model_name})")
        llm = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=google_key,
            temperature=0.0,
            request_timeout=15,
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

    return llm, agent


def create_agent(tools: Optional[list] = None):
    """Create a LangGraph ReAct agent (for backward compatibility)."""
    llm, agent = create_llm_and_agent(tools)
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
        self._llm = None
        self._tools = None
        self.conversation_history: List[Dict[str, str]] = []

    def _ensure_initialized(self):
        if self._agent is None:
            logger.info("Initializing CampusAI agent (LangGraph + Gemini)...")
            from core.tools import get_all_tools
            self._tools = get_all_tools()
            self._llm, self._agent = create_llm_and_agent(self._tools)
            logger.info("CampusAI agent ready.")

    def _direct_rag_chat(self, user_message: str, history: List[Dict[str, str]]) -> Tuple[str, str]:
        """Runs RAG in a single LLM call for ultra-low latency."""
        import re
        from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
        
        context = ""
        sources = set()
        tool_used = "direct_rag"
        
        # Simple keywords classification
        query_lower = user_message.lower()
        
        # Check contact directory keywords
        if any(w in query_lower for w in ["contact", "phone", "email", "number", "faculty", "professor", "hod", "dean", "warden", "office", "directory"]):
            from core.tools import ContactDirectoryTool
            try:
                tool = ContactDirectoryTool()
                context = tool._run(user_message)
                sources.add("Verified Faculty & Staff Directory")
                tool_used = "search_contacts"
            except Exception as e:
                logger.error(f"Direct contact lookup error: {e}")
                
        # Check calendar keywords
        elif any(w in query_lower for w in ["event", "calendar", "date", "holiday", "exam", "fest", "schedule", "admission date", "deadline"]):
            from core.tools import EventCalendarTool
            try:
                tool = EventCalendarTool()
                context = tool._run(user_message)
                sources.add("Official Academic Calendar 2025-26")
                tool_used = "get_campus_events"
            except Exception as e:
                logger.error(f"Direct calendar lookup error: {e}")
                
        # Default: Fall back to semantic vector store search
        if not context:
            try:
                from core.embeddings import get_vector_store
                vs = get_vector_store()
                if vs.is_ready:
                    # Search matching chunks
                    context = vs.get_relevant_context(user_message, top_k=3)
                    
                    # Extract sources from context string
                    found = re.findall(r'\[Source:\s*([^\]]+)\]', context)
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
                    for f in found:
                        clean_name = f.strip().lower()
                        if clean_name in SOURCE_NAME_MAP:
                            sources.add(SOURCE_NAME_MAP[clean_name])
                        else:
                            sources.add(f.strip().replace('.json','').replace('.csv','').replace('.md','').replace('_',' ').title())
                    tool_used = "campus_knowledge_search"
            except Exception as e:
                logger.error(f"Direct vector store lookup error: {e}")
        
        # Build Message list
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
        ]
        if context:
            messages.append(SystemMessage(content=f"Use this retrieved verified information to answer the question:\n{context}"))
            
        # Append conversation history
        for msg in history[-4:]:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
                
        # Append latest user message
        messages.append(HumanMessage(content=user_message))
        
        # Invoke LLM
        res = self._llm.invoke(messages)
        response = _extract_text(res.content)
        
        # Clean up any LLM-generated sources sections first
        response = re.sub(r'\n+(?:\*\*|)?Sources?(?:\*\*|)?:\s*.*$', '', response, flags=re.IGNORECASE | re.DOTALL)
        
        # Append formatted verified sources list
        if sources:
            sources_list = "\n".join(f"• {s}" for s in sorted(sources))
            response += f"\n\nSource:\n{sources_list}"
            
        return response, tool_used

    def chat(self, user_message: str, session_id: str = "default") -> Tuple[str, str, int]:
        """Process a user message. Returns (response, tool_used, response_time_ms)."""
        import time
        from langchain_core.messages import HumanMessage, AIMessage
        import re

        start_time = time.time()

        # Check cache first
        try:
            from core.database import get_cached_response
            cached = get_cached_response(user_message)
            if cached:
                logger.info(f"Cache hit for: {user_message[:50]}...")
                response_time_ms = int((time.time() - start_time) * 1000)
                # Update history
                self.conversation_history.append({"role": "user",      "content": user_message})
                self.conversation_history.append({"role": "assistant",  "content": cached})
                if len(self.conversation_history) > MAX_HISTORY * 2:
                    self.conversation_history = self.conversation_history[-(MAX_HISTORY * 2):]
                return cached, "cache", response_time_ms
        except Exception as e:
            logger.error(f"Error checking cache: {e}")

        self._ensure_initialized()

        response = ""
        tool_used = ""
        last_error = None

        # ── Step 1: Try single-step RAG path (takes ~1.2s) ──
        try:
            response, tool_used = self._direct_rag_chat(user_message, self.conversation_history)
        except Exception as e:
            logger.warning(f"Direct RAG path failed, falling back to agent loop: {e}")
            response = ""

        # ── Step 2: Fallback to multi-step agent loop if direct path failed ──
        if not response:
            messages = []
            for msg in self.conversation_history[-6:]:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                else:
                    messages.append(AIMessage(content=msg["content"]))
            messages.append(HumanMessage(content=user_message))

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

                    sources = set()
                    for msg in all_messages:
                        if msg.__class__.__name__ == "ToolMessage" and msg.content:
                            content_str = str(msg.content)
                            found = re.findall(r'\[Source:\s*([^\]]+)\]', content_str)
                            for f in found:
                                clean_name = f.strip().lower()
                                if clean_name in SOURCE_NAME_MAP:
                                    clean_name = SOURCE_NAME_MAP[clean_name]
                                else:
                                    clean_name = f.strip().replace('.pdf', '').replace('.txt', '').replace('.json', '').replace('.csv', '').replace('.md', '').replace('_', ' ').replace('-', ' ').title()
                                sources.add(clean_name)
                            
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
                else:
                    response = f"⚠️ **Error**: {err_str[:200]}\n\nPlease check your API key in `.env` and try again."
                tool_used = "error"

        response_time_ms = int((time.time() - start_time) * 1000)

        # Save to cache if successful
        if response and not response.startswith("⚠️") and tool_used != "error":
            try:
                from core.database import set_cached_response
                set_cached_response(user_message, response)
            except Exception as e:
                logger.error(f"Error writing to cache: {e}")

        # Update history
        self.conversation_history.append({"role": "user",      "content": user_message})
        self.conversation_history.append({"role": "assistant",  "content": response})
        if len(self.conversation_history) > MAX_HISTORY * 2:
            self.conversation_history = self.conversation_history[-(MAX_HISTORY * 2):]

        return response, tool_used, response_time_ms

    def stream_chat(self, user_message: str, session_id: str = "default"):
        """
        Generator method that yields chunks of the chatbot's response in real-time.
        Saves the final response to history and cache when generation completes.
        """
        import time
        import re
        from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

        start_time = time.time()

        # Check cache first
        try:
            from core.database import get_cached_response
            cached = get_cached_response(user_message)
            if cached:
                yield {"type": "tool", "name": "cache"}
                # Yield in small chunks to simulate typing
                words = cached.split(" ")
                for i, word in enumerate(words):
                    yield {"type": "content", "text": word + (" " if i < len(words) - 1 else "")}
                    time.sleep(0.01)
                yield {"type": "time", "ms": int((time.time() - start_time) * 1000), "full_text": cached}
                # Update history
                self.conversation_history.append({"role": "user",      "content": user_message})
                self.conversation_history.append({"role": "assistant",  "content": cached})
                if len(self.conversation_history) > MAX_HISTORY * 2:
                    self.conversation_history = self.conversation_history[-(MAX_HISTORY * 2):]
                return
        except Exception as e:
            logger.error(f"Error checking cache: {e}")

        self._ensure_initialized()

        context = ""
        sources = set()
        tool_used = "direct_rag"
        query_lower = user_message.lower()

        # Check contact directory keywords
        if any(w in query_lower for w in ["contact", "phone", "email", "number", "faculty", "professor", "hod", "dean", "warden", "office", "directory"]):
            from core.tools import ContactDirectoryTool
            try:
                tool = ContactDirectoryTool()
                context = tool._run(user_message)
                sources.add("Verified Faculty & Staff Directory")
                tool_used = "search_contacts"
            except Exception as e:
                logger.error(f"Direct contact lookup error: {e}")
        # Check calendar keywords
        elif any(w in query_lower for w in ["event", "calendar", "date", "holiday", "exam", "fest", "schedule", "admission date", "deadline"]):
            from core.tools import EventCalendarTool
            try:
                tool = EventCalendarTool()
                context = tool._run(user_message)
                sources.add("Official Academic Calendar 2025-26")
                tool_used = "get_campus_events"
            except Exception as e:
                logger.error(f"Direct calendar lookup error: {e}")
        # Default: Fall back to semantic vector store search
        if not context:
            try:
                from core.embeddings import get_vector_store
                vs = get_vector_store()
                if vs.is_ready:
                    context = vs.get_relevant_context(user_message, top_k=3)
                    found = re.findall(r'\[Source:\s*([^\]]+)\]', context)
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
                    for f in found:
                        clean_name = f.strip().lower()
                        if clean_name in SOURCE_NAME_MAP:
                            sources.add(SOURCE_NAME_MAP[clean_name])
                        else:
                            sources.add(f.strip().replace('.json','').replace('.csv','').replace('.md','').replace('_',' ').title())
                    tool_used = "campus_knowledge_search"
            except Exception as e:
                logger.error(f"Direct vector store lookup error: {e}")

        yield {"type": "tool", "name": tool_used}

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
        ]
        if context:
            messages.append(SystemMessage(content=f"Use this retrieved verified information to answer the question:\n{context}"))
        for msg in self.conversation_history[-4:]:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
        messages.append(HumanMessage(content=user_message))

        full_response = ""
        try:
            for chunk in self._llm.stream(messages):
                text_chunk = _extract_text(chunk.content)
                if text_chunk:
                    full_response += text_chunk
                    yield {"type": "content", "text": text_chunk}
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            try:
                res = self._llm.invoke(messages)
                full_response = _extract_text(res.content)
                yield {"type": "content", "text": full_response}
            except Exception as e2:
                yield {"type": "error", "text": f"Error: {e2}"}
                return

        full_response = re.sub(r'\n+(?:\*\*|)?Sources?(?:\*\*|)?:\s*.*$', '', full_response, flags=re.IGNORECASE | re.DOTALL)
        
        if sources:
            sources_list = "\n".join(f"• {s}" for s in sorted(sources))
            sources_suffix = f"\n\nSource:\n{sources_list}"
            full_response += sources_suffix
            yield {"type": "content", "text": sources_suffix}

        if full_response and not full_response.startswith("⚠️"):
            try:
                from core.database import set_cached_response
                set_cached_response(user_message, full_response)
            except Exception as e:
                logger.error(f"Error writing to cache: {e}")

        self.conversation_history.append({"role": "user",      "content": user_message})
        self.conversation_history.append({"role": "assistant",  "content": full_response})
        if len(self.conversation_history) > MAX_HISTORY * 2:
            self.conversation_history = self.conversation_history[-(MAX_HISTORY * 2):]

        resp_time_ms = int((time.time() - start_time) * 1000)
        yield {"type": "time", "ms": resp_time_ms, "full_text": full_response}

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
