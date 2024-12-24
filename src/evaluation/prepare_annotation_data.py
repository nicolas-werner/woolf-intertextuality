from typing import List, Dict
import pandas as pd
from pathlib import Path
import random
import uuid

def prepare_annotation_csv(results_file: Path) -> Path:
    """Prepare anonymized results for blind annotation
    
    Args:
        results_file: Path to the original results CSV
    
    Returns:
        Path to the prepared annotation CSV
    """
    # Read original results
    df = pd.read_csv(results_file)
    
    # Generate random IDs for each analysis pair
    df['analysis_id'] = [str(uuid.uuid4()) for _ in range(len(df))]
    
    # Prepare annotation format
    annotation_data = []
    for _, row in df.iterrows():
        annotation_data.append({
            'analysis_id': row['analysis_id'],
            'dalloway_text': row['dalloway_text'],
            'odyssey_text': row['odyssey_text'],
            'initial_observation': row['initial_observation'],
            'textual_intersections': row['textual_intersections'],
            'synthesis': row['synthesis'],
            'supporting_evidence': row['supporting_evidence'],
            # Fields for annotators
            'classified_as': '',  # Annotator fills with 'naive' or 'expert'
            'justification': '',  # Annotator's reasoning
            'thematic_subtleties_noted': '',  # Yes/No + comments
            'surface_similarities_noted': '',  # Yes/No + comments
            'additional_observations': ''
        })
    
    # Create annotation DataFrame
    annotation_df = pd.DataFrame(annotation_data)
    
    # Save to new CSV
    output_dir = Path("data/evaluation")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"annotation_ready_{results_file.stem}.csv"
    annotation_df.to_csv(output_path, index=False)
    
    # Create answer key mapping analysis_ids to their true prompt types
    answer_key = pd.DataFrame({
        'analysis_id': df['analysis_id'],
        'true_prompt_type': df['prompt_type'],
        'similarity_type': df['similarity_type']
    })
    answer_key.to_csv(output_dir / f"answer_key_{results_file.stem}.csv", index=False)
    
    return output_path 