import pandas as pd
from pathlib import Path
import uuid
from rich.console import Console
import csv

console = Console()


def prepare_annotation_csv(analysis_file: str) -> str:
    """Prepare anonymized version of analysis results for annotation"""
    df = pd.read_csv(analysis_file)

    if "analysis_id" not in df.columns:
        df["analysis_id"] = [str(uuid.uuid4()) for _ in range(len(df))]

    annotation_data = []
    for _, row in df.iterrows():
        try:
            textual_intersections = "; ".join(
                [f"{row['specific_elements']} - {row['transformation_types']}"]
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

    annotation_df = pd.DataFrame(annotation_data)
    
    output_dir = Path("data/evaluation")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    base_name = Path(analysis_file).stem
    annotation_path = output_dir / f"annotation_ready_{base_name}.csv"
    
    annotation_df.to_csv(annotation_path, index=False)
    
    return str(annotation_path)
