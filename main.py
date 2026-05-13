from fastapi import FastAPI, APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from routes.health import router as health_router
from core.auth import verify_token


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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)