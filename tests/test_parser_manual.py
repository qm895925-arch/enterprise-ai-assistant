from app.services.document_parser import DocumentParser


result = DocumentParser.parse(
    document_id="doc_f500c22a",
    filename="DMC2606016.pdf",
    file_path="data/uploads/doc_f500c22a.pdf",
)

print(f"Document ID: {result.document_id}")
print(f"Filename: {result.filename}")
print(f"Page count: {len(result.pages)}")

for page in result.pages:
    print(f"\n--- Page {page.page_number} ---")
    print(f"Text length: {len(page.text)}")
    print(repr(page.text[:500]))