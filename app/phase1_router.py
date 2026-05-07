import chromadb
from sentence_transformers import SentenceTransformer
from app.personas import BOT_PERSONAS

#Setup ChromaDB and SentenceTransformer
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="bot_personas",
    metadata={"hnsw:space": "cosine"}
)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def upsert_personas():
    """Upsert bot personas into ChromaDB collection with their embeddings."""
    for bot in BOT_PERSONAS:
        embedding = embedding_model.encode(
            bot["persona"],
            normalize_embeddings=True
            ).tolist()
        collection.upsert(
            ids=[bot["bot_id"]],
            documents=[bot["persona"]],
            embeddings=[embedding],
            metadatas=[{"name": bot["name"]}],
        )

def route_post_to_bots(post_content: str, threshold: float = 0.4):
    """Route a post to the most relevant bots based on cosine similarity."""
    post_embedding = embedding_model.encode(
        post_content,
        normalize_embeddings=True
    ).tolist()
    results = collection.query(
        query_embeddings=[post_embedding],
        n_results=3,
    )
    matches = []
    if results["ids"][0] == []:
        return matches
    for idx, distance in enumerate(results["distances"][0]):
        similarity = 1 - distance  # Convert cosine distance to similarity
        if similarity >= threshold:
            matches.append((results["ids"][0][idx], results["metadatas"][0][idx]["name"], similarity))
    return matches

if __name__ == "__main__":
    upsert_personas()
    tests = [
        "I think AI will revolutionize the world and we should embrace it. However, we should also be cautious about potential risks and ethical concerns.",
        "Tech monopolies are exploiting user data while social media platforms destroy attention spans and personal privacy.",
        "With the onset of AI, we can see the RoI in software development skyrocketing, with huge potential for economy to grow.",
    ]

    for test_post in tests:
        print(f"{test_post}: {route_post_to_bots(test_post)}")
