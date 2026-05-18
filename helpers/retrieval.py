from azure.search.documents.models import VectorizedQuery

from helpers.search_client import search_client
from helpers.embeddings import generate_embedding




async def retrieve_documents(query: str):

    embedding = await generate_embedding(query)

    vector_query = VectorizedQuery(
        vector=embedding,
        k_nearest_neighbors=3,
        fields="contentVector"
    )

    results = search_client.search(
        search_text=None,
        vector_queries=[vector_query],
        select=["content"]
    )

    docs = []

    for result in results:
        docs.append(result["content"])

    return docs