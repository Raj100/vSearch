import os
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv
import uuid

load_dotenv()

class VectorDB:
    def __init__(self, url, api_key, collection_name):
        self.client = QdrantClient(
            url=url,
            api_key=api_key or None,
            timeout=30
        )
        
        self.collection_name = collection_name
        self._create_collection()

    def _create_collection(self):
        try:
            if not self.client.collection_exists(self.collection_name):
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=256,
                        distance=models.Distance.COSINE
                    )
                )
        except Exception as e:
            print(f"Collection creation failed: {str(e)}")
            raise

    def upsert(self, vector: list, payload: dict):
        try:
                frame_path = payload["frame_path"]
                file_name = os.path.basename(frame_path)
                point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, file_name))
                
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=[
                        models.PointStruct(
                            id=point_id,
                            vector=vector,
                            payload=payload
                        )
                    ]
                )
        except Exception as e:
            print(f"Upsert failed: {str(e)}")
            raise
    def search(self, query_vector: list, limit: int = 5):
        try:
            return self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                with_vectors=True 

            )
        except Exception as e:
            print(f"Search failed: {str(e)}")
            raise

