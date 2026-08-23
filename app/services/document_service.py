from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


ALLOWED_EXTENSIONS = {".pdf", ".txt"}
UPLOAD_DIR = Path("data/uploads")


class DocumentService:
    @staticmethod
    async def save_upload(file: UploadFile) -> dict:
        filename = file.filename or ""

        suffix = Path(filename).suffix.lower()

        if suffix not in ALLOWED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {suffix}. "
                f"Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            )

        document_id = f"doc_{uuid4().hex[:8]}"

        saved_filename = f"{document_id}{suffix}"
        file_path = UPLOAD_DIR / saved_filename

        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        content = await file.read()
        file_path.write_bytes(content)

        return {
            "document_id": document_id,
            "filename": filename,
            "file_path": str(file_path),
            "file_type": suffix.lstrip("."),
            "status": "uploaded",
        }