import os
import argparse
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeRemainingColumn
import pandas as pd
from datetime import datetime
from src.pipeline.pipeline_facade import PipelineFacade
from src.data_preparation.data_manager import DataManager
from src.config.settings import settings
from src.utils.token_counter import TokenCounter
import csv
import json
from haystack import Document
from src.models.schemas import Analysis

console = Console()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze intertextual references between Mrs Dalloway and The Odyssey"
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit the number of Dalloway queries to process",
        default=None,
    )
    parser.add_argument(
        "--prompt-template",
        type=str,
        choices=["expert_prompt", "naive_prompt"],
        help="Choose the prompt template to use (overrides settings.py)",
        default=None,
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


def process_analysis_results(analysis: Analysis, query_text: str, doc: Document):
    """Convert analysis to dictionary format for DataFrame"""
    return {
        "dalloway_text": query_text,
        "odyssey_text": doc.content,
        "odyssey_chapter": doc.meta.get("chapter", ""),
        "similarity_score": doc.score,
        "similarity_type": doc.meta["similarity_type"],
        "prompt_type": settings.llm.prompt_template,
        
        "initial_observations": analysis.initial_observations,
        
        "thinking_steps": json.dumps([step.model_dump() for step in analysis.thinking_steps]),
        "connections": json.dumps([conn.model_dump() for conn in analysis.connections]),
        "evaluation": json.dumps(analysis.evaluation.model_dump()),
    }


def main():
    args = parse_args()

    if args.prompt_template:
        settings.llm.prompt_template = args.prompt_template

    display_settings_table()

    data_manager = DataManager()
    token_counter = TokenCounter()
    pipeline = PipelineFacade(token_counter=token_counter)

    console.log("📚 Loading and preparing documents")
    query_chunks, odyssey_docs = data_manager.load_data()

    if args.limit:
        console.log(f"[yellow]Limiting analysis to first {args.limit} queries[/yellow]")
        query_chunks = query_chunks[: args.limit]

    pipeline.index_documents(odyssey_docs)

    results = []

    total_queries = len(query_chunks)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TimeRemainingColumn(),
        console=console,
        transient=False,
    ) as progress:
        dalloway_task = progress.add_task(
            "[cyan]Processing Mrs Dalloway chunks...", total=total_queries
        )

        analysis_task = progress.add_task(
            "[cyan]Analyzing passages...",
            total=total_queries * 2,  # 1 similar + 1 dissimilar passage per chunk
        )

        for i, query_doc in enumerate(query_chunks, 1):
            query_text = query_doc.content

            progress.update(
                dalloway_task,
                description=f"[cyan]Processing Dalloway chunk {i}/{total_queries}",
            )

            all_docs = pipeline.find_similar_passages(query_text)

            for j, doc in enumerate(all_docs, 1):
                progress.update(
                    analysis_task,
                    description=f"[cyan]Analyzing {doc.meta['similarity_type']} passage {j}/{len(all_docs)} for chunk {i}/{total_queries}",
                )

                analysis = pipeline.analyze_similarity(query_text, doc)
                result = process_analysis_results(analysis, query_text, doc)
                results.append(result)

                progress.update(analysis_task, advance=1)

            progress.update(dalloway_task, advance=1)

    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_filename = get_timestamped_filename(
        f"intertextual_analysis_{settings.llm.prompt_template}_{settings.llm.model}.csv"
    )
    output_path = output_dir / output_filename

    column_order = [
        "dalloway_text",
        "odyssey_text",
        "odyssey_chapter",
        "similarity_score",
        "similarity_type",
        "prompt_type",
        "initial_observations",
        "thinking_steps",
        "connections",
        "evaluation"
    ]

    df = pd.DataFrame(results)
    
    existing_columns = [col for col in column_order if col in df.columns]
    remaining_columns = [col for col in df.columns if col not in column_order]
    df = df[existing_columns + remaining_columns]

    df.to_csv(output_path, index=False, encoding="utf-8")
    console.print(
        f"\n[bold green]✅ Analysis results saved to {output_path}[/bold green]"
    )

    token_counter.print_usage_report()


if __name__ == "__main__":
    main()
