import re

from app.schemas.parser import ParsedDocument, ParsedPage


class DocumentPreprocessor:
    TOC_LINE_PATTERN = re.compile(
        r"^\s*\d+(\.\d+)*\s+.+[.…]{3,}\s*\d+\s*$"
    )

    @staticmethod
    def process(document: ParsedDocument) -> ParsedDocument:
        pages: list[ParsedPage] = []

        for page in document.pages:
            cleaned_text = DocumentPreprocessor._clean_page(
                page.text
            )

            if cleaned_text:
                pages.append(
                    ParsedPage(
                        page_number=page.page_number,
                        text=cleaned_text,
                    )
                )

        return ParsedDocument(
            document_id=document.document_id,
            filename=document.filename,
            pages=pages,
        )

    @staticmethod
    def _clean_page(text: str) -> str:
        cleaned_lines: list[str] = []

        for line in text.splitlines():
            stripped = line.strip()

            if not stripped:
                continue

            # 删除单独出现的页码
            if stripped.isdigit():
                continue

            # 删除明显的目录项，例如：
            # 1.1 问题背景..................................1
            # 5.2 模型建立..................................5
            if DocumentPreprocessor.TOC_LINE_PATTERN.match(
                stripped
            ):
                continue

            # 删除纯点线/省略号噪声
            if (
                re.fullmatch(r"[.…\s]{3,}", stripped)
                or re.fullmatch(r"\.+", stripped)
            ):
                continue

            cleaned_lines.append(stripped)

        return "\n".join(cleaned_lines).strip()