from azure.identity.aio import DefaultAzureCredential
from openai import AsyncAzureOpenAI
from core.config import settings
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import os

credential = DefaultAzureCredential()

token_provider = get_bearer_token_provider(
    credential,
    "https://cognitiveservices.azure.com/.default"
)

client = AsyncAzureOpenAI(
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
    azure_ad_token_provider=token_provider,
    api_version="2024-12-01-preview"
)



async def generate_embedding(text: str):

    response = await client.embeddings.create(
        model=settings.AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        input=text,
        dimensions= 1536
    )

    return response.data[0].embedding