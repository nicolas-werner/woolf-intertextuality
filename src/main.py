import os
from pathlib import Path
from haystack import Document
from rich.console import Console
import pandas as pd
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
    
    # Prepare list to store results
    results = []
    
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
            
            # Store results
            result = {
                'dalloway_text': query,
                'odyssey_text': doc.content,
                'odyssey_chapter': doc.meta['chapter'],
                'similarity_score': doc.score,
                'is_reference': analysis.reference.is_reference,
                'reference_type': analysis.reference.reference_type,
                'confidence': analysis.reference.confidence,
                'textual_codes': ','.join(sorted(analysis.reference.textual_codes)),
                'explanation': analysis.reference.explanation,
                'transformation': analysis.reference.transformation,
                'supporting_evidence': ';'.join(analysis.reference.supporting_evidence),
                'initial_observation': analysis.thought_process.initial_observation,
                'contextual_analysis': analysis.thought_process.contextual_analysis,
                'code_identification': ','.join(analysis.thought_process.code_identification),
                'dialogic_analysis': analysis.thought_process.dialogic_analysis,
                'transformation_analysis': analysis.thought_process.transformation_analysis,
                'counter_arguments': ','.join(analysis.thought_process.counter_arguments),
                'synthesis': analysis.thought_process.synthesis
            }
            results.append(result)
            
            # Print analysis results
            console.print("\n[bold blue]Analysis:[/bold blue]")
            console.print(f"[cyan]Is Reference:[/cyan] {analysis.reference.is_reference}")
            if analysis.reference.is_reference:
                console.print(f"[cyan]Type:[/cyan] {analysis.reference.reference_type}")
                console.print(f"[cyan]Confidence:[/cyan] {analysis.reference.confidence}")
                console.print(f"[cyan]Explanation:[/cyan] {analysis.reference.explanation}")
            console.print("\n" + "="*80 + "\n")
    
    # Save results to CSV
    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "intertextual_analysis.csv"
    
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False, encoding='utf-8')
    console.print(f"\n[bold green]✅ Analysis results saved to {output_path}[/bold green]")

if __name__ == "__main__":
    main()
