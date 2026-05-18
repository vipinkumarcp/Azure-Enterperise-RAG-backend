import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
)

from storage.blob_storage import (
    upload_file_to_blob,
)

from services.ingestion_service import (
    ingest_blob_document,
)

router = APIRouter()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    content = await file.read()

    blob_name = (
        f"{uuid.uuid4()}-{file.filename}"
    )

    blob_url = await upload_file_to_blob(
        blob_name,
        content,
    )

    chunk_count = await ingest_blob_document(
        blob_name
    )

    return {
        "message": "Upload successful",
        "blob_url": blob_url,
        "chunks_indexed": chunk_count,
    }