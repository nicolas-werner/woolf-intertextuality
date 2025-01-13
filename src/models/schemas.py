from typing import List, Literal
from pydantic import BaseModel, Field

# Type Definitions
ConfidenceLevel = Literal["low", "medium", "high"]
ConnectionType = Literal[
    "intertextual",    # Direct presence through quotation, allusion, or plagiarism
    "hypertextual",     # Transformation or adaptation of earlier text
    "none"  # No connection found
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
    confidence: ConfidenceLevel = Field(
        description=(
            "Confidence in this step's conclusion:\n"
            "- low: Speculative or requires more evidence\n"
            "- medium: Clear connection but interpretive questions remain\n"
            "- high: Strong textual and theoretical support"
        )
    )
    next_thought: str = Field(
        description=(
            "Based on this result, what should be considered next. For example:\n"
            "- Examine how this connection creates new meaning\n"
            "- Analyze how transformation serves Woolf's purposes\n"
            "- Consider broader patterns of engagement\n"
            "- Evaluate significance within modernist context\n"
            "- If no further thoughts are needed: 'I can't think of anything else. No further thoughts needed'"
        )
    )
    

class Connection(BaseModel):
    """Details of a specific transtextual relationship based on Genette's framework."""
    connection_type: ConnectionType = Field(
        description=(
            "The type of transtextual relationship identified:\n"
            "- intertextual: 'Effective presence of one text within another' through "
            "quotation, allusion, or plagiarism\n"
            "- hypertextual: 'Transformation or adaptation of an earlier text (hypotext) "
            "into a new text (hypertext)'\n"
            "- none: No connection found"
        )
    )
    text1_evidence: str = Field(
        description=(
            "Relevant passage from the Odyssey, including:\n"
            "- Specific quotation or description\n"
            "- Context within the Odyssey\n"
            "- Significant elements or motifs"        
            )
    )
    text2_evidence: str = Field(
        description=(
            "Relevant passage from Mrs. Dalloway, showing:\n"
            "- How Woolf incorporates or transforms the Homeric material\n"
            "- Context within Mrs. Dalloway\n"
            "- Significance of the adaptation"
        )
    )
    explanation: str = Field(
        description=(
            "Literary analysis of the potential transtextual relationship, including:\n"
            "- Nature of the connection\n"
            "- How Woolf adapts, references or reinterprets Homer\n"
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

class Evaluation(BaseModel):
    """Critical evaluation of the potential transtextual relationships"""
    intentionality: str = Field(
        description="Critical analysis of the intentionality of the connections"
    )
    significance: str = Field(
        description="Synthesis of the significance of the connections"
    )
    interpretation: str = Field(
        description="Possible interpretation of the connections"
    )
    uncertainties: str = Field(
        description="Could the connections be interpreted differently? Is it possible that the connections are not intentional?"
    )
    conclusion: str = Field(
        description="Conclusion on whether a meaningful relationship exists between the texts based on the analysis"
    )
    is_reference: bool = Field(
        description="Whether the connections are references to the Odyssey"
    )

class Analysis(BaseModel):
    """The complete transtextual analysis following Genette's framework."""
    initial_observations: str = Field(
        description=(
            "Preliminary analysis of the passages, including:\n"
            "- Initial identification of potential connections\n"
            "- Notable patterns of reference or transformation\n"
            "- Key elements that could suggest relationship"
        )
    )
    
    thinking_steps: List[ThinkingStep] = Field(
        description=(
            "Systematic analysis process, showing:\n"
            "- Application of theoretical framework\n"
            "- Close reading and comparison\n"
            "- Development of interpretation"
        )
    )
    
    connections: List[Connection] = Field(
        description=(
            "Detailed analysis of each potential transtextual relationship, examining:\n"
            "- Type of connection (intertextual/hypertextual)\n"
            "- Evidence from both texts\n"
            "- Literary and theoretical significance"
        )
    )
    
    evaluation: Evaluation = Field(
        description="Synthesis and evaluation of the analysis"
    )


