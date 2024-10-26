import os
from pathlib import Path
from haystack import Document
from rich.console import Console
from pipeline.intertextuality_pipeline import IntertextualityPipeline
from data_preparation.data_manager import DataManager

console = Console()

def main():
    # Initialize components
    data_manager = DataManager()
    pipeline = IntertextualityPipeline()
    
    # Load data
    console.log("📚 Loading and preparing documents")
    query_chunks, odyssey_docs = data_manager.load_data()
    
    # Index Odyssey documents
    pipeline.index_documents(odyssey_docs)
    
    # Process each chunk from Mrs Dalloway
    console.print("\n[bold]Analyzing Mrs Dalloway chunks:[/bold]")
    for i, query in enumerate(query_chunks, 1):
        console.print(f"\n[cyan]Query chunk {i}:[/cyan] {query[:100]}...")
        
        # Find similar passages
        similar_docs = pipeline.find_similar_passages(query)
        
        # Analyze each similar passage
        for doc in similar_docs:
            console.print(f"\n[magenta]Chapter:[/magenta] {doc.meta['chapter']}")
            console.print(f"[yellow]Content:[/yellow] {doc.content[:200]}...")
            console.print(f"[green]Score:[/green] {doc.score:.4f}")
            
            # Perform intertextual analysis
            analysis = pipeline.analyze_similarity(query, doc)
            
            # Print analysis results
            console.print("\n[bold blue]Analysis:[/bold blue]")
            console.print(f"[cyan]Is Reference:[/cyan] {analysis.reference.is_reference}")
            if analysis.reference.is_reference:
                console.print(f"[cyan]Type:[/cyan] {analysis.reference.reference_type}")
                console.print(f"[cyan]Confidence:[/cyan] {analysis.reference.confidence}")
                console.print(f"[cyan]Explanation:[/cyan] {analysis.reference.explanation}")
            console.print("\n" + "="*80 + "\n")

if __name__ == "__main__":
    main()
