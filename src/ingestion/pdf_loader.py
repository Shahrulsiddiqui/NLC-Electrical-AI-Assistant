import fitz  # PyMuPDF
import hashlib
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def generate_doc_hash(file_bytes: bytes) -> str:
    """Generates a SHA-256 hash for strict document deduplication."""
    return hashlib.sha256(file_bytes).hexdigest()

def load_pdf_from_bytes(file_bytes: bytes, filename: str) -> Dict[str, Any]:
    """Extracts text and structural metadata from a PDF file via PyMuPDF."""
    doc_hash = generate_doc_hash(file_bytes)
    pages_data = []
    
    try:
        pdf_document = fitz.open(stream=file_bytes, filetype="pdf")
        
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text = page.get_text("text").strip()
            
            if text:
                pages_data.append({
                    "page_number": page_num + 1,
                    "text": text,
                    "source": filename,
                    "doc_hash": doc_hash
                })
            else:
                logger.warning(f"Page {page_num + 1} in {filename} lacks extractable text. Scanned document detected.")
                
        pdf_document.close()
        
    except Exception as e:
        logger.error(f"Failed to parse PDF {filename}: {str(e)}")
        raise ValueError(f"Failed to parse {filename}. Ensure it is a valid, uncorrupted PDF.")

    return {
        "filename": filename,
        "doc_hash": doc_hash,
        "pages": pages_data,
        "total_pages": len(pages_data)
    }
