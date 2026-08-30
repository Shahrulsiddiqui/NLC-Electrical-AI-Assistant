
from src.prompts import build_rag_prompt

def test_build_rag_prompt():
    chunks = [
        {"source": "doc1.pdf", "page": 5, "text": "Transformer relays trip on faults."},
        {"source": "doc2.pdf", "page": 10, "text": "CT saturation causes errors."}
    ]
    
    query = "What causes errors?"
    prompt = build_rag_prompt(query, chunks)
    
    assert "doc1.pdf" in prompt
    assert "CT saturation causes errors." in prompt
    assert "USER QUESTION:\nWhat causes errors?" in prompt
    assert "Do not invent information" in prompt
