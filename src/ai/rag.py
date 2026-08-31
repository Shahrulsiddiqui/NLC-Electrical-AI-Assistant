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
            
            # 4. Generate Answer
            raw_answer = self.llm.generate_response(prompt, chat_history)
            
            # 5. Inject Safety Guardrails for High-Risk Queries
            safety_prefix = SafetyClassifier.get_safety_disclaimer(risk_level)
            final_answer = safety_prefix + raw_answer
            
            return {
                "answer": final_answer,
                "sources": retrieved_chunks,
                "metadata": {
                    "query_type": query_type.name,
                    "risk_level": risk_level.name
                }
            }
            
        except Exception as e:
            logger.error(f"RAG Error: {e}")
            return {"answer": f"An error occurred during retrieval/generation: {str(e)}", "sources": []}
