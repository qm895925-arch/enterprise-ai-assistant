from app.services.document_parser import DocumentParser
from app.services.document_preprocessor import DocumentPreprocessor


document = DocumentParser.parse(
    document_id="doc_f500c22a",
    filename="DMC2606016.pdf",
    file_path="data/uploads/doc_f500c22a.pdf",
)

processed = DocumentPreprocessor.process(document)

print(f"Original pages: {len(document.pages)}")
print(f"Processed pages: {len(processed.pages)}")

for page in processed.pages[:5]:
    print(f"\n--- Page {page.page_number} ---")
    print(page.text[:1000])