import os
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from models.database import VectorDB
from video_processing.video_processing_main import process_video, compute_histogram
from models.search_schema import SearchResponse

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
        # Save video temporarily
        video_path = f"./temp/temp_{file.filename}"
        with open(video_path, "wb") as f:
            f.write(await file.read())
        
        # Process video and extract frames
        frame_paths = process_video(
            video_path=video_path,
            output_dir="static/frames",
            interval=interval
        )
        # Compute and store feature vectors
        for path in frame_paths:
            vector = compute_histogram(path)
            payload = {"frame_path": path}
            qdrant.upsert(vector=vector, payload=payload)
    
        os.remove(video_path)
        return {"message": f"Processed {len(frame_paths)} frames"}
    except Exception as e:
        raise HTTPException(500, f"Processing failed: {str(e)}")
    
@app.post("/search", response_model=list[SearchResponse])
async def search_similar_frames(
    query_image: UploadFile = File(...),
    limit: int = Form(5, description="Number of results to return")
):
    try:
        # Save query image temporarily
        image_path = f"./temp/temp_{query_image.filename}"
        with open(image_path, "wb") as f:
            f.write(await query_image.read())
        
        # Compute query vector
        query_vector = compute_histogram(image_path)
        os.remove(image_path)
        
        # Search database
        results = qdrant.search(
            query_vector=query_vector,
            limit=limit
        )
        return [
            {
                "frame_path": hit.payload["frame_path"],
                "score": hit.score,
                "vector": hit.vector
            } for hit in results
        ]
    except Exception as e:
        raise HTTPException(500, f"Search failed: {str(e)}")