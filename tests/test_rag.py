from src.ai.prompts import build_rag_prompt

def test_build_rag_prompt():
    query = "What is differential protection?"
    chunks = [{"source": "SOP.pdf", "page": 1, "text": "Differential protects the transformer."}]
    
    # V1.0 requires confidence scoring
    prompt = build_rag_prompt(query, chunks, confidence="HIGH")
    
    assert "SOP.pdf" in prompt
    assert "Differential protects" in prompt
