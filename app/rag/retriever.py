from app.rag.embedder import Embedder
from app.rag.qdrant_client import get_qdrant_client, COLLECTION_NAME

class FestivalRetriever:

    def __init__(self):
        self.embedder = Embedder()
        self.client = get_qdrant_client()

    def search(self, query: str, limit: int = 3):
        vector = self.embedder.embed(query)

        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=vector,
            limit=limit,
            with_payload=True
        )

        # results.points is the list of matches
        return [point.payload for point in results.points]
