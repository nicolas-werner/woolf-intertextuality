from typing import List, Literal
from pydantic import BaseModel, Field

ConfidenceLevel = Literal["low", "medium", "high"]

class AnalysisThoughtProcess(BaseModel):
    """Chain of thought reasoning process for intertextual analysis"""
    initial_observation: str = Field(
        description="Initial observations about textual similarities, including linguistic echoes, thematic resonances, and structural parallels"
    )
    contextual_analysis: str = Field(
        description="Analysis of how each text functions within its historical, cultural, and literary context, and how these contexts interact"
    )
    code_identification: List[str] = Field(
        description="Identification of shared literary codes, cultural references, and semiotic systems between the texts"
    )
    dialogic_analysis: str = Field(
        description="Analysis of how the texts engage in dialogue with each other, including how meaning is transformed across contexts"
    )
    transformation_analysis: str = Field(
        description="Analysis of how Woolf's text transforms, subverts, or reinterprets elements from The Odyssey"
    )
    counter_arguments: List[str] = Field(
        description="Potential arguments against the intertextual connection, considering alternative interpretations"
    )
    synthesis: str = Field(
        description="Final synthesis of how the texts create meaning through their interaction and dialogue"
    )

class IntertextualReference(BaseModel):
    """Details of an identified intertextual reference and its characteristics"""
    is_reference: bool = Field(
        description="Whether the textual relationship constitutes a meaningful intertextual connection"
    )
    reference_type: str = Field(
        description="Type of intertextual reference (e.g., allusion, quotation, parody, pastiche, structural echo, thematic parallel)"
    )
    confidence: ConfidenceLevel = Field(
        description="Confidence in the intertextual identification based on textual evidence and scholarly context"
    )
    textual_codes: List[str] = Field(
        description="Literary and cultural codes shared between the texts, including narrative techniques, motifs, and symbolic systems"
    )
    explanation: str = Field(
        description="Detailed explanation of how the texts interact and create meaning through their relationship"
    )
    transformation: str = Field(
        description="Analysis of how Woolf's modernist text transforms classical elements for contemporary meaning"
    )
    supporting_evidence: List[str] = Field(
        description="Textual evidence supporting the intertextual connection, including linguistic, thematic, and structural parallels"
    )

class IntertextualAnalysis(BaseModel):
    """Complete analysis of intertextual relationships between text passages"""
    thought_process: AnalysisThoughtProcess = Field(
        description="Detailed chain of thought analysis examining the intertextual relationship"
    )
    reference: IntertextualReference = Field(
        description="Structured analysis of the identified intertextual connection and its characteristics"
    ) 