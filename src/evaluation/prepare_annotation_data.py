import pandas as pd
from pathlib import Path
import uuid
from rich.console import Console

console = Console()


def prepare_annotation_csv(analysis_file: str) -> str:
    """Prepare anonymized version of analysis results for annotation"""
    df = pd.read_csv(analysis_file)

    # Create analysis_id if it doesn't exist
    if "analysis_id" not in df.columns:
        df["analysis_id"] = [str(uuid.uuid4()) for _ in range(len(df))]

    # Create simplified version for annotation
    annotation_data = []
    for _, row in df.iterrows():
        # Handle textual_intersections data
        try:
            textual_intersections = "; ".join(
                [f"{row['surface_elements']} - {row['transformation']}"]
            )
        except (KeyError, TypeError, ValueError) as e:
            console.log(
                f"[yellow]Warning: Could not process textual intersections: {e}[/yellow]"
            )
            textual_intersections = ""

        annotation_data.append(
            {
                "analysis_id": row["analysis_id"],
                "dalloway_text": row["dalloway_text"],
                "odyssey_text": row["odyssey_text"],
                "similarity_score": row["similarity_score"],
                "similarity_type": row["similarity_type"],
                "textual_intersections": textual_intersections,
                "initial_observation": row["initial_observation"],
                "synthesis": row["synthesis"],
            }
        )

    # Create DataFrame
    annotation_df = pd.DataFrame(annotation_data)

    # Create output directory structure
    output_dir = Path("data/evaluation")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Get the base filename without path
    base_filename = Path(analysis_file).name

    # Create output paths
    annotation_path = output_dir / f"annotation_ready_{base_filename}"
    answer_key_path = output_dir / f"answer_key_{base_filename}"

    # Save files
    annotation_df.to_csv(annotation_path, index=False)

    # Create answer key mapping analysis_ids to their true prompt types
    answer_key = pd.DataFrame(
        {
            "analysis_id": df["analysis_id"],
            "true_prompt_type": df["prompt_type"],
            "similarity_type": df["similarity_type"],
        }
    )
    answer_key.to_csv(answer_key_path, index=False)

    console.log(f"[green]✓ Annotation files saved to {output_dir}[/green]")
    return str(annotation_path)
