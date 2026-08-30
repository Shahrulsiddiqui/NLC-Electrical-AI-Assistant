
from src.embeddings import EmbeddingService
from src.vector_store import VectorStore
from src.llm import GeminiService
from src.prompts import build_rag_prompt
import logging

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self):
        try:
            self.embedder = EmbeddingService()
            self.vector_store = VectorStore()
            self.llm = GeminiService()
            self.is_ready = True
        except ValueError as e:
            logger.error(f"RAG Pipeline initialization failed: {e}")
            self.is_ready = False
            self.error_msg = str(e)

    def answer_question(self, query: str, chat_history: list) -> dict:
        if not self.is_ready:
            return {"answer": f"System configuration error: {self.error_msg}", "sources": []}

        try:
            # 1. Embed query
            query_embedding = self.embedder.embed_query(query)
            
            # 2. Retrieve chunks
            retrieved_chunks = self.vector_store.search(query_embedding)
            
            # 3. Format Prompt
            prompt = build_rag_prompt(query, retrieved_chunks)
            
            # 4. Exclude the RAG context from being stored raw in the UI history
            # Gemini gets the context, but the UI just shows the user's question.
            answer = self.llm.generate_response(prompt, chat_history)
            
            return {
                "answer": answer,
                "sources": retrieved_chunks
            }
            
        except Exception as e:
            logger.error(f"RAG Error: {e}")
            return {"answer": f"An error occurred during retrieval/generation: {str(e)}", "sources": []}
