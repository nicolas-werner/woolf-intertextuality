from typing import List, Literal, Optional, Dict
from pydantic import BaseModel, Field

ConfidenceLevel = Literal["low", "medium", "high"]
TransformationType = Literal["thematic", "structural", "linguistic", "cultural"]
IntersectionType = Literal[
    "intertextual",  # Direct quotations, allusions (Genette)
    "hypertextual",  # Transformative reworkings (Genette)
    "dialogic",  # Dynamic interplay (Kristeva)
    "pragmatic",  # Effective presence (Schubert)
]


class TextualIntersection(BaseModel):
    """Represents how texts intersect and transform each other."""

    surface_elements: List[str] = Field(
        description="Specific textual elements (e.g., words, themes, motifs) that create intertextual networks."
    )
    transformation: TransformationType = Field(
        description="How Odyssey elements are transformed in Mrs. Dalloway's modernist context."
    )
    dialogic_aspects: IntersectionType = Field(
        description="Type of intertextual relationship based on Kristeva, Genette, and Schubert's theories."
    )
    meaning_transformation: str = Field(
        description="Analysis of how meaning emerges through textual interactions and transformations."
    )
    feminist_reimagining: str = Field(
        description="How Woolf reinterprets male-centric narratives from a feminist perspective.",
        default=None,
    )
    integration_technique: str = Field(
        description="How Woolf subtly integrates the reference (e.g., hermetic, structural, thematic).",
        default=None,
    )


class AnalysisStep(BaseModel):
    """Represents a step in the thought process of intertextual analysis."""

    step_description: str = Field(
        description="Description of the analysis performed at this step."
    )
    evidence: str = Field(
        description="supporting evidence or reasoning for this step.", default=None
    )


class AnalysisThoughtProcess(BaseModel):
    """Represents the thought process for analyzing intertextual relationships."""

    initial_observation: str = Field(
        description="Initial observations about textual networks and relationships."
    )
    analytical_steps: List[AnalysisStep] = Field(
        description="Step-by-step reasoning process."
    )
    counter_arguments: List[str] = Field(
        description="Potential counterarguments or alternative interpretations."
    )
    synthesis: str = Field(
        description="Synthesis of how texts create meaning through their interactions."
    )
    theoretical_grounding: Optional[Dict[str, str]] = Field(
        description="How the analysis applies Kristeva, Genette, and Schubert's theories.",
        default_factory=dict,
    )


class IntertextualConnections(BaseModel):
    """Detailed analysis of intertextual relationships between text passages."""

    is_meaningful: bool = Field(
        description="Whether the texts create meaningful networks of significance."
    )
    confidence: ConfidenceLevel = Field(
        description="Confidence level in the intertextual identification."
    )
    intersections: List[TextualIntersection] = Field(
        description="Points of intersection in the dynamic network of textual relationships."
    )
    supporting_evidence: List[str] = Field(
        description="Evidence of textual absorption, transformation, and dialogue."
    )


class IntertextualAnalysis(BaseModel):
    """Complete analysis of intertextual relationships between text passages."""

    thought_process: AnalysisThoughtProcess = Field(
        description="Detailed reasoning behind the intertextual analysis."
    )
    structured_analysis: IntertextualConnections = Field(
        description="Structured analysis of the identified intertextual connection."
    )
    critique: Optional[str] = Field(
        default=None,
        description="critical evaluation of the analysis process or results whether it is a meaningful intertextual connection or not",
    )
