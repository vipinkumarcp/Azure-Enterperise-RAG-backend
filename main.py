from fastapi import FastAPI, APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from core.config import settings
from routes.health import router as health_router
from core.auth import verify_token
from helpers.openai_client import client
from pydantic import BaseModel
from azure.identity import DefaultAzureCredential


credential = DefaultAzureCredential()
# Create the main FastAPI app
app = FastAPI(title="Azure Search OpenAI", version="1.0.0")




# Add CORS middleware (equivalent to quart_cors)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a router for routes (equivalent to Blueprint)
router = APIRouter()



@router.get("/")
async def say_hi():
    return {"message": "hi welcome to fastapi"}

# Include the router in the app
app.include_router(router)
app.include_router(health_router)

@app.get("/protected")
async def protected_route(
    user=Depends(verify_token)
):
    return {
        "message": "Protected route accessed",
        "user": user
    }

@app.get("/azure-token")
async def get_azure_token():

    token = credential.get_token(
        "https://cognitiveservices.azure.com/.default"
    )

    return {
        "token_preview": token.token[:50],
        "expires_on": token.expires_on
    }

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(
    request: ChatRequest,
    user=Depends(verify_token)
):

    response = client.chat.completions.create(
        model=settings.AZURE_OPENAI_DEPLOYMENT,
        messages=[
            {
                "role": "system",
                "content": "You are an enterprise AI assistant."
            },
            {
                "role": "user",
                "content": request.message
            }
        ],
        temperature=0.7,
        max_tokens=500
    )

    return {
        "response": response.choices[0].message.content
    }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)