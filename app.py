import streamlit as st
import os
from dotenv import load_dotenv
import time

# Load environment variables first
load_dotenv()

from src.ingestion.pdf_loader import load_pdf_from_bytes
from src.ingestion.chunker import chunk_text
from src.retrieval.vector_store import VectorStore
from src.retrieval.embeddings import EmbeddingService
from src.ai.rag import RAGPipeline
from src.engineering.calculations import ElectricalCalculators
from src.engineering.troubleshooting import TroubleshootingFramework

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
                        pdf_result = load_pdf_from_bytes(file.read(), file.name)
                        pages_data = pdf_result["pages"]
                        
                        if not pages_data:
                            st.error(f"No extractable text found in {file.name}")
                            continue
                            
                        chunks = chunk_text(pages_data)
                        texts = [c["text"] for c in chunks]
                        embeddings = embedder.embed_texts(texts)
                        
                        was_added = vector_store.add_chunks(chunks, embeddings)
                        
                        if was_added:
                            total_chunks += len(chunks)
                            st.success(f"Processed {file.name}")
                        else:
                            st.info(f"Skipped {file.name} - Already exists in knowledge base.")
                            
                    except Exception as e:
                        st.error(f"Error processing {file.name}: {e}")
                
                if total_chunks > 0:
                    st.success(f"Successfully added {total_chunks} new chunks!")
        else:
            st.warning("Please upload PDFs first.")

    st.divider()
    
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
    st.caption("LLM: Gemini 3.6 Flash")
    st.caption("Embeddings: all-MiniLM-L6-v2")

# ==========================================
# UI: MAIN AREA
# ==========================================
st.title("⚡ NLC Electrical Engineering AI Copilot")

st.info("⚠️ **DISCLAIMER:** This AI assistant is intended for engineering learning, documentation assistance, and preliminary analysis. It must not replace approved plant procedures, OEM manuals, protection philosophies, statutory requirements, or qualified engineering judgment.")

# Create modular navigation tabs
tab_chat, tab_calc, tab_troubleshoot = st.tabs(["💬 Assistant", "🧮 Calculators", "🔧 Troubleshooting"])

# --- TAB 1: Chat Assistant ---
with tab_chat:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("E.g. Explain transformer differential protection..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            # Stream the answer directly to the UI
            response_data = rag_pipeline.stream_answer(prompt, st.session_state.messages[:-1])
            answer = st.write_stream(response_data["generator"])
            
            if response_data.get("sources"):
                with st.expander("View Retrieved Context"):
                    for idx, src in enumerate(response_data["sources"]):
                        st.markdown(f"**Source:** `{src['source']}` (Page {src['page']})")
                        st.caption(src["text"])
                        if idx < len(response_data["sources"]) - 1:
                            st.divider()
                                
        st.session_state.messages.append({"role": "assistant", "content": answer})

# --- TAB 2: Deterministic Calculators ---
with tab_calc:
    st.markdown("### Electrical Calculations Engine")
    calc_option = st.selectbox("Select Calculation", ["Three-Phase Current", "Transformer Impedance"])
    
    if calc_option == "Three-Phase Current":
        col1, col2, col3 = st.columns(3)
        mva = col1.number_input("Power (MVA)", min_value=0.1, value=10.0)
        kv = col2.number_input("Voltage (kV)", min_value=0.1, value=11.0)
        pf = col3.number_input("Power Factor", min_value=0.1, max_value=1.0, value=0.85)
        
        if st.button("Calculate Current"):
            res = ElectricalCalculators.three_phase_current(mva, kv, pf)
            st.success(f"**Result:** {res['result']} {res['units']}")
            st.caption(f"**Formula:** {res['formula']}")
            
    elif calc_option == "Transformer Impedance":
        col1, col2, col3 = st.columns(3)
        kv = col1.number_input("Voltage (kV)", min_value=0.1, value=11.0)
        base = col2.number_input("Base (MVA)", min_value=0.1, value=10.0)
        z = col3.number_input("% Impedance", min_value=0.1, value=5.0)
        
        if st.button("Calculate Impedance"):
            res = ElectricalCalculators.transformer_impedance(kv, base, z)
            st.success(f"**Result:** {res['result']} {res['units']}")
            st.caption(f"**Formula:** {res['formula']}")

# --- TAB 3: Troubleshooting ---
with tab_troubleshoot:
    st.markdown("### Engineering Fault Analysis")
    fault_opt = st.selectbox("Select Fault Scenario", ["Earth_Fault", "Differential"])
    
    if st.button("Generate Troubleshooting Guide"):
        guide = TroubleshootingFramework.get_template(fault_opt)
        st.markdown(guide)
