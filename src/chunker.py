
from typing import List, Dict, Any
import config

def chunk_text(pages_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Splits page text into smaller chunks based on word count with overlap.
    Preserves document name and page number metadata.
    """
    chunks = []
    chunk_id_counter = 0

    for page_dict in pages_data:
        text = page_dict["text"]
        source = page_dict["source"]
        page_num = page_dict["page"]
        
        words = text.split()
        
        if not words:
            continue
            
        step = config.CHUNK_SIZE - config.CHUNK_OVERLAP
        if step <= 0:
            step = config.CHUNK_SIZE # Fallback if misconfigured
            
        for i in range(0, len(words), step):
            chunk_words = words[i:i + config.CHUNK_SIZE]
            chunk_text_str = " ".join(chunk_words)
            
            chunk_id = f"{source}_p{page_num}_c{chunk_id_counter}"
            
            chunks.append({
                "chunk_id": chunk_id,
                "source": source,
                "page": page_num,
                "text": chunk_text_str
            })
            chunk_id_counter += 1
            
    return chunks
