from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME

# Load local embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")  # outputs 384-dim vectors

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Check if index exists
indexes = [i["name"] for i in pc.list_indexes()]
if PINECONE_INDEX_NAME in indexes:
    # Get index description
    desc = pc.describe_index(PINECONE_INDEX_NAME)
    if desc["dimension"] != 384:
        print(f"⚠️ Index dimension mismatch ({desc['dimension']} vs 384). Recreating index...")
        pc.delete_index(PINECONE_INDEX_NAME)
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
else:
    # Create new index
    pc.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

# Connect to index
index = pc.Index(PINECONE_INDEX_NAME)

# Load knowledge base
with open("knowledge_base.txt", "r", encoding="utf-8") as f:
    chunks = [line.strip() for line in f if line.strip()]

# Upload embeddings
for i, chunk in enumerate(chunks):
    embedding = model.encode(chunk).tolist()
    index.upsert(vectors=[{
        "id": str(i),
        "values": embedding,
        "metadata": {"text": chunk}
    }])

print("✅ Knowledge base uploaded successfully!")
