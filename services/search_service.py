import os

from azure.identity import (
    DefaultAzureCredential,
)

from azure.search.documents.aio import (
    SearchClient,
)

credential = DefaultAzureCredential()

search_client = SearchClient(
    endpoint=os.getenv(
        "AZURE_SEARCH_ENDPOINT"
    ),
    index_name=os.getenv(
        "AZURE_SEARCH_INDEX"
    ),
    credential=credential,
)


async def upload_chunks(documents):

    result = await search_client.upload_documents(
        documents
    )

    return result