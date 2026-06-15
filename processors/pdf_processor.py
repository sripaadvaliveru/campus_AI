"""
pdf_processor.py — Extracts and chunks text from PDF handbooks and policy documents.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def extract_text_from_pdf(filepath: Path) -> List[Dict[str, Any]]:
    """Extract text from a PDF file and return as chunked documents."""
    documents = []
    try:
        import PyPDF2

        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            num_pages = len(reader.pages)

            full_text = ""
            page_texts = []
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text = page.extract_text() or ""
                page_texts.append((page_num + 1, text))
                full_text += text + "\n"

            # Create chunks of ~600 chars with overlap
            chunks = _chunk_text_with_metadata(page_texts, filepath.name)
            documents.extend(chunks)

            logger.info(f"Extracted {len(documents)} chunks from {filepath.name} ({num_pages} pages)")

    except ImportError:
        logger.error("PyPDF2 not installed. Run: pip install PyPDF2")
    except Exception as e:
        logger.error(f"Error processing PDF {filepath}: {e}")

    return documents


def _chunk_text_with_metadata(
    page_texts: List[tuple],
    source_name: str,
    chunk_size: int = 600,
    overlap: int = 100
) -> List[Dict[str, Any]]:
    """Create overlapping text chunks from page-level text, preserving page metadata."""
    documents = []
    current_chunk = ""
    current_page = 1

    for page_num, text in page_texts:
        sentences = text.replace("\n", " ").split(". ")
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if len(current_chunk) + len(sentence) > chunk_size:
                if current_chunk.strip():
                    documents.append({
                        "text": current_chunk.strip(),
                        "metadata": {
                            "source": source_name,
                            "page": current_page,
                            "type": "pdf_handbook"
                        }
                    })
                # Start new chunk with overlap
                words = current_chunk.split()
                overlap_text = " ".join(words[-20:]) if len(words) > 20 else current_chunk
                current_chunk = overlap_text + " " + sentence
                current_page = page_num
            else:
                current_chunk += " " + sentence
                current_page = page_num

    # Add final chunk
    if current_chunk.strip():
        documents.append({
            "text": current_chunk.strip(),
            "metadata": {
                "source": source_name,
                "page": current_page,
                "type": "pdf_handbook"
            }
        })

    return documents


def load_all_pdfs(pdf_dir: Path) -> List[Dict[str, Any]]:
    """Load all PDF files from the given directory."""
    all_docs = []

    if not pdf_dir.exists():
        logger.warning(f"PDF directory not found: {pdf_dir}")
        return all_docs

    pdf_files = list(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        logger.info(f"No PDF files found in {pdf_dir}")
        return all_docs

    for pdf_file in pdf_files:
        docs = extract_text_from_pdf(pdf_file)
        all_docs.extend(docs)

    logger.info(f"Total PDF documents loaded: {len(all_docs)}")
    return all_docs
