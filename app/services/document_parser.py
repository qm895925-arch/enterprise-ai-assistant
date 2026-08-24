from pathlib import Path

import pymupdf

from app.schemas.parser import ParsedDocument, ParsedPage


class DocumentParser:
    @staticmethod
    def parse(
        document_id: str,
        filename: str,
        file_path: str,
    ) -> ParsedDocument:
        suffix = Path(filename).suffix.lower()

        if suffix == ".txt":
            return DocumentParser._parse_txt(
                document_id=document_id,
                filename=filename,
                file_path=file_path,
            )

        if suffix == ".pdf":
            return DocumentParser._parse_pdf(
                document_id=document_id,
                filename=filename,
                file_path=file_path,
            )

        raise ValueError(f"Unsupported file type: {suffix}")

    @staticmethod
    def _parse_txt(
        document_id: str,
        filename: str,
        file_path: str,
    ) -> ParsedDocument:
        text = Path(file_path).read_text(
            encoding="utf-8-sig"
        )

        return ParsedDocument(
            document_id=document_id,
            filename=filename,
            pages=[
                ParsedPage(
                    page_number=1,
                    text=text,
                )
            ],
        )

    @staticmethod
    def _parse_pdf(
        document_id: str,
        filename: str,
        file_path: str,
    ) -> ParsedDocument:
        pages: list[ParsedPage] = []

        with pymupdf.open(file_path) as pdf:
            for page_number, page in enumerate(pdf, start=1):
                text = page.get_text("text")

                pages.append(
                    ParsedPage(
                        page_number=page_number,
                        text=text,
                    )
                )

        return ParsedDocument(
            document_id=document_id,
            filename=filename,
            pages=pages,
        )