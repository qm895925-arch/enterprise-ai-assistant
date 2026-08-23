from pydantic import BaseModel


class ParsedPage(BaseModel):
    page_number: int
    text: str


class ParsedDocument(BaseModel):
    document_id: str
    filename: str
    pages: list[ParsedPage]