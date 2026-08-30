
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
CHUNK_SIZE = 400      # Words per chunk
CHUNK_OVERLAP = 50   # Overlap in words

# Embedding Configuration
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"

# Vector Store Configuration
COLLECTION_NAME = "nlc_electrical_docs"
TOP_K_RETRIEVAL = 5

# LLM Configuration
GEMINI_MODEL_NAME = "gemini-3.6-flash"
