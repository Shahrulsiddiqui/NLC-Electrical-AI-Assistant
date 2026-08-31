# NLC Electrical AI Assistant (V1)

An AI-powered electrical engineering copilot designed for power-plant engineers. This tool combines Retrieval-Augmented Generation (RAG) with deterministic engineering calculations and strict safety guardrails to assist with documentation lookup, troubleshooting, and plant maintenance.

### 🚀 V1 Capabilities
* **Intelligent RAG Assistant:** Query technical documents with accurate citations and source page references.
* **Smart Ingestion Pipeline:** Automatic SHA-256 duplicate detection prevents re-indexing the same PDF, saving compute and time.
* **Deterministic Calculations:** A dedicated Python engine handles math (e.g., three-phase current, transformer impedance) safely outside the LLM to eliminate AI hallucinations on critical numbers.
* **Troubleshooting Framework:** Structured diagnostic templates for common electrical faults (e.g., Earth Faults, Differential Trips).
* **Safety Guardrails:** Pre-generation query classification actively identifies and blocks unauthorized operational commands while injecting required safety warnings.

### 🏗️ Modular Architecture
The V1 codebase is decoupled for maintainability and scalability:
* **`src/ingestion/`**: Handles PyMuPDF parsing, text extraction, and stable, hash-aware text chunking.
* **`src/retrieval/`**: Manages the in-memory ChromaDB vector store and semantic embeddings.
* **`src/ai/`**: Contains the Gemini 3.6 Flash integration, query routing, and RAG pipeline logic.
* **`src/engineering/`**: Houses the deterministic math calculators and structured troubleshooting templates.
* **`src/safety/`**: Executes risk classification (Low/Normal/High) to enforce plant safety protocols before the LLM generates a response.

### 🧪 Automated Testing (GitHub Actions)
This repository utilizes GitHub Actions for Continuous Integration (CI). Every commit pushed to the `main` branch automatically triggers an Ubuntu virtual runner to execute the `pytest` suite. 

The automated pipeline rigorously verifies:
* Accuracy of the deterministic calculation engine.
* Keyword detection in the safety guardrail classifier.
* Stability of document hashing and chunk ID generation.
* Proper import paths across the modular architecture.

To view the latest test results or run logs, navigate to the **Actions** tab in this GitHub repository.
