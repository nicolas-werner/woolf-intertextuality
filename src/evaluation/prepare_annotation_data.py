import pandas as pd
from pathlib import Path
import uuid
from rich.console import Console
import csv
import json

console = Console()


def prepare_annotation_csv(results_path: str) -> str:
    """Prepare annotation CSV from analysis results."""
    df = pd.read_csv(results_path)
    
    # Create annotation dataframe with core fields
    annotation_df = pd.DataFrame({
        "dalloway_text": df["dalloway_text"],
        "odyssey_text": df["odyssey_text"],
        "similarity_score": df["similarity_score"],
        "similarity_type": df["similarity_type"],
        
        # Extract key analysis components
        "initial_observations": df["initial_observations"],
        
        # Convert thinking steps from string to structured data
        "thinking_steps": df["thinking_steps"].apply(
            lambda x: json.loads(x) if isinstance(x, str) else x
        ),
        
        # Convert connections from string to structured data
        "connections": df["connections"].apply(
            lambda x: json.loads(x) if isinstance(x, str) else x
        ),
        
        # Extract evaluation components
        "intentionality": df["evaluation"].apply(
            lambda x: json.loads(x)["intentionality"] if isinstance(x, str) else x.get("intentionality")
        ),
        "significance": df["evaluation"].apply(
            lambda x: json.loads(x)["significance"] if isinstance(x, str) else x.get("significance")
        ),
        "interpretation": df["evaluation"].apply(
            lambda x: json.loads(x)["interpretation"] if isinstance(x, str) else x.get("interpretation")
        ),
        "uncertainties": df["evaluation"].apply(
            lambda x: json.loads(x)["uncertainties"] if isinstance(x, str) else x.get("uncertainties")
        ),
        
        # Extract summary components
        "meaningful_relationship": df["summary"].apply(
            lambda x: json.loads(x)["meaningful_relationship"] if isinstance(x, str) else x.get("meaningful_relationship")
        ),
        "primary_connection_type": df["summary"].apply(
            lambda x: json.loads(x)["primary_connection_type"] if isinstance(x, str) else x.get("primary_connection_type")
        ),
        "key_evidence": df["summary"].apply(
            lambda x: json.loads(x)["key_evidence"] if isinstance(x, str) else x.get("key_evidence")
        ),
        "transformation_analysis": df["summary"].apply(
            lambda x: json.loads(x)["transformation_analysis"] if isinstance(x, str) else x.get("transformation_analysis")
        ),
        "literary_significance": df["summary"].apply(
            lambda x: json.loads(x)["literary_significance"] if isinstance(x, str) else x.get("literary_significance")
        ),
    })
    
    # Add annotation columns
    annotation_df["annotator_name"] = ""
    annotation_df["annotation_date"] = ""
    annotation_df["connection_quality"] = ""  # High/Medium/Low
    annotation_df["theoretical_soundness"] = ""  # High/Medium/Low
    annotation_df["evidence_quality"] = ""  # High/Medium/Low
    annotation_df["notes"] = ""
    
    # Save to new file
    output_dir = Path("data/evaluation")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    base_name = Path(results_path).stem
    annotation_path = output_dir / f"{base_name}_annotation.csv"
    
    annotation_df.to_csv(annotation_path, index=False, encoding="utf-8")
    
    return str(annotation_path)
