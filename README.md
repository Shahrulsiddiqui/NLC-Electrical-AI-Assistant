# NLC Electrical Engineering AI Assistant ⚡

## Overview
A Retrieval-Augmented Generation (RAG) AI assistant designed specifically for electrical engineers in power plants. It enables users to upload technical PDFs (manuals, SOPs, relay catalogs), automatically chunks and embeds the text into a local vector database, and uses Google's Gemini API to answer engineering questions accurately while citing document sources.

## Features
- **Local PDF Processing**: Extract and chunk text preserving page numbers.
- **Local Vector Search**: Uses ChromaDB and `all-MiniLM-L6-v2` embeddings for fast, private document retrieval.
- **Context-Aware AI Answers**: Powered by Google Gemini 1.5 Flash.
- **Engineering Guardrails**: Strict system prompts to prevent hallucination of critical data (relay settings, ratings).
- **Source Citations**: Clearly displays the source document and page number for every answer.
- **Conversation Memory**: Remembers context during a chat session.

## Architecture
```text
PDF Document
    ↓
Text Extraction (PyMuPDF)
    ↓
Text Chunking (Overlap window)
    ↓
Embeddings (sentence-transformers)
    ↓
Vector DB (ChromaDB - Local)
    ↓
Similarity Search (Top K Retrieval)
    ↓
LLM Generation (Gemini API + System Prompt)
    ↓
Answer + Source Citations + UI (Streamlit)
