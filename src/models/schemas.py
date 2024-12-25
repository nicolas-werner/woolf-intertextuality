from typing import List, Literal, Optional
from pydantic import BaseModel, Field

ConfidenceLevel = Literal["low", "medium", "high"]
TransformationType = Literal["thematic", "structural", "linguistic", "cultural"]
IntersectionType = Literal["direct", "allusive", "structural", "thematic"]


class TextualIntersection(BaseModel):
    """Represents how texts intersect and transform each other."""

    surface_elements: List[str] = Field(
        description="Specific textual elements where the texts intersect (e.g., words, themes, structures, motifs)."
    )
    transformation: TransformationType = Field(
        description="Type of transformation from The Odyssey to Mrs. Dalloway."
    )
    dialogic_aspects: IntersectionType = Field(
        description="Nature of the dialogic relationship between the texts (e.g., direct, thematic)."
    )
    meaning_transformation: str = Field(
        description="Explanation of how meaning evolves when elements are moved from The Odyssey to Mrs. Dalloway's context."
    )


class AnalysisStep(BaseModel):
    """Represents a step in the thought process of intertextual analysis."""

    step_description: str = Field(
        description="Description of the analysis performed at this step."
    )
    evidence: Optional[str] = Field(
        default=None,
        description="Optional supporting evidence or reasoning for this step.",
    )


class AnalysisThoughtProcess(BaseModel):
    """Represents the thought process for analyzing intertextual relationships."""

    initial_observation: str = Field(
        description="Initial observations about textual similarities and resonances."
    )
    analytical_steps: List[AnalysisStep] = Field(
        description="Step-by-step reasoning process for intertextual analysis."
    )
    counter_arguments: List[str] = Field(
        description="Potential counterarguments or alternative interpretations of the relationship."
    )
    synthesis: str = Field(
        description="Final conclusion on whether and how Mrs. Dalloway engages intertextually with The Odyssey."
    )


class IntertextualConnections(BaseModel):
    """Detailed analysis of intertextual relationships between text passages."""

    is_meaningful: bool = Field(
        description="Whether the textual relationship constitutes a meaningful intertextual connection."
    )
    confidence: ConfidenceLevel = Field(
        description="Confidence level in the intertextual identification based on analysis and evidence."
    )
    intersections: List[TextualIntersection] = Field(
        description="Specific points where the texts intersect and transform each other."
    )
    supporting_evidence: List[str] = Field(
        description="Direct textual evidence supporting the intertextual connection."
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
        description="Optional critical evaluation of the analysis process or results.",
    )
