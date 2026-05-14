from helpers.search_client import search_client
from helpers.embeddings import generate_embedding

docs = [
    {
        "id": "1",
        "content": "RAG stands for Retrieval-Augmented Generation."
    },
    {
        "id": "2",
        "content": "Azure AI Search supports vector search."
    }
]

for doc in docs:

    embedding = generate_embedding(doc["content"])

    doc["contentVector"] = embedding

search_client.upload_documents(docs)

print("Documents uploaded")