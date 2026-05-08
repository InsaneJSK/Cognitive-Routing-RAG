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

def phase1_demo():
    from app.testcases import phase1_tests
    upsert_personas()
    output = {}
    for idx, test_post in enumerate(phase1_tests):
        matches = route_post_to_bots(test_post)
        output[f"Test Post {idx+1}"] = {
            "content": test_post,
            "matches": matches
        }
    return output

if __name__ == "__main__":
    from pprint import pprint
    pprint(phase1_demo())
