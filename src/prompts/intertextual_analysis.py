from typing import List, Literal
from pydantic import BaseModel, Field
from pathlib import Path

# Define confidence levels as a literal type
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

def load_system_prompt(scholarly: bool = False) -> str:
    """Load the system prompt from file"""
    prompt_path = Path(__file__).parent / (
        "system_prompt_scholarly.txt" if scholarly else "system_prompt.txt"
    )
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

ANALYSIS_PROMPT = """Analyze the following passages for potential intertextual references:

Mrs Dalloway passage:
{dalloway_text}

The Odyssey passage:
{odyssey_text}
Semantic Similarity Score: {similarity_score}

Follow these steps in your analysis:

1. Initial Observation:
- Note semantic similarities in themes, motifs, or narrative patterns
- Consider how similar meanings are expressed in different ways
- Identify shared concepts or ideas, even if expressed differently

2. Contextual Analysis:
- Examine how each passage functions within its larger narrative
- Consider the thematic role of each passage
- Analyze how similar meanings serve different purposes in each text

3. Literary Techniques:
- Identify how each author conveys similar meanings through different techniques
- Compare modernist vs. classical narrative approaches
- Note how Woolf might transform Homeric techniques

4. Thematic Resonance:
- Analyze how similar themes are treated differently
- Consider how Woolf might be reinterpreting Homeric themes
- Examine how gender and social perspectives influence similar themes

5. Critical Evaluation:
- Consider whether semantic similarities suggest intentional reference
- Evaluate if similarities reflect broader literary/cultural patterns
- Assess whether the similarity score reflects meaningful connections

6. Synthesis:
- Determine if this represents meaningful intertextual dialogue
- Consider how Woolf's modernist perspective transforms classical themes
- Evaluate the significance of any semantic parallels

Remember:
- High semantic similarity doesn't always indicate intentional reference
- Consider how similar meanings can serve different narrative purposes
- Pay attention to how Woolf might transform classical themes
- Consider both explicit and implicit semantic connections
- The similarity score provides context but isn't definitive
"""

def get_analysis_prompt(dalloway_text: str, odyssey_text: str, similarity_score: float) -> str:
    """Get the analysis prompt with the texts inserted"""
    return ANALYSIS_PROMPT.format(
        dalloway_text=dalloway_text,
        odyssey_text=odyssey_text,
        similarity_score=similarity_score
    )
