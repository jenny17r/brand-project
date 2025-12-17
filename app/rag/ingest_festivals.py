from app.rag.embedder import Embedder
from app.rag.qdrant_client import get_qdrant_client, ensure_collection, COLLECTION_NAME

festivals = [
    {
        "name": "Pongal",
        "region": "Tamil Nadu",
        "description": "Harvest festival celebrating gratitude, prosperity, traditional food, sugarcane, and family gatherings.",
        "marketing_angles": [
            "Traditional vibes",
            "Family offers",
            "Local flavors",
            "Morning promotions"
        ]
    },
    {
        "name": "Diwali",
        "region": "India",
        "description": "Festival of lights symbolizing joy, prosperity, gifting, and celebration.",
        "marketing_angles": [
            "Festive offers",
            "Evening ambience",
            "Lights & decor",
            "Celebration moments"
        ]
    }
]

def build_text(festival):
    return f"""
    Festival: {festival['name']}
    Region: {festival['region']}
    Description: {festival['description']}
    Marketing angles: {', '.join(festival['marketing_angles'])}
    """

def ingest():
    embedder = Embedder()
    client = get_qdrant_client()

    ensure_collection(client, vector_size=384)

    points = []

    for idx, fest in enumerate(festivals):
        vector = embedder.embed(build_text(fest))

        points.append({
            "id": idx + 1,
            "vector": vector,
            "payload": fest
        })

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print("✅ Festivals ingested into Qdrant")

if __name__ == "__main__":
    ingest()
