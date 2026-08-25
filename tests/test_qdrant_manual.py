from app.services.embedding_service import EmbeddingService
from app.services.vector_store import QdrantService


embedding_service = EmbeddingService()
qdrant = QdrantService()

qdrant.create_collection()

# 1. 写入知识
knowledge = (
    "对于车型2（680×245×250cm），"
    "单车最优装载408件货物，"
    "空间利用率达94.04%。"
)

knowledge_vector = embedding_service.embed_text(
    knowledge
)

qdrant.upsert_point(
    point_id="550e8400-e29b-41d4-a716-446655440000",
    vector=knowledge_vector,
    payload={
        "document_id": "doc_f500c22a",
        "filename": "DMC2606016.pdf",
        "page_number": 1,
        "chunk_index": 0,
        "text": knowledge,
    },
)

# 2. 模拟用户问题
question = "车型2一次最多可以装多少件货物？"

query_vector = embedding_service.embed_text(
    question
)

# 3. 向量检索
results = qdrant.client.query_points(
    collection_name=qdrant.COLLECTION_NAME,
    query=query_vector,
    limit=3,
    with_payload=True,
)

print("=== Retrieval Results ===")

for result in results.points:
    print(f"\nScore: {result.score}")
    print(f"Payload: {result.payload}")