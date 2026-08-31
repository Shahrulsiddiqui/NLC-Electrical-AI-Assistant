from typing import List, Dict, Any
import config

def chunk_text(pages_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Splits page text into smaller chunks with overlap and deterministic IDs."""
    chunks = []

    for page_dict in pages_data:
        text = page_dict["text"]
        source = page_dict["source"]
        doc_hash = page_dict["doc_hash"]
        page_num = page_dict["page"]
        
        words = text.split()
        if not words:
            continue
            
        step = config.CHUNK_SIZE - config.CHUNK_OVERLAP
        if step <= 0:
            step = config.CHUNK_SIZE
            
        chunk_counter = 0
        for i in range(0, len(words), step):
            chunk_words = words[i:i + config.CHUNK_SIZE]
            chunk_text_str = " ".join(chunk_words)
            
            # V1 Stable ID Format: hash_p[page]_c[chunk]
            chunk_id = f"{doc_hash}_p{page_num:03d}_c{chunk_counter:03d}"
            
            chunks.append({
                "chunk_id": chunk_id,
                "source": source,
                "doc_hash": doc_hash,
                "page": page_num,
                "text": chunk_text_str
            })
            chunk_counter += 1
            
    return chunks
