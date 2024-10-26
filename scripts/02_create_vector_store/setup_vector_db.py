import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer
from rich.console import Console
from rich.progress import track

console = Console()

def setup_vector_db(input_file, collection_name):
    console.log("🔗 Connecting to Qdrant")
    client = QdrantClient("localhost", port=6333)

    console.log("🔍 Loading SentenceTransformer model")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    console.log(f"📚 Reading processed Odyssey chunks from {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        chunks = f.read().split('\n\n')

    console.log(f"🗑️ Recreating collection: {collection_name}")
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=model.get_sentence_embedding_dimension(), distance=Distance.COSINE),
    )

    console.log("🔢 Generating embeddings and uploading to Qdrant")
    batch_size = 100
    for i in track(range(0, len(chunks), batch_size), description="Uploading chunks"):
        batch = chunks[i:i+batch_size]
        ids = list(range(i, min(i+batch_size, len(chunks))))
        embeddings = model.encode(batch)
        client.upsert(
            collection_name=collection_name,
            points=zip(ids, embeddings, batch)
        )

    console.log("[bold green]✅ Vector database setup complete![/bold green]")

# Setup vector database for Odyssey
input_file = '../../data_src/odyssey_butcher_processed.txt'
collection_name = 'odyssey_vectors'
setup_vector_db(input_file, collection_name)