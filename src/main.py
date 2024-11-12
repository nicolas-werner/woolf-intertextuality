import os
import argparse
from pathlib import Path
from haystack import Document
from rich.console import Console
import pandas as pd
from datetime import datetime
from src.pipeline.intertextuality_pipeline import IntertextualityPipeline
from src.data_preparation.data_manager import DataManager

console = Console()

def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze intertextual references between Mrs Dalloway and The Odyssey"
    )
    parser.add_argument(
        "--limit", 
        type=int, 
        help="Limit the number of Dalloway queries to process",
        default=None
    )
    return parser.parse_args()

def get_timestamped_filename(base_name: str) -> str:
    """Create filename with ISO timestamp suffix"""
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    name, ext = os.path.splitext(base_name)
    return f"{name}_{timestamp}{ext}"

def main():
    args = parse_args()
    
    # Initialize components
    data_manager = DataManager()
    pipeline = IntertextualityPipeline()
    
    # Load data
    console.log("📚 Loading and preparing documents")
    query_chunks, odyssey_docs = data_manager.load_data()
    
    # Apply limit if specified
    if args.limit:
        console.log(f"[yellow]Limiting analysis to first {args.limit} queries[/yellow]")
        query_chunks = query_chunks[:args.limit]
    
    # Index Odyssey documents
    pipeline.index_documents(odyssey_docs)
    
    # Prepare list to store results
    results = []
    
    # Process each chunk from Mrs Dalloway
    total_queries = len(query_chunks)
    console.print(f"\n[bold]Analyzing {total_queries} Mrs Dalloway chunks:[/bold]")
    
    for i, query_doc in enumerate(query_chunks, 1):
        query_text = query_doc.content
        console.print(f"\n[cyan]Query {i}/{total_queries}:[/cyan] {query_text[:100]}...")
        
        # Find similar passages
        similar_docs = pipeline.find_similar_passages(query_text)
        
        # Analyze each similar passage
        for doc in similar_docs:
            console.print(f"\n[magenta]Chapter:[/magenta] {doc.meta['chapter']}")
            console.print(f"[yellow]Content:[/yellow] {doc.content[:200]}...")
            console.print(f"[green]Score:[/green] {doc.score:.4f}")
            
            # Perform intertextual analysis
            analysis = pipeline.analyze_similarity(query_text, doc)
            
            # Store results
            result = {
                'dalloway_text': query_text,
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
    
    # Save results to CSV with timestamp
    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_filename = get_timestamped_filename("intertextual_analysis.csv")
    output_path = output_dir / output_filename
    
    df = pd.DataFrame(results)
    df.to_csv(output_path, index=False, encoding='utf-8')
    console.print(f"\n[bold green]✅ Analysis results saved to {output_path}[/bold green]")

if __name__ == "__main__":
    main()
