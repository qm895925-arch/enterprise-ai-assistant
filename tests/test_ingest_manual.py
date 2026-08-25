from app.services.chunker import TextChunker
from app.services.document_parser import DocumentParser
from app.services.document_preprocessor import DocumentPreprocessor
from app.services.embedding_service import EmbeddingService
from app.services.vector_store import QdrantService


DOCUMENT_ID = "doc_f500c22a"
FILENAME = "DMC2606016.pdf"
FILE_PATH = "data/uploads/doc_f500c22a.pdf"


# 1. Parse
document = DocumentParser.parse(
    document_id=DOCUMENT_ID,
    filename=FILENAME,
    file_path=FILE_PATH,
)

print(f"Original pages: {len(document.pages)}")


# 2. Preprocess
processed_document = DocumentPreprocessor.process(
    document
)

print(
    f"Processed pages: "
    f"{len(processed_document.pages)}"
)


# 3. Chunk
chunker = TextChunker(
    chunk_size=500,
    chunk_overlap=100,
)

chunks = chunker.split(
    processed_document
)

print(f"Chunk count: {len(chunks)}")


# 4. Embedding
embedding_service = EmbeddingService()

texts = [
    chunk.text
    for chunk in chunks
]

vectors = embedding_service.embed_texts(
    texts
)

print(
    f"Vector count: {len(vectors)}"
)

print(
    f"Vector dimension: "
    f"{len(vectors[0])}"
)


# 5. Qdrant
qdrant = QdrantService()

qdrant.create_collection()

qdrant.upsert_chunks(
    chunks=chunks,
    vectors=vectors,
)

print("Chunks successfully indexed.")