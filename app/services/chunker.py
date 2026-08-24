from uuid import uuid4

from app.schemas.chunk import TextChunk
from app.schemas.parser import ParsedDocument


class TextChunker:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
    ):
        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0")

        if chunk_overlap < 0:
            raise ValueError("chunk_overlap must not be negative")

        if chunk_overlap >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(
        self,
        document: ParsedDocument,
    ) -> list[TextChunk]:
        chunks: list[TextChunk] = []

        for page in document.pages:
            page_text_chunks = self._chunk_page(page.text)

            for chunk_index, text in enumerate(page_text_chunks):
                chunks.append(
                    TextChunk(
                        chunk_id=f"chunk_{uuid4().hex[:8]}",
                        document_id=document.document_id,
                        filename=document.filename,
                        page_number=page.page_number,
                        chunk_index=chunk_index,
                        text=text,
                    )
                )

        return chunks

    def _chunk_page(self, text: str) -> list[str]:
        paragraphs = self._split_paragraphs(text)

        chunks: list[str] = []
        current = ""

        for paragraph in paragraphs:
            if len(paragraph) > self.chunk_size:
                if current:
                    chunks.append(current)
                    current = ""

                chunks.extend(
                    self._split_long_text(paragraph)
                )
                continue

            if not current:
                current = paragraph
                continue

            candidate = f"{current}\n\n{paragraph}"

            if len(candidate) <= self.chunk_size:
                current = candidate
            else:
                chunks.append(current)
                current = paragraph

        if current:
            chunks.append(current)

        return chunks

    @staticmethod
    def _split_paragraphs(text: str) -> list[str]:
        return [
            paragraph.strip()
            for paragraph in text.split("\n\n")
            if paragraph.strip()
        ]

    def _split_long_text(self, text: str) -> list[str]:
        chunks: list[str] = []

        start = 0
        step = self.chunk_size - self.chunk_overlap

        while start < len(text):
            end = start + self.chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += step

        return chunks