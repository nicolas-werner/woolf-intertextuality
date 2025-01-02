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
from src.evaluation.prepare_annotation_data import prepare_annotation_csv
from src.utils.token_counter import TokenCounter
import csv

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


def main():
    args = parse_args()

    # Override prompt template if specified in command line
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
            total=total_queries * 4,  # 2 similar + 2 dissimilar passages per chunk
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

                # Extract the parsed data first for cleaner access
                parsed_analysis = analysis.choices[0].message.parsed
                
                result = {
                    "dalloway_text": query_text,
                    "odyssey_text": doc.content,
                    "odyssey_chapter": doc.meta["chapter"],
                    "similarity_score": doc.score,
                    "similarity_type": doc.meta["similarity_type"],
                    "prompt_type": settings.llm.prompt_template,
                    # Introduction and high-level analysis
                    "introduction": parsed_analysis.introduction,
                    # Process details
                    "initial_observation": parsed_analysis.process.initial_observation,
                    "analytical_steps": [
                        {
                            "step_description": step.step_description,
                            "evidence": step.evidence,
                            "theoretical_reference": step.theoretical_reference,
                            "contrasting_evidence": step.contrasting_evidence,
                        }
                        for step in parsed_analysis.process.steps
                    ],
                    "synthesis": parsed_analysis.process.synthesis_with_implications,
                    "counter_arguments": ";".join(parsed_analysis.process.counterpoints),
                    # Intersection details
                    "confidence": parsed_analysis.intersections.confidence,
                    "textual_intersections": [
                        {
                            "specific_elements": ";".join(intersection.specific_elements),
                            "relationship_types": ";".join(intersection.relationship_types),
                            "transformation_types": ";".join(intersection.transformation_types),
                            "meaning_analysis": intersection.meaning_analysis,
                            "contextual_significance": intersection.contextual_significance,
                            "relationship_evaluation": intersection.relationship_evaluation,
                        }
                        for intersection in parsed_analysis.intersections.intersection_details
                    ],
                    "evidence_passages": ";".join(parsed_analysis.intersections.evidence_passages),
                    "novelty": parsed_analysis.intersections.novelty,
                    # Critique and recommendations
                    "critique": parsed_analysis.critique,
                    "recommendations": parsed_analysis.recommendations,
                }
                results.append(result)

                progress.update(analysis_task, advance=1)

            progress.update(dalloway_task, advance=1)

    output_dir = Path("data/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_filename = get_timestamped_filename(
        f"intertextual_analysis_{settings.llm.prompt_template}_{settings.llm.model}.csv"
    )
    output_path = output_dir / output_filename

    df = pd.DataFrame(results)

    # Simple flattening of textual intersections
    df["textual_intersection"] = df["textual_intersections"].apply(
        lambda x: x[0] if x else None
    )

    intersection_df = pd.DataFrame(df["textual_intersection"].tolist())

    df = df.drop(["textual_intersections", "textual_intersection"], axis=1).join(
        intersection_df
    )

    column_order = [
        # Core text chunks
        "dalloway_text",
        "odyssey_text",
        "odyssey_chapter",
        "similarity_score",
        "similarity_type",
        "prompt_type",
        # Introduction
        "introduction",
        # Process details
        "initial_observation",
        "analytical_steps",
        "synthesis",
        "counter_arguments",
        # Intersection analysis
        "confidence",
        "specific_elements",
        "relationship_types",
        "transformation_types",
        "meaning_analysis",
        "contextual_significance",
        "relationship_evaluation",
        "evidence_passages",
        "novelty",
        # Critique and recommendations
        "critique",
        "recommendations",
    ]

    existing_columns = [col for col in column_order if col in df.columns]
    remaining_columns = [col for col in df.columns if col not in column_order]
    final_column_order = existing_columns + remaining_columns

    df = df[final_column_order]

    # Simple CSV writing
    df.to_csv(output_path, index=False, encoding="utf-8")
    console.print(
        f"\n[bold green]✅ Analysis results saved to {output_path}[/bold green]"
    )

    annotation_path = prepare_annotation_csv(output_path)
    console.log(f"[green]✓[/green] Prepared annotation file: {annotation_path}")

    token_counter.print_usage_report()


if __name__ == "__main__":
    main()
