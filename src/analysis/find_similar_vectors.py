import os
import json
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from rich.console import Console
from rich.table import Table
import openai

console = Console()

def find_similar_vectors(dalloway_file, collection_name, top_k=5):
    console.log("🔗 Connecting to Qdrant")
    client = QdrantClient("localhost", port=6333)

    console.log("🔍 Loading SentenceTransformer model")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    console.log(f"📚 Reading Mrs Dalloway chunks from {dalloway_file}")
    with open(dalloway_file, 'r', encoding='utf-8') as f:
        dalloway_chunks = f.read().split('\n\n')

    console.log("🔎 Searching for similar vectors")
    results = []

    for dalloway_chunk in dalloway_chunks:
        query_vector = model.encode(dalloway_chunk)
        search_result = client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k
        )

        for hit in search_result:
            odyssey_chunk = hit.payload
            similarity_score = hit.score

            # Use OpenAI to analyze the intertextual reference
            analysis = analyze_intertextuality(dalloway_chunk, odyssey_chunk)

            results.append({
                "dalloway_chunk": dalloway_chunk,
                "odyssey_chunk": odyssey_chunk,
                "similarity_score": similarity_score,
                "analysis": analysis
            })

    return results

def analyze_intertextuality(dalloway_chunk, odyssey_chunk):
    prompt = f"""
    Analyze the following two text chunks for potential intertextual references:

    Mrs Dalloway chunk:
    {dalloway_chunk}

    The Odyssey chunk:
    {odyssey_chunk}

    Determine if there is a meaningful intertextual reference between these chunks.
    If yes, briefly explain the connection. If no, state that no significant reference was found.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a literary analyst specializing in intertextuality."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message['content']

def main():
    dalloway_file = os.path.join('data', 'processed', 'mrs_dalloway_processed.txt')
    collection_name = 'odyssey_vectors'
    results = find_similar_vectors(dalloway_file, collection_name)
    
    # Save results to a JSON file
    results_file = os.path.join('results', 'intertextuality_analysis.json')
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    console.print(f"[bold green]✅ Analysis complete. Results saved to {results_file}[/bold green]")

if __name__ == "__main__":
    main()