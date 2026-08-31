from src.retrieval.embeddings import EmbeddingService
from src.retrieval.vector_store import VectorStore
from src.ai.llm import GeminiService
from src.ai.prompts import build_rag_prompt
from src.safety.guardrails import SafetyClassifier, RiskLevel
from src.ai.query_router import QueryRouter, QueryType
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
        # Fallback method if not streaming
        try:
            risk_level = SafetyClassifier.classify_query(query)
            query_embedding = self.embedder.embed_query(query)
            retrieved_chunks = self.vector_store.search(query_embedding)
            prompt = build_rag_prompt(query, retrieved_chunks)
            raw_answer = self.llm.generate_response(prompt, chat_history)
            safety_prefix = SafetyClassifier.get_safety_disclaimer(risk_level)
            return {"answer": safety_prefix + raw_answer, "sources": retrieved_chunks}
        except Exception as e:
            return {"answer": f"Error: {str(e)}", "sources": []}

    def stream_answer(self, query: str, chat_history: list) -> dict:
        """Handles RAG retrieval and returns a real-time text generator."""
        if not self.is_ready:
            def error_gen(): yield f"System configuration error: {self.error_msg}"
            return {"generator": error_gen(), "sources": []}

        try:
            # 1. Classification & Routing
            risk_level = SafetyClassifier.classify_query(query)
            query_type = QueryRouter.route_query(query)
            logger.info(f"Query routed as {query_type.name} with {risk_level.name} risk.")
            
            # 2. Embed & Retrieve
            query_embedding = self.embedder.embed_query(query)
            retrieved_chunks = self.vector_store.search(query_embedding)
            
            # 3. Format Prompt
            prompt = build_rag_prompt(query, retrieved_chunks)
            
            # 4. Create Stream Generator
            def response_generator():
                safety_prefix = SafetyClassifier.get_safety_disclaimer(risk_level)
                if safety_prefix:
                    yield safety_prefix + "\n\n"
                
                # Yield tokens from LLM as they arrive
                for chunk in self.llm.generate_stream(prompt, chat_history):
                    yield chunk

            return {
                "generator": response_generator(),
                "sources": retrieved_chunks,
                "metadata": {
                    "query_type": query_type.name,
                    "risk_level": risk_level.name
                }
            }
            
        except Exception as e:
            logger.error(f"RAG Error: {e}")
            def error_gen(): yield f"An error occurred during retrieval/generation: {str(e)}"
            return {"generator": error_gen(), "sources": []}
