from typing import List, Literal
from pydantic import BaseModel, Field

ConfidenceLevel = Literal["low", "medium", "high"]

class TextualIntersection(BaseModel):
    """Represents how texts intersect and transform each other"""
    surface_elements: List[str] = Field(
        description="Textual elements where the texts intersect (words, themes, structures, motifs)"
    )
    transformation: str = Field(
        description="How Mrs. Dalloway absorbs and transforms elements from The Odyssey"
    )
    dialogic_aspects: str = Field(
        description="How the texts engage in dialogue with each other and create new meanings"
    )
    differential_meaning: str = Field(
        description="How meanings transform across historical and cultural contexts"
    )

class AnalysisThoughtProcess(BaseModel):
    """Chain of thought reasoning process for intertextual analysis"""
    initial_observation: str = Field(
        description="Initial observations about textual similarities and resonances"
    )
    textual_intersections: List[TextualIntersection] = Field(
        description="Analysis of specific points where texts intersect and transform"
    )
    counter_arguments: List[str] = Field(
        description="Potential arguments against the intertextual connection or alternative interpretations"
    )
    synthesis: str = Field(
        description="Final conclusion about how and why this Mrs. Dalloway passage functions as an intertextual reference to The Odyssey or not"
    )

class IntertextualReference(BaseModel):
    """Analysis of the intertextual relationship between text passages"""
    is_meaningful: bool = Field(
        description="Whether the textual relationship constitutes a meaningful intertextual connection"
    )
    confidence: ConfidenceLevel = Field(
        description="Confidence in the intertextual identification based on similarity and evidence"
    )
    intersections: List[TextualIntersection] = Field(
        description="Points where the texts intersect and transform each other"
    )
    supporting_evidence: List[str] = Field(
        description="Textual evidence supporting the intertextual connection"
    )

class IntertextualAnalysis(BaseModel):
    """Complete analysis of intertextual relationships between text passages"""
    thought_process: AnalysisThoughtProcess = Field(
        description="Chain of thought analysis examining the intertextual relationship"
    )
    reference: IntertextualReference = Field(
        description="Structured analysis of the identified intertextual connection"
    )
