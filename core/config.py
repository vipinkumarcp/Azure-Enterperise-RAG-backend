from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    APP_NAME = "RAG FastAPI Backend"

    AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")

    AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")

    API_AUDIENCE = os.getenv("API_AUDIENCE")

    AZURE_OPENAI_ENDPOINT = os.getenv(
        "AZURE_OPENAI_ENDPOINT"
    )

    AZURE_OPENAI_DEPLOYMENT = os.getenv(
        "AZURE_OPENAI_DEPLOYMENT"
    )
    AZURE_SEARCH_ENDPOINT=os.getenv(
        "AZURE_SEARCH_ENDPOINT"
    )

    AZURE_SEARCH_INDEX=os.getenv(
        "AZURE_SEARCH_INDEX"
    )
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv(
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT"
    )


settings = Settings()