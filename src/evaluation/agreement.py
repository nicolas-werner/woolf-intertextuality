from typing import List
import pandas as pd
import numpy as np
from krippendorff import alpha
from sklearn.metrics import cohen_kappa_score


def calculate_agreement_metrics(
    annotation_files: List[str], answer_key_path: str
) -> dict:
    """Calculate inter-annotator agreement metrics

    Args:
        annotation_files: List of paths to annotator CSV files
        answer_key_path: Path to answer key CSV

    Returns:
        Dictionary containing agreement metrics
    """
    # Load annotations
    annotator_dfs = [pd.read_csv(f) for f in annotation_files]
    answer_key = pd.read_csv(answer_key_path)

    # Calculate metrics
    results = {"accuracy": [], "cohen_kappa": [], "krippendorff_alpha": None}

    # Prepare data for Krippendorff's alpha
    classifications = np.array(
        [
            df["classified_as"].map({"naive": 0, "expert": 1}).values
            for df in annotator_dfs
        ]
    )

    # Calculate Krippendorff's alpha if we have multiple annotators
    if len(annotator_dfs) > 1:
        results["krippendorff_alpha"] = alpha(
            reliability_data=classifications, level_of_measurement="nominal"
        )

    # Calculate accuracy and Cohen's kappa for each annotator
    true_labels = answer_key["true_prompt_type"].map({"naive": 0, "expert": 1}).values

    for i, df in enumerate(annotator_dfs):
        pred_labels = df["classified_as"].map({"naive": 0, "expert": 1}).values

        results["accuracy"].append(np.mean(pred_labels == true_labels))
        results["cohen_kappa"].append(cohen_kappa_score(true_labels, pred_labels))

    return results
