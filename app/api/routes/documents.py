from fastapi import APIRouter, File, HTTPException, UploadFile

from app.schemas.document import DocumentUploadResponse
from app.services.document_service import DocumentService


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...)
):
    try:
        document = await DocumentService.save_upload(file)

        return DocumentUploadResponse(
            document_id=document["document_id"],
            filename=document["filename"],
            status=document["status"],
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc