# Computational Analysis of Intertextual Relationships: A Large Language Model Approach

This repository presents a methodological framework for investigating intertextual relationships through computational means, specifically examining the connections between Virginia Woolf's *Mrs Dalloway* and Homer's *Odyssey* using Large Language Models (LLMs) and semantic search techniques.

## Research Context

This study addresses fundamental methodological challenges in computational literary studies, particularly the operationalization of complex literary concepts for computational analysis. We investigate the capabilities and limitations of Large Language Models in detecting and analyzing sophisticated intertextual relationships, with specific attention to the integration of domain knowledge and theoretical frameworks.

### Theoretical Framework

The methodology draws upon:
- Genette's theory of transtextuality
- Contemporary computational approaches to literary analysis
- Advances in Large Language Model capabilities, particularly in-context learning, chain-of-thought prompting, and structured output generation

### Methodological Design

The implementation comprises three integrated components:

1. **Semantic Similarity Analysis**
   - Vector embedding generation (OpenAI text-embedding-3-small)
   - Cosine similarity computation for passage pair identification
   - Bidirectional retrieval strategy (most/least similar passages)

2. **Domain Knowledge Integration**
   - Expert-informed prompt engineering
   - Integration of literary theoretical frameworks
   - Structured analysis generation with attention to:
     - Explicit and implicit intertextual markers
     - Multiple operational levels (linguistic, structural, thematic)
     - Feminist transformations of classical motifs

3. **Evaluation Framework**
   - Comparative analysis of expert vs. naive prompting approaches
   - Multi-dimensional quality assessment (theoretical alignment, evidence quality, internal consistency)
   - Systematic bias detection and analysis

## Technical Implementation

### Technical Requirements

- Python >= 3.13
- Key Dependencies:
  - OpenAI API client
  - Qdrant for vector storage
  - Haystack AI (v2.7.0+) for RAG pipeline
  - Pandas & NumPy for data processing
  - Rich for CLI interface
  - Pydantic for data validation and structured output generation

For the complete list of dependencies, see `pyproject.toml`.

### Installation Requirements

1. Environment Setup:
```bash
git clone https://github.com/yourusername/woolf-intertextuality.git
cd woolf-intertextuality
```

2. Dependency Installation:
```bash
# Using uv
uv sync
```

3. Configuration:
```bash
cp .env.example .env
# Configure environment variables according to OpenAI documentation
```

### Methodological Execution

The analysis pipeline can be executed using the following commands:

```bash
# 1. Generate analysis files (run twice)
# Run expert analysis
python -m src.main --prompt-template expert_prompt

# Run naive analysis
python -m src.main --prompt-template naive_prompt

# Run expert analysis with a limit
python -m src.main --limit 5 --prompt-template expert_prompt

# 2. Prepare evaluation template
# Combines expert and naive analyses into evaluation template
python -m src.evaluation.create_eval_csv

```

### Output Structure

The analysis generates two categories of data:

1. **Primary Analysis Data** (`data/results/`):
   - Passage-level comparisons with similarity metrics
   - Structured analytical content
   - Format: 
     - Analysis results: `intertextual_analysis_{prompt_type}_{model}_{timestamp}.csv`

2. **Evaluation Materials**:
   - Evaluation template combining expert and naive analyses
   - Format:
     - Template: `evaluation_template.csv` (created by create_eval_csv.py)

### Evaluation Workflow

The evaluation process follows these steps:

1. Run main.py twice to generate both expert and naive analyses
2. Run create_eval_csv.py in `src/evaluation/` to combine analyses into evaluation template
