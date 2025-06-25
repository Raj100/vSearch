import os
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

qdrant = VectorDB(
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    api_key=os.getenv("QDRANT_API_KEY", None),
    collection_name=os.getenv("COLLECTION_NAME", "video_frames")
)

@app.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    interval: int = Form(1, description="Frame extraction interval in seconds")
):
    try:
        print("hello")