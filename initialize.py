"""
initialize.py -- One-time setup script for CampusAI.

Run this BEFORE starting the Streamlit app:
    python initialize.py

What it does:
  1. Validates the environment (.env, API key)
  2. Loads all campus data (JSON, CSV) via processors
  3. Embeds data using sentence-transformers (MiniLM)
  4. Saves FAISS vector index to ./vector_store/
  5. Initializes the SQLite database
  6. Prints a summary of everything loaded
"""

import os
import sys
import logging
from pathlib import Path

# ---- Setup ------------------------------------------------------------------
ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("initialize")

SEP  = "=" * 60
SEP2 = "-" * 40


def print_banner():
    print("\n" + SEP)
    print("   CampusAI -- Universal Campus Info Chatbot")
    print("   Knowledge Base Initialization")
    print(SEP + "\n")


def check_env() -> bool:
    """Check .env file and API key."""
    from dotenv import load_dotenv
    env_path    = ROOT / ".env"
    env_example = ROOT / ".env.example"

    if not env_path.exists():
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_path)
            print("[OK] Created .env from .env.example")
            print("[!!] Please add your OPENAI_API_KEY to .env and re-run.\n")
        else:
            print("[ERR] .env file not found. Create it with your OPENAI_API_KEY.")
        return False

    load_dotenv(env_path)
    api_key = os.getenv("OPENAI_API_KEY", "")

    if not api_key or api_key == "your_openai_api_key_here":
        print("[!!] OPENAI_API_KEY is not set in .env")
        print("     Get a key at: https://platform.openai.com/api-keys")
        print("     Then add:  OPENAI_API_KEY=your_key_here  to .env\n")
        return False

    masked = api_key[:8] + "*" * max(0, len(api_key) - 8)
    print(f"[OK] API Key found: {masked}")
    return True


def check_dependencies() -> bool:
    """Verify all required packages are installed."""
    required = {
        "streamlit":            "streamlit",
        "langchain":            "langchain",
        "langchain_google_genai": "langchain-google-genai",
        "langchain_community":  "langchain-community",
        "langchain_core":       "langchain-core",
        "faiss":                "faiss-cpu",
        "sentence_transformers":"sentence-transformers",
        "bs4":                  "beautifulsoup4",
        "PyPDF2":               "PyPDF2",
        "pandas":               "pandas",
        "plotly":               "plotly",
        "dotenv":               "python-dotenv",
    }

    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)

    if missing:
        print(f"[ERR] Missing packages: {', '.join(missing)}")
        print(f"      Run: pip install {' '.join(missing)}\n")
        return False

    print("[OK] All dependencies installed")
    return True


def load_all_documents() -> list:
    """Load and process all campus data sources."""
    from processors.data_loader import load_all_data
    from processors.contact_processor import process_contacts
    from processors.calendar_processor import process_calendar
    from processors.pdf_processor import load_all_pdfs

    DATA_DIR = ROOT / "data"
    all_docs  = []

    print("\nLoading campus data sources...")

    # 1. JSON data files
    print("   [1] Loading campus JSON data files...")
    json_docs = load_all_data()
    all_docs.extend(json_docs)
    print(f"       -> {len(json_docs)} chunks from JSON files")

    # 2. Contacts CSV
    contacts_file = DATA_DIR / "contacts" / "directory.csv"
    if contacts_file.exists():
        print("   [2] Processing contact directory...")
        contact_docs = process_contacts(contacts_file)
        all_docs.extend(contact_docs)
        print(f"       -> {len(contact_docs)} contact documents")

    # 3. Academic Calendar
    calendar_file = DATA_DIR / "events" / "academic_calendar.json"
    if calendar_file.exists():
        print("   [3] Processing academic calendar...")
        calendar_docs = process_calendar(calendar_file)
        all_docs.extend(calendar_docs)
        print(f"       -> {len(calendar_docs)} calendar documents")

    # 4. PDF handbooks (optional)
    handbooks_dir = DATA_DIR / "handbooks"
    handbooks_dir.mkdir(exist_ok=True)
    pdf_files = list(handbooks_dir.glob("*.pdf"))
    if pdf_files:
        print(f"   [4] Processing {len(pdf_files)} PDF handbook(s)...")
        pdf_docs = load_all_pdfs(handbooks_dir)
        all_docs.extend(pdf_docs)
        print(f"       -> {len(pdf_docs)} PDF chunks")
    else:
        print("   [4] No PDF handbooks found (add PDFs to data/handbooks/ later)")

    print(f"\nTotal: {len(all_docs)} documents loaded from all sources")
    return all_docs


def build_vector_store(documents: list) -> bool:
    """Build and save the FAISS vector index."""
    if not documents:
        print("[ERR] No documents to index!")
        return False

    print(f"\nBuilding FAISS vector index ({len(documents)} documents)...")
    print("    Model: sentence-transformers/all-MiniLM-L6-v2")
    print("    NOTE: First run downloads ~90MB model -- please wait...\n")

    try:
        from core.embeddings import build_and_save_vector_store
        vs = build_and_save_vector_store(documents)
        print(f"\n[OK] Vector store built: {vs.index.ntotal} vectors indexed")
        print(f"     Saved to: {ROOT / 'vector_store'}")
        return True
    except Exception as e:
        print(f"[ERR] Vector store build failed: {e}")
        logger.exception("Vector store build error")
        return False


def init_database() -> bool:
    """Initialize the SQLite database."""
    print("\nInitializing SQLite database...")
    try:
        from core.database import initialize_database
        initialize_database()
        db_path = os.getenv("DB_PATH", "./campus.db")
        print(f"[OK] Database ready at: {db_path}")
        return True
    except Exception as e:
        print(f"[ERR] Database init failed: {e}")
        return False


def test_vector_search() -> bool:
    """Run a quick test query on the vector store."""
    print("\nTesting vector search...")
    try:
        from core.embeddings import get_vector_store
        vs      = get_vector_store()
        results = vs.search("minimum attendance requirement", top_k=2)
        if results:
            score, doc = results[0]
            preview = doc["text"][:80].replace("\n", " ")
            print(f"[OK] Search test passed (score={score:.3f})")
            print(f"     Sample: \"{preview}...\"")
            return True
        else:
            print("[!!] Search returned no results. Check data files.")
            return False
    except Exception as e:
        print(f"[ERR] Search test failed: {e}")
        return False


def print_summary(doc_count: int, success: bool):
    print("\n" + SEP)
    if success:
        print("   INITIALIZATION COMPLETE!")
        print(f"   {doc_count} documents indexed in vector store")
        print("\n   Start the app with:")
        print("       streamlit run app.py")
        print("\n   Then open: http://localhost:8501")
    else:
        print("   INITIALIZATION FAILED")
        print("   Please fix the errors above and re-run:")
        print("       python initialize.py")
    print(SEP + "\n")


def main():
    print_banner()

    # Step 1: Environment check
    print("Step 1/5  Environment check")
    print(SEP2)
    env_ok = check_env()
    if not env_ok:
        from dotenv import load_dotenv
        load_dotenv()     # load anyway so DB_PATH etc. are available

    # Step 2: Dependency check
    print("\nStep 2/5  Dependency check")
    print(SEP2)
    deps_ok = check_dependencies()
    if not deps_ok:
        print("\n[ERR] Please install missing packages and re-run.")
        sys.exit(1)

    # Step 3: Load documents
    print("\nStep 3/5  Data loading")
    print(SEP2)
    documents = load_all_documents()

    # Step 4: Build vector store
    print("\nStep 4/5  Building knowledge base")
    print(SEP2)
    vs_ok = build_vector_store(documents)

    # Step 5: Initialize database
    print("\nStep 5/5  Database initialization")
    print(SEP2)
    db_ok = init_database()

    # Quick search test
    if vs_ok:
        test_vector_search()

    success = vs_ok and db_ok
    print_summary(len(documents), success)

    if not env_ok:
        print("[!!] REMINDER: Add your OPENAI_API_KEY to .env before running the app!")
        print("     Get a key at: https://platform.openai.com/api-keys\n")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
