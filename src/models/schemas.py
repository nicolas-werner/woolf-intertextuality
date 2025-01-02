from typing import List, Literal
from pydantic import BaseModel, Field

# Type Definitions
ConfidenceLevel = Literal["low", "medium", "high"]
ConnectionType = Literal[
    "intertextual",    # Direct presence through quotation, allusion, or plagiarism
    "hypertextual"     # Transformation or adaptation of earlier text
]

class ThinkingStep(BaseModel):
    """A step in the analytical thinking process following Genette's framework."""
    step_number: int = Field(
        description="Sequential number of this thinking step"
    )
    thought: str = Field(
        description=(
            "Current analytical consideration. For example:\n"
            "- First examining text for direct references (intertextuality)\n"
            "- Then considering possible transformations (hypertextuality)\n"
            "- Analyzing the significance of identified connections\n"
            "- Evaluating how the connection contributes to meaning"
        )
    )
    action: str = Field(
        description=(
            "Specific analysis being performed. For example:\n"
            "- Close reading of specific passages\n"
            "- Comparing textual elements\n"
            "- Analyzing transformation techniques\n"
            "- Examining contextual significance"
        )
    )
    result: str = Field(
        description=(
            "What was discovered in this step. For example:\n"
            "- Identified specific textual parallel\n"
            "- Found transformation of Homeric element\n"
            "- Discovered pattern of adaptation\n"
            "- Recognized significant variation"
        )
    )
    next_thought: str = Field(
        description=(
            "Based on this result, what should be considered next. For example:\n"
            "- Examine how this connection creates new meaning\n"
            "- Analyze how transformation serves Woolf's purposes\n"
            "- Consider broader patterns of engagement\n"
            "- Evaluate significance within modernist context"
        )
    )
    confidence: ConfidenceLevel = Field(
        description=(
            "Confidence in this step's conclusion:\n"
            "- low: Speculative or requires more evidence\n"
            "- medium: Clear connection but interpretive questions remain\n"
            "- high: Strong textual and theoretical support"
        )
    )

class Connection(BaseModel):
    """Details of a specific intertextual connection based on Genette's framework."""
    connection_type: ConnectionType = Field(
        description=(
            "The type of transtextual relationship identified:\n"
            "- intertextual: 'Effective presence of one text within another' through "
            "quotation, allusion, or similar phrases\n"
            "- hypertextual: 'Transformation or adaptation of an earlier text (hypotext) "
            "into a new text (hypertext)'"
        )
    )
    text1_evidence: str = Field(
        description=(
            "Relevant passage from the Odyssey (hypotext), including:\n"
            "- Specific quotation or description\n"
            "- Context within the Odyssey\n"
            "- Significant elements or motifs"
        )
    )
    text2_evidence: str = Field(
        description=(
            "Relevant passage from Mrs. Dalloway (hypertext), showing:\n"
            "- How Woolf incorporates or transforms the Homeric material\n"
            "- Context within Mrs. Dalloway\n"
            "- Significance of the adaptation"
        )
    )
    explanation: str = Field(
        description=(
            "Analysis of the transtextual relationship, including:\n"
            "- Nature of the connection (direct reference or transformation)\n"
            "- How Woolf adapts or reinterprets Homer\n"
            "- Purpose and effect of the connection\n"
            "- Contribution to broader themes and meanings"
        )
    )
    confidence: ConfidenceLevel = Field(
        description=(
            "Confidence level in this connection:\n"
            "- low: Possible but requires more evidence\n"
            "- medium: Clear connection but questions about significance remain\n"
            "- high: Well-supported connection with clear literary significance"
        )
    )

class Analysis(BaseModel):
    """The complete transtextual analysis following Genette's framework."""
    initial_observations: str = Field(
        description=(
            "Preliminary analysis of the passages, including:\n"
            "- Initial identification of potential connections\n"
            "- Notable patterns of reference or transformation\n"
            "- Key themes or motifs that suggest relationship"
        )
    )
    
    thinking_steps: List[ThinkingStep] = Field(
        description=(
            "Systematic analysis process, showing:\n"
            "- Application of theoretical framework\n"
            "- Close reading and comparison\n"
            "- Development of interpretation\n"
            "- Critical evaluation of evidence and significance"
        )
    )
    
    connections: List[Connection] = Field(
        description=(
            "Detailed analysis of each transtextual relationship, examining:\n"
            "- Type of connection (intertextual/hypertextual)\n"
            "- Evidence from both texts\n"
            "- Nature of transformation or reference\n"
            "- Literary and theoretical significance"
        )
    )
    
    evaluation: dict = Field(
        description="Critical evaluation of the transtextual relationships",
        example={
            "intentionality": "Analysis of deliberate engagement with Homer",
            "significance": "Literary and theoretical importance of connections",
            "interpretation": "How connections contribute to meaning",
            "uncertainties": "Areas requiring further investigation"
        }
    )
    
    summary: dict = Field(
        description="Synthesis of analysis",
        example={
            "meaningful_relationship": bool,
            "primary_connection_type": ConnectionType,
            "key_evidence": "Most significant textual evidence",
            "transformation_analysis": "How Woolf engages with and transforms Homer",
            "literary_significance": "Broader implications for interpretation"
        }
    )


