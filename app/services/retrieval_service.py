from app.services.embedding_service import EmbeddingService
from app.services.vector_store import QdrantService


class RetrievalService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.qdrant_service = QdrantService()

    def search(
        self,
        question: str,
        top_k: int = 5,
    ):
        query_vector = (
            self.embedding_service.embed_text(question)
        )

        return self.qdrant_service.search(
            query_vector=query_vector,
            limit=top_k,
        )