
import fitz  # PyMuPDF
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def load_pdf_from_bytes(file_bytes: bytes, filename: str) -> List[Dict[str, Any]]:
    """
    Extracts text from a PDF file in memory.
    Returns a list of dictionaries containing page metadata and text.
    """
    pages_data = []
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text").strip()
            
            if text:  # Ignore empty pages
                pages_data.append({
                    "source": filename,
                    "page": page_num + 1,  # 1-indexed pages for users
                    "text": text
                })
        doc.close()
        logger.info(f"Successfully processed {len(pages_data)} pages from {filename}")
        return pages_data
    except Exception as e:
        logger.error(f"Failed to extract text from {filename}: {str(e)}")
        raise e
