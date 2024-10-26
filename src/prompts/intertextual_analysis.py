from typing import List, Optional, Set
from pydantic import BaseModel, Field
from enum import Enum
from pathlib import Path

class ReferenceType(str, Enum):
    QUOTATION = "quotation"          # Direct textual borrowing
    ALLUSION = "allusion"            # Indirect reference
    STRUCTURAL = "structural"        # Similar narrative patterns
    DIALOGIC = "dialogic"           # Text responding to or in dialogue with other text
    TRANSFORMATION = "transformation" # Rewriting or reimagining of themes/motifs
    NONE = "none"                   # No meaningful intertextual relationship

class TextualCode(str, Enum):
    LITERARY = "literary"           # Literary conventions and traditions
    CULTURAL = "cultural"           # Cultural codes and contexts
    SOCIAL = "social"              # Social norms and structures
    HISTORICAL = "historical"       # Historical context and references
    LINGUISTIC = "linguistic"       # Language patterns and structures

class ConfidenceLevel(str, Enum):
    HIGH = "high"          # Strong evidence and clear connections
    MODERATE = "moderate"  # Some evidence but with caveats
    LOW = "low"           # Possible but speculative connection
    UNCERTAIN = "uncertain" # Not enough evidence to make a determination

class IntertextualReference(BaseModel):
    """Represents a potential intertextual reference based on Kristeva's theory"""
    is_reference: bool = Field(
        description="Whether this similarity represents a meaningful intertextual reference"
    )
    reference_type: ReferenceType = Field(
        description="The type of intertextual relationship present"
    )
    textual_codes: Set[TextualCode] = Field(
        description="The types of codes/systems through which the texts interact",
        min_items=1
    )
    explanation: str = Field(
        description="Detailed explanation of the intertextual relationship"
    )
    confidence: ConfidenceLevel = Field(
        description="Qualitative assessment of confidence in the reference identification"
    )
    supporting_evidence: List[str] = Field(
        description="Specific textual evidence supporting the reference",
        min_items=1
    )
    transformation: str = Field(
        description="How Woolf transforms or recontextualizes the Homeric text"
    )

class AnalysisThoughtProcess(BaseModel):
    """Represents the Chain of Thought reasoning process"""
    initial_observation: str = Field(
        description="Initial observation about textual similarities"
    )
    contextual_analysis: str = Field(
        description="Analysis of historical and cultural contexts of both passages"
    )
    code_identification: List[str] = Field(
        description="Identification of shared textual codes and systems"
    )
    dialogic_analysis: str = Field(
        description="How the texts engage in dialogue with each other"
    )
    transformation_analysis: str = Field(
        description="How Woolf transforms or reinterprets Homeric elements"
    )
    counter_arguments: List[str] = Field(
        description="Possible arguments against this being an intertextual reference"
    )
    synthesis: str = Field(
        description="Final synthesis of the intertextual analysis"
    )

class IntertextualAnalysis(BaseModel):
    """Complete analysis of a potential intertextual reference"""
    thought_process: AnalysisThoughtProcess = Field(
        description="Chain of thought reasoning process"
    )
    reference: IntertextualReference = Field(
        description="The identified intertextual reference"
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
Similarity score: {similarity_score}

Follow these steps in your analysis:

1. Initial Observation:
- Note any immediate similarities in language, theme, or structure

2. Contextual Analysis:
- Consider the context of both passages
- Think about their role in their respective works

3. Literary Devices:
- Identify any shared literary devices or techniques
- Consider how they're used in each text

4. Thematic Connections:
- Analyze potential thematic parallels
- Consider Woolf's known engagement with classical texts

5. Counter Arguments:
- Consider why this might NOT be an intentional reference
- Evaluate the strength of the connection

6. Synthesis:
- Weigh the evidence
- Determine if this represents a meaningful intertextual reference

Provide your analysis in a structured format that includes both your thought process and final determination.

Remember:
- Not all similarities are meaningful intertextual references
- Consider Woolf's documented interest in classical literature
- Consider the similarity score in your analysis
- Be specific in citing textual evidence
"""

def get_analysis_prompt(dalloway_text: str, odyssey_text: str, similarity_score: float) -> str:
    """Generate the analysis prompt with the given texts"""
    return ANALYSIS_PROMPT.format(
        dalloway_text=dalloway_text,
        odyssey_text=odyssey_text,
        similarity_score=similarity_score
    )
