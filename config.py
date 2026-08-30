
import os
from pathlib import Path

# Project Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CHROMA_PATH = DATA_DIR / "chroma"
DOCUMENTS_DIR = BASE_DIR / "documents"

# Ensure directories exist
CHROMA_PATH.mkdir(parents=True, exist_ok=True)
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

# Chunking Configuration
CHUNK_SIZE = 800      # Words per chunk
CHUNK_OVERLAP = 150   # Overlap in words

# Embedding Configuration
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# Vector Store Configuration
COLLECTION_NAME = "nlc_electrical_docs"
TOP_K_RETRIEVAL = 5

# LLM Configuration
GEMINI_MODEL_NAME = "gemini-2.5-flash"
