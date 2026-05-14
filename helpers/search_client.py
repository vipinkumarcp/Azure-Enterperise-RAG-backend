from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential

from core.config import settings

credential = DefaultAzureCredential()

search_client = SearchClient(
    endpoint=settings.AZURE_SEARCH_ENDPOINT,
    index_name=settings.AZURE_SEARCH_INDEX,
    credential=credential
)