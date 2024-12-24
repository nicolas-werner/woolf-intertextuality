import os
import argparse
from pathlib import Path
from haystack import Document
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeRemainingColumn
import pandas as pd
from datetime import datetime
from src.pipeline.pipeline_facade import PipelineFacade
from src.data_preparation.data_manager import DataManager
from src.config.settings import settings
from typing import List
from sklearn.metrics.pairwise import cosine_similarity
from src.evaluation.prepare_annotation_data import prepare_annotation_csv

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

def display_settings_table():
    """Display analysis settings in a formatted table"""
    table = Table(title="Analysis Settings")
    
    table.add_column("Parameter", style="cyan", no_wrap=True)
    table.add_column("Value", style="green")
    
    table.add_row("LLM Model", settings.llm.model)
    table.add_row("Prompt Template", settings.llm.prompt_template)
    table.add_row("Temperature", str(settings.llm.temperature))
    table.add_row("Max Tokens", str(settings.llm.max_tokens))
    table.add_row("Chunk Size", str(settings.preprocessing.chunk_size))
    table.add_row("Chunk Overlap", str(settings.preprocessing.chunk_overlap))
    
    console.print(table)

def get_dissimilar_chunks(query_embedding: List[float], docs: List[Document], k: int = 2) -> List[Document]:
    """Find the k most dissimilar chunks based on cosine similarity
    
    Args:
        query_embedding: Embedding vector of query text
        docs: List of documents to search
        k: Number of dissimilar chunks to return
    """
    # Calculate similarities
    for doc in docs:
        doc.score = 1 - cosine_similarity(query_embedding, doc.embedding)
    
    # Sort by dissimilarity (highest score = most dissimilar)
    sorted_docs = sorted(docs, key=lambda x: x.score, reverse=True)
    return sorted_docs[:k]

def main():
    args = parse_args()
    
    # Display settings table
    display_settings_table()
    
    # Initialize components
    data_manager = DataManager()
    pipeline = PipelineFacade()
    
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
    
    # Process each chunk from Mrs Dalloway with progress bar
    total_queries = len(query_chunks)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeRemainingColumn(),
        console=console,
        transient=False  # Make progress bar sticky
    ) as progress:
        # Main analysis task
        analysis_task = progress.add_task(
            f"[cyan]Processing Mrs Dalloway chunks...", 
            total=total_queries
        )
        
        for i, query_doc in enumerate(query_chunks, 1):
            query_text = query_doc.content
            
            # Find similar passages
            similar_docs = pipeline.find_similar_passages(query_text)
            
            # Analyze each similar passage
            for j, doc in enumerate(similar_docs, 1):
                # Update progress description for each similar chunk
                progress.update(
                    analysis_task,
                    description=f"[cyan]Analyzing similar chunk {j}/{len(similar_docs)} of Dalloway chunk {i}/{total_queries}"
                )
                
                # Perform intertextual analysis
                analysis = pipeline.analyze_similarity(query_text, doc)
                
                # Store results
                result = {
                    'dalloway_text': query_text,
                    'odyssey_text': doc.content,
                    'odyssey_chapter': doc.meta['chapter'],
                    'similarity_score': doc.score,
                    'similarity_type': doc.meta.get('similarity_type', 'similar'),  # Add similarity type
                    'prompt_type': settings.llm.prompt_template,  # Add prompt type
                    
                    # Thought Process
                    'initial_observation': analysis.thought_process.initial_observation,
                    'analytical_steps': [
                        {
                            'step_description': step.step_description,
                            'evidence': step.evidence
                        } for step in analysis.thought_process.analytical_steps
                    ],
                    'counter_arguments': ';'.join(analysis.thought_process.counter_arguments),
                    'synthesis': analysis.thought_process.synthesis,
                    
                    # Structured Analysis
                    'is_meaningful': analysis.structured_analysis.is_meaningful,
                    'confidence': analysis.structured_analysis.confidence,
                    'textual_intersections': [
                        {
                            'surface_elements': ';'.join(intersection.surface_elements),
                            'transformation': intersection.transformation,
                            'dialogic_aspects': intersection.dialogic_aspects,
                            'meaning_transformation': intersection.meaning_transformation
                        }
                        for intersection in analysis.structured_analysis.intersections
                    ],
                    'supporting_evidence': ';'.join(analysis.structured_analysis.supporting_evidence),
                    'critique': analysis.critique
                }
                results.append(result)
            
            # Update progress
            progress.update(analysis_task, advance=1)
    
    # Save results to CSV with timestamp
    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_filename = get_timestamped_filename(f"intertextual_analysis_{settings.llm.prompt_template}_{settings.llm.model}.csv")
    output_path = output_dir / output_filename
    
    # Convert results directly to DataFrame
    df = pd.DataFrame(results)
    
    # Extract the first textual intersection for each row
    df['textual_intersection'] = df['textual_intersections'].apply(lambda x: x[0] if x else None)
    
    # Convert the dictionary in textual_intersection to separate columns
    intersection_df = pd.DataFrame(df['textual_intersection'].tolist())
    
    # Drop the original columns and combine with the intersection details
    df = df.drop(['textual_intersections', 'textual_intersection'], axis=1).join(intersection_df)
    
    # Reorder columns
    column_order = [
        # Core text chunks
        'dalloway_text', 
        'odyssey_text',
        'odyssey_chapter',
        'similarity_score',
        'similarity_type',  # Added to distinguish similar/dissimilar pairs
        'prompt_type',      # Added to track naive/expert prompt
        
        # Analysis results
        'is_meaningful',
        'confidence',
        
        # Thought process
        'initial_observation',
        'analytical_steps',  # Added from AnalysisThoughtProcess
        'counter_arguments',
        'synthesis',
        
        # Textual intersections
        'surface_elements',
        'transformation',
        'dialogic_aspects',
        'meaning_transformation',
        
        # Evidence and critique
        'supporting_evidence',
        'critique'          # Added optional critique field
    ]
    
    # Reorder columns and handle any missing columns
    existing_columns = [col for col in column_order if col in df.columns]
    remaining_columns = [col for col in df.columns if col not in column_order]
    final_column_order = existing_columns + remaining_columns
    
    df = df[final_column_order]
    
    df.to_csv(output_path, index=False, encoding='utf-8')
    console.print(f"\n[bold green]✅ Analysis results saved to {output_path}[/bold green]")
    
    # Prepare annotation version
    annotation_path = prepare_annotation_csv(output_path)
    console.log(f"[green]✓[/green] Prepared annotation file: {annotation_path}")

if __name__ == "__main__":
    main()
