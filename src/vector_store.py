
import chromadb
from typing import List, Dict, Any
import config
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name=config.COLLECTION_NAME)

    def add_chunks(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        """Adds text chunks and embeddings to ChromaDB."""
        if not chunks:
            return

        ids = [chunk["chunk_id"] for chunk in chunks]
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [{"source": c["source"], "page": c["page"]} for c in chunks]

        # Check if documents already exist to prevent duplicate chunks
        existing_sources = set(m["source"] for m in self.collection.get(include=["metadatas"])["metadatas"] if m)
        new_sources = set(c["source"] for c in chunks)
        
        for source in new_sources:
            if source in existing_sources:
                logger.warning(f"Deleting existing chunks for {source} before inserting updates.")
                self.collection.delete(where={"source": source})

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )
        logger.info(f"Added {len(chunks)} chunks to vector store.")

    def search(self, query_embedding: List[float], top_k: int = config.TOP_K_RETRIEVAL) -> List[Dict[str, Any]]:
        """Searches for most similar chunks."""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas"]
        )
        
        retrieved = []
        if results["documents"] and results["documents"][0]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            for doc, meta in zip(docs, metas):
                retrieved.append({
                    "text": doc,
                    "source": meta["source"],
                    "page": meta["page"]
                })
        return retrieved

    def clear_database(self):
        """Deletes all entries in the collection."""
        try:
            self.client.delete_collection(config.COLLECTION_NAME)
            self.collection = self.client.create_collection(name=config.COLLECTION_NAME)
            logger.info("Knowledge base cleared.")
        except Exception as e:
            logger.error(f"Error clearing database: {e}")

    def get_collection_count(self) -> int:
        return self.collection.count()
        
    def get_uploaded_documents(self) -> List[str]:
        metadatas = self.collection.get(include=["metadatas"])["metadatas"]
        if not metadatas:
            return []
        sources = set(meta["source"] for meta in metadatas if meta and "source" in meta)
        return sorted(list(sources))
