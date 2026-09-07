# ⚡ NLC Electrical AI Assistant V1.0
**Power Plant Engineering Copilot**

A production-ready, mobile-first AI assistant designed for NLC electrical engineers. It combines document-grounded Retrieval-Augmented Generation (RAG) with isolated deterministic calculation engines and strict operational safety guardrails.

## Core Capabilities
* **Structure-Aware RAG:** Ingests plant manuals using PyMuPDF, chunks text by structural paragraphs, and persistently stores embeddings in ChromaDB for cross-session memory.
* **Deterministic Calculators:** A dedicated Python engine processes 3-phase power, load current, and transformer impedance. Math is isolated from the LLM to prevent hallucinations.
* **Troubleshooting Matrices:** Instant access to structured diagnostic guides for complex faults (e.g., Transformer Differential, Buchholz trips, Earth Faults).
* **Safety-First Routing:** Active regex-based guardrails intercept operational commands (e.g., "close breaker", "bypass relay") and enforce strict permit-to-work/LOTO warnings.
* **Mobile-First UI:** A ChatGPT-style interface with a sticky unified attachment composer and real-time streaming AI responses.

## Architecture Stack
* **Frontend:** Streamlit
* **LLM Framework:** Google Gemini (Streaming enabled)
* **Vector Database:** ChromaDB (Persistent Local Storage)
* **Ingestion:** PyMuPDF & Sentence-Transformers (`all-MiniLM-L6-v2`)
* **CI/CD:** GitHub Actions (Pytest)

## Local Installation
1. Clone the repository and navigate to the project directory.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file in the root directory and add: `GEMINI_API_KEY=your_api_key_here`
4. Launch the copilot: `streamlit run app.py`

## Safety Philosophy
This AI is an engineering assistant, not an operational authority. It is hardcoded to never authorize equipment energization, override LOTO protocols, or replace approved Standard Operating Procedures (SOPs). All safety-critical queries are automatically routed to a non-authoritative diagnostic mode.

## V2.0 Roadmap
* Plant-specific equipment databases
* Single-line diagram (SLD) visual analysis
* Disturbance recorder (DR) event file parsing
