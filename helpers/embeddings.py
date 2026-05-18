from helpers.openai_client import client
from core.config import settings





async def generate_embedding(text: str):

    response = await client.embeddings.create(
        model=settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        input=text,
        dimensions=1536
    )

    return response.data[0].embedding