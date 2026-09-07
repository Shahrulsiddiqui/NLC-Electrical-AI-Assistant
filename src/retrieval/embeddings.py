import google.generativeai as genai
import os
import logging
from typing import List

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is missing.")
        genai.configure(api_key=api_key)
        self.model_name = "models/text-embedding-004"

    def embed_query(self, query: str) -> List[float]:
        """Instantly embeds the user's search query using Google's API."""
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Query Embedding Error: {e}")
            raise

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Instantly embeds PDF chunks using Google's API."""
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=texts,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            logger.error(f"Document Embedding Error: {e}")
            raise
