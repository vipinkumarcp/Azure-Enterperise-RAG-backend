from core.config import settings

import os

from dotenv import load_dotenv

from azure.identity import DefaultAzureCredential

from azure.search.documents.indexes import (
    SearchIndexClient,
)

from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
)

load_dotenv()

credential = DefaultAzureCredential()

index_client = SearchIndexClient(
    endpoint=settings.AZURE_SEARCH_ENDPOINT,
    credential=credential
)


fields = [

    SimpleField(
        name="id",
        type=SearchFieldDataType.String,
        key=True,
    ),

    SearchableField(
        name="content",
        type=SearchFieldDataType.String,
    ),

    SearchField(
        name="contentVector",
        type=SearchFieldDataType.Collection(
            SearchFieldDataType.Single
        ),
        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name="default",
    ),

    SearchableField(
        name="sourcefile",
        type=SearchFieldDataType.String,
        filterable=True,
    ),
]

vector_search = VectorSearch(
    algorithms=[
        HnswAlgorithmConfiguration(
            name="default-hnsw"
        )
    ],
    profiles=[
        VectorSearchProfile(
            name="default",
            algorithm_configuration_name="default-hnsw",
        )
    ],
)

index = SearchIndex(
    name=os.getenv("AZURE_SEARCH_INDEX"),
    fields=fields,
    vector_search=vector_search,
)

index_client.create_or_update_index(index)

print("Index created successfully")