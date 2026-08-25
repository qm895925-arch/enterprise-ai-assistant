from app.services.embedding_service import EmbeddingService
from app.services.vector_store import QdrantService


embedding_service = EmbeddingService()
qdrant = QdrantService()


questions = [
    "车型2一次最多可以装多少件货物？",
    "车型2的空间利用率是多少？",
    "问题二采用了什么优化策略？",
]


for question in questions:
    print("\n" + "=" * 60)
    print(f"Question: {question}")

    query_vector = embedding_service.embed_text(
        question
    )

    results = qdrant.search(
        query_vector=query_vector,
        limit=5,
    )

    for rank, result in enumerate(
        results,
        start=1,
    ):
        payload = result.payload or {}

        print(
            f"\nRank {rank}"
            f"\nScore: {result.score:.4f}"
            f"\nPage: {payload.get('page_number')}"
            f"\nChunk: {payload.get('chunk_index')}"
            f"\nText: "
            f"{payload.get('text', '')[:300]}"
        )