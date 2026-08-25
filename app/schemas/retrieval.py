from pydantic import BaseModel


class RetrievalResult(BaseModel):
    score: float
    document_id: str
    filename: str
    page_number: int
    chunk_index: int
    text: str