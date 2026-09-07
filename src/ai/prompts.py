SYSTEM_INSTRUCTION = """You are the NLC Electrical AI Assistant, a deterministic power plant engineering copilot.
1. Distinguish clearly between NLC-verified facts and general engineering principles.
2. NEVER instruct the user to operate live plant equipment. Defer to official SOPs and permits.
3. Keep answers highly structured, technical, and concise. Do not use conversational fluff."""

def build_rag_prompt(query: str, retrieved_chunks: list, confidence: str) -> str:
    context_blocks = []
    for idx, chunk in enumerate(retrieved_chunks):
        context_blocks.append(f"--- SOURCE {idx+1}: {chunk['source']} (Page {chunk['page']}) ---\n{chunk['text']}")
    
    context_str = "\n\n".join(context_blocks)
    
    if confidence == "HIGH":
        behavior_instruction = "Answer the query using ONLY the provided NLC Document Context. Cite the source name and page number."
    elif confidence == "LOW" and retrieved_chunks:
        behavior_instruction = "The retrieved NLC documents lack sufficient detail. State explicitly that NLC documentation is insufficient, then provide an answer based on GENERAL ELECTRICAL ENGINEERING principles."
    else:
        behavior_instruction = "No NLC documents are available. Answer based on general electrical engineering principles."

    prompt = f"""
    {behavior_instruction}

    NLC DOCUMENT CONTEXT:
    {context_str if context_str else "No documents uploaded."}

    ENGINEER'S QUERY:
    {query}
    """
    return prompt

