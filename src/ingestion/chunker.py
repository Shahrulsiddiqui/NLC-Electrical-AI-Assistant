import hashlib
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def generate_chunk_id(doc_hash: str, page_num: int, chunk_index: int) -> str:
    """Creates a deterministic ID for tracking individual chunks in ChromaDB."""
    raw_id = f"{doc_hash}_p{page_num}_c{chunk_index}"
    return hashlib.md5(raw_id.encode()).hexdigest()

def chunk_text(pages_data: List[Dict[str, Any]], max_chars: int = 1500, overlap: int = 200) -> List[Dict[str, Any]]:
    """Splits text by structural paragraphs before falling back to character limits."""
    chunks = []
    
    for page in pages_data:
        source = page["source"]
        doc_hash = page["doc_hash"]
        page_num = page["page_number"]
        full_text = page["text"]
        
        # Structure-aware split: target double newlines first
        paragraphs = [p.strip() for p in full_text.split('\n\n') if p.strip()]
        
        current_chunk_text = ""
        chunk_index = 0
        
        for para in paragraphs:
            if len(current_chunk_text) + len(para) <= max_chars:
                current_chunk_text += para + "\n\n"
            else:
                if current_chunk_text.strip():
                    chunks.append({
                        "chunk_id": generate_chunk_id(doc_hash, page_num, chunk_index),
                        "text": current_chunk_text.strip(),
                        "source": source,
                        "page": page_num,
                        "doc_hash": doc_hash
                    })
                    chunk_index += 1
                
                # Maintain overlap context across chunk boundaries
                overlap_text = current_chunk_text[-overlap:] if len(current_chunk_text) > overlap else current_chunk_text
                current_chunk_text = overlap_text.strip() + "\n\n" + para + "\n\n"
        
        # Flush the remaining text
        if current_chunk_text.strip():
            chunks.append({
                "chunk_id": generate_chunk_id(doc_hash, page_num, chunk_index),
                "text": current_chunk_text.strip(),
                "source": source,
                "page": page_num,
                "doc_hash": doc_hash
            })
            
    logger.info(f"Generated {len(chunks)} structural chunks.")
    return chunks
