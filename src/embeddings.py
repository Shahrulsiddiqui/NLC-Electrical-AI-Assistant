
from sentence_transformers import SentenceTransformer
from typing import List
import config
import logging

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        logger.info(f"Loading embedding model: {config.EMBEDDING_MODEL_NAME}")
        self.model = SentenceTransformer(config.EMBEDDING_MODEL_NAME)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generates embeddings for a list of texts."""
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()
        
    def embed_query(self, query: str) -> List[float]:
        """Generates embedding for a single query."""
        embedding = self.model.encode([query], show_progress_bar=False)
        return embedding[0].tolist()
