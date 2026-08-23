from app.services.document_parser import DocumentParser


result = DocumentParser.parse(
    document_id="doc_dbfd23c9",
    filename="test.txt",
    file_path="data/uploads/doc_dbfd23c9.txt",
)

print(result.model_dump())