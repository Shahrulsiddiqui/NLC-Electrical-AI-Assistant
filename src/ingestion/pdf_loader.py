import fitz  # PyMuPDF
import hashlib
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def get_file_hash(file_bytes: bytes) -> str:
    """Generates a SHA-256 hash of the file for duplicate detection."""
    return hashlib.sha256(file_bytes).hexdigest()[:16]  # Short hash for clean IDs

def load_pdf_from_bytes(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    """
    Extracts text from a PDF file in memory.
    Returns a dictionary containing the document hash and page data.
    """
    doc_hash = get_file_hash(file_bytes)
    pages_data = []
    
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text").strip()
            
            if text:
                pages_data.append({
                    "source": filename,
                    "doc_hash": doc_hash,
                    "page": page_num + 1,
                    "text": text
                })
        doc.close()
        logger.info(f"Processed {len(pages_data)} pages from {filename} (Hash: {doc_hash})")
        return {"doc_hash": doc_hash, "pages": pages_data}
    except Exception as e:
        logger.error(f"Failed to extract text from {filename}: {str(e)}")
        raise e
