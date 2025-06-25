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