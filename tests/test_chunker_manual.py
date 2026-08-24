from app.services.document_parser import DocumentParser
from app.services.chunker import TextChunker


document = DocumentParser.parse(
    document_id="doc_f500c22a",
    filename="DMC2606016.pdf",
    file_path="data/uploads/doc_f500c22a.pdf",
)

chunker = TextChunker(
    chunk_size=500,
    chunk_overlap=100,
)

chunks = chunker.split(document)

print(f"Page count: {len(document.pages)}")
print(f"Chunk count: {len(chunks)}")

for chunk in chunks[:10]:
    print("\n--- Chunk ---")
    print(f"ID: {chunk.chunk_id}")
    print(f"Page: {chunk.page_number}")
    print(f"Index: {chunk.chunk_index}")
    print(f"Length: {len(chunk.text)}")
    print(chunk.text)