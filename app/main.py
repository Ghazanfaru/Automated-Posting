
from fastapi import FastAPI

from app.schema import PostingRequest, PostingResponse
from app.services.posting_service import publish_to_all


app = FastAPI(
    title="Automated Multi-Platform Posting API",
    description="Publish messages across multiple platforms.",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {
        "message": "Automated Posting API is running"
    }


@app.post("/posting", response_model=PostingResponse)
async def create_post(request: PostingRequest):
    return await publish_to_all(request.message)