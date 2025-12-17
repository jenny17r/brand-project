from app.rag.retriever import FestivalRetriever

retriever = FestivalRetriever()

results = retriever.search(
    query="festival in Tamil Nadu for cafe promotion",
    limit=3
)

print("🔍 Retrieved festivals:")
for r in results:
    print("-", r["name"], "|", r["region"])
