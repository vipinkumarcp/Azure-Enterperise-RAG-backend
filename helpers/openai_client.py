from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

from core.config import settings

credential = DefaultAzureCredential()

token_provider = get_bearer_token_provider(
    credential,
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
    azure_ad_token_provider=token_provider,
    api_version="2024-12-01-preview"
)