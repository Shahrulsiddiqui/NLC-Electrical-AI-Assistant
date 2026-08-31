from src.ingestion.chunker import chunk_text
import config

def test_chunking_with_stable_ids():
    pages_data = [
        {
            "source": "Transformer_Manual.pdf",
            "doc_hash": "a83f9c21",
            "page": 47,
            "text": "The 87T relay protects against internal winding faults."
        }
    ]
    
    config.CHUNK_SIZE = 100
    config.CHUNK_OVERLAP = 20
    
    chunks = chunk_text(pages_data)
    
    assert len(chunks) == 1
    assert chunks[0]["source"] == "Transformer_Manual.pdf"
    assert chunks[0]["doc_hash"] == "a83f9c21"
    assert chunks[0]["page"] == 47
    assert chunks[0]["chunk_id"] == "a83f9c21_p047_c000"
