import os
from azure.identity.aio import DefaultAzureCredential

from azure.storage.blob.aio import (
    BlobServiceClient,
)

credential = DefaultAzureCredential()

ACCOUNT_URL = (
    f"https://{os.getenv('AZURE_STORAGE_ACCOUNT')}"
    ".blob.core.windows.net"
)

blob_service_client = BlobServiceClient(
    account_url=ACCOUNT_URL,
    credential=credential,
)

container_client = (
    blob_service_client.get_container_client(
        os.getenv("AZURE_STORAGE_CONTAINER")
    )
)


async def upload_file_to_blob(
    file_name: str,
    data: bytes,
):

    blob_client = (
        container_client.get_blob_client(
            blob=file_name
        )
    )

    await blob_client.upload_blob(
        data,
        overwrite=True,
    )

    return blob_client.url


async def download_blob(
    blob_name: str,
) -> bytes:

    blob_client = (
        container_client.get_blob_client(
            blob=blob_name
        )
    )

    stream = await blob_client.download_blob()

    return await stream.readall()