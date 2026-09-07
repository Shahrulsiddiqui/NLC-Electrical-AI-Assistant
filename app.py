import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

from src.ingestion.pdf_loader import load_pdf_from_bytes
from src.ingestion.chunker import chunk_text
from src.retrieval.vector_store import VectorStore
from src.retrieval.embeddings import EmbeddingService
from src.ai.rag import RAGPipeline
from src.engineering.calculations import ElectricalCalculators
from src.engineering.troubleshooting import TroubleshootingFramework

st.set_page_config(page_title="NLC Electrical AI", page_icon="⚡", layout="centered", initial_sidebar_state="collapsed")

@st.cache_resource
def get_rag_components():
    rag = RAGPipeline()
    return rag, rag.vector_store, rag.embedder

rag_pipeline, vector_store, embedder = get_rag_components()

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("⚡ NLC AI Settings")
    st.caption("Power Plant Engineering Copilot")
    st.divider()
    chunk_count = vector_store.get_collection_count()
    st.metric("Database Chunks", chunk_count)
    if st.button("🗑️ Clear Knowledge Base", type="primary"):
        vector_store.clear_database()
        st.success("Database cleared.")
        st.rerun()

st.markdown("### ⚡ NLC Electrical AI")
st.caption("Power Plant Engineering Copilot")

tab_chat, tab_calc, tab_troubleshoot = st.tabs(["💬 Chat", "🧮 Calculators", "🔧 Troubleshoot"])

with tab_chat:
    doc_count = len(vector_store.get_uploaded_documents())
    if doc_count > 0:
        st.caption(f"🟢 **Knowledge Active:** {doc_count} NLC documents loaded.")
    else:
        st.caption("⚪ **Knowledge Empty:** Attach PDFs below to ground the AI.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    with st.expander("📎 Attach Documents (PDF)", expanded=False):
        uploaded_files = st.file_uploader("Upload NLC manuals before asking", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")
        if st.button("Process Documents", use_container_width=True):
            if uploaded_files:
                with st.spinner("Processing..."):
                    total_added = 0
                    for file in uploaded_files:
                        try:
                            pdf_result = load_pdf_from_bytes(file.read(), file.name)
                            if pdf_result["pages"]:
                                chunks = chunk_text(pdf_result["pages"])
                                texts = [c["text"] for c in chunks]
                                embeddings = embedder.embed_texts(texts)
                                if vector_store.add_chunks(chunks, embeddings):
                                    total_added += len(chunks)
                        except Exception as e:
                            st.error(f"Error processing {file.name}: {e}")
                    if total_added > 0:
                        st.success(f"Added {total_added} chunks. Ready to answer.")
                        st.rerun()
            else:
                st.warning("Select a file first.")

    if prompt := st.chat_input("Ask NLC Electrical AI..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response_data = rag_pipeline.stream_answer(prompt, st.session_state.messages[:-1])
            answer = st.write_stream(response_data["generator"])
            
            if response_data.get("sources"):
                with st.expander("📚 View Retrieved Context"):
                    for idx, src in enumerate(response_data["sources"]):
                        st.markdown(f"**📄 {src['source']}** (Page {src['page']})")
                        st.caption(src["text"])
                        if idx < len(response_data["sources"]) - 1:
                            st.divider()
            
            if answer and str(answer).strip():
                st.session_state.messages.append({"role": "assistant", "content": answer})

with tab_calc:
    calc_option = st.selectbox("Select Calculation", ["Three-Phase Current", "Three-Phase Power", "Transformer Impedance"], label_visibility="collapsed")
    
    if calc_option == "Three-Phase Current":
        col1, col2, col3 = st.columns(3)
        mva = col1.number_input("MVA", min_value=0.1, value=10.0)
        kv = col2.number_input("kV", min_value=0.1, value=11.0)
        pf = col3.number_input("PF", min_value=0.1, max_value=1.0, value=0.85)
        if st.button("Calculate", use_container_width=True):
            res = ElectricalCalculators.three_phase_current(mva, kv, pf)
            st.success(f"**Result:** {res['result']} {res['units']}")
            st.caption(f"**Formula:** {res['formula']}")
            
    elif calc_option == "Three-Phase Power":
        col1, col2, col3 = st.columns(3)
        kv = col1.number_input("Voltage (kV)", min_value=0.1, value=11.0)
        amp = col2.number_input("Current (A)", min_value=0.0, value=500.0)
        pf = col3.number_input("PF", min_value=0.1, max_value=1.0, value=0.85)
        if st.button("Calculate", use_container_width=True):
            res = ElectricalCalculators.three_phase_power(kv, amp, pf)
            st.success(f"**Result:** {res['result']} {res['units']}")
            st.caption(f"**Formula:** {res['formula']}")

    elif calc_option == "Transformer Impedance":
        col1, col2, col3 = st.columns(3)
        kv = col1.number_input("kV", min_value=0.1, value=11.0)
        base = col2.number_input("Base MVA", min_value=0.1, value=10.0)
        z = col3.number_input("% Z", min_value=0.1, value=5.0)
        if st.button("Calculate", use_container_width=True):
            res = ElectricalCalculators.transformer_impedance(kv, base, z)
            st.success(f"**Result:** {res['result']} {res['units']}")
            st.caption(f"**Formula:** {res['formula']}")

with tab_troubleshoot:
    fault_opt = st.selectbox("Select Fault Scenario", ["Earth_Fault", "Differential", "Buchholz"], label_visibility="collapsed")
    if st.button("Generate Guide", use_container_width=True):
        guide = TroubleshootingFramework.get_template(fault_opt)
        st.markdown(guide)
