import streamlit as st
import os
from dotenv import load_dotenv
import time

# Load environment variables first
load_dotenv()

from src.pdf_loader import load_pdf_from_bytes
from src.chunker import chunk_text
from src.rag import RAGPipeline
from src.vector_store import VectorStore
from src.embeddings import EmbeddingService

st.set_page_config(page_title="NLC Electrical AI", page_icon="⚡", layout="wide")

# ==========================================
# INITIALIZATION
# ==========================================
@st.cache_resource
def get_rag_components():
    return RAGPipeline(), VectorStore(), EmbeddingService()

rag_pipeline, vector_store, embedder = get_rag_components()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# UI: SIDEBAR
# ==========================================
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/f/fa/NLC_India_Limited_Logo.svg/220px-NLC_India_Limited_Logo.svg.png", width=150)
    st.title("Knowledge Base")
    
    uploaded_files = st.file_uploader("Upload Technical Documents (PDF)", type=["pdf"], accept_multiple_files=True)
    
    if st.button("Process Documents"):
        if uploaded_files:
            with st.spinner("Extracting, chunking, and embedding..."):
                total_chunks = 0
                for file in uploaded_files:
                    try:
                        pages_data = load_pdf_from_bytes(file.read(), file.name)
                        if not pages_data:
                            st.error(f"No extractable text found in {file.name}")
                            continue
                            
                        chunks = chunk_text(pages_data)
                        texts = [c["text"] for c in chunks]
                        embeddings = embedder.embed_texts(texts)
                        vector_store.add_chunks(chunks, embeddings)
                        total_chunks += len(chunks)
                    except Exception as e:
                        st.error(f"Error processing {file.name}: {e}")
                
                if total_chunks > 0:
                    st.success(f"Successfully added {total_chunks} chunks to the knowledge base!")
        else:
            st.warning("Please upload PDFs first.")

    st.divider()
    
    # DB Stats
    chunk_count = vector_store.get_collection_count()
    docs = vector_store.get_uploaded_documents()
    
    st.metric("Total Chunks in DB", chunk_count)
    if docs:
        with st.expander("Uploaded Documents"):
            for doc in docs:
                st.write(f"📄 {doc}")
                
    if st.button("Clear Knowledge Base", type="primary"):
        vector_store.clear_database()
        st.success("Knowledge base cleared.")
        st.rerun()

    st.divider()
    st.caption("**Model Info:**")
    st.caption(f"LLM: Gemini 1.5 Flash")
    st.caption(f"Embeddings: all-MiniLM-L6-v2")

# ==========================================
# UI: MAIN AREA
# ==========================================
st.title("⚡ NLC Electrical Engineering AI Assistant")
st.markdown("##### AI-powered electrical engineering knowledge and document assistant.")

st.info("⚠️ **DISCLAIMER:** This AI assistant is intended for engineering learning, documentation assistance, and preliminary analysis. It must not replace approved plant procedures, OEM manuals, protection philosophies, statutory requirements, or qualified engineering judgment. Verify safety-critical information before use.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("E.g. Explain transformer differential protection..."):
    # 1. Add user message to state and UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Get RAG response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing documents & generating response..."):
            response_data = rag_pipeline.answer_question(prompt, st.session_state.messages[:-1])
            answer = response_data["answer"]
            
            st.markdown(answer)
            
            # Show retrieved context optionally
            if response_data["sources"]:
                with st.expander("View Retrieved Context"):
                    for idx, src in enumerate(response_data["sources"]):
                        st.markdown(f"**Source:** `{src['source']}` (Page {src['page']})")
                        st.caption(src["text"])
                        if idx < len(response_data["sources"]) - 1:
                            st.divider()
                            
    # 3. Add assistant response to state
    st.session_state.messages.append({"role": "assistant", "content": answer})

