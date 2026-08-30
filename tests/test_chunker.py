
from src.chunker import chunk_text
import config

def test_chunking_preserves_metadata():
    pages_data = [
        {"source": "test.pdf", "page": 1, "text": "word " * 1000},
    ]
    
    # Temporarily override config for testing
    config.CHUNK_SIZE = 100
    config.CHUNK_OVERLAP = 20
    
    chunks = chunk_text(pages_data)
    
    assert len(chunks) > 1
    assert chunks[0]["source"] == "test.pdf"
    assert chunks[0]["page"] == 1
    assert "chunk_id" in chunks[0]
