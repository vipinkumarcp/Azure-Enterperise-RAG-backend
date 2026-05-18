from io import BytesIO
import uuid

from pypdf import PdfReader

from storage.blob_storage import (
    download_blob,
)

from services.chunking import (
    chunk_text,
)

from services.embedding_service import (
    generate_embedding,
)

from services.search_service import (
    upload_chunks,
)


async def ingest_blob_document(
    blob_name: str,
):

    blob_data = await download_blob(
        blob_name
    )

    pdf = PdfReader(BytesIO(blob_data))

    text = ""

    for page in pdf.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    chunks = chunk_text(text)

    documents = []

    for chunk in chunks:

        embedding = await generate_embedding(
            chunk
        )

        documents.append({
            "id": str(uuid.uuid4()),
            "content": chunk,
            "sourcefile": blob_name,
            "contentVector": embedding,
        })

    await upload_chunks(documents)

    return len(documents)