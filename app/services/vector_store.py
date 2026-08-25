from uuid import NAMESPACE_URL, uuid5

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)


class QdrantService:
    COLLECTION_NAME = "enterprise_documents"
    VECTOR_SIZE = 512

    def __init__(self):
        self.client = QdrantClient(
            url="http://localhost:6333"
        )

    def create_collection(self) -> None:
        collections = self.client.get_collections()

        exists = any(
            collection.name == self.COLLECTION_NAME
            for collection in collections.collections
        )

        if exists:
            return

        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=VectorParams(
                size=self.VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )

    def upsert_point(
        self,
        point_id: str,
        vector: list[float],
        payload: dict,
    ) -> None:
        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload,
                )
            ],
        )

    def upsert_chunks(
        self,
        chunks,
        vectors: list[list[float]],
    ) -> None:
        if len(chunks) != len(vectors):
            raise ValueError(
                "chunks and vectors must have the same length"
            )

        points = []

        for chunk, vector in zip(chunks, vectors):
            point_id = str(
                uuid5(
                    NAMESPACE_URL,
                    chunk.chunk_id,
                )
            )

            points.append(
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={
                        "chunk_id": chunk.chunk_id,
                        "document_id": chunk.document_id,
                        "filename": chunk.filename,
                        "page_number": chunk.page_number,
                        "chunk_index": chunk.chunk_index,
                        "text": chunk.text,
                    },
                )
            )

        if points:
            self.client.upsert(
                collection_name=self.COLLECTION_NAME,
                points=points,
            )

    def search(
        self,
        query_vector: list[float],
        limit: int = 5,
    ):
        result = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=query_vector,
            limit=limit,
            with_payload=True,
        )

        return result.points