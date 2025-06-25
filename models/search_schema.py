from pydantic import BaseModel

class SearchResponse(BaseModel):
    frame_path: str
    score: float
    vector: list