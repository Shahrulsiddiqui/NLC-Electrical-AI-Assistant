from src.ingestion.chunker import chunk_text

def test_chunking_with_stable_ids():
    mock_pages = [{
        "page_number": 1, 
        "text": "Engineering Paragraph 1\n\nEngineering Paragraph 2",
        "source": "manual.pdf",
        "doc_hash": "testhash123"
    }]
    
    chunks = chunk_text(mock_pages, max_chars=150)
    assert len(chunks) == 2
    assert chunks[0]["page"] == 1
    assert "chunk_id" in chunks[0]
