# Woolf Intertextuality Analysis

A pipeline for detecting and analyzing intertextual references between Virginia Woolf's "Mrs Dalloway" and Homer's "The Odyssey" using semantic search and large language models.

## Project Overview

This project implements a Retrieval Augmented Generation (RAG) pipeline to identify and analyze potential intertextual references between Virginia Woolf's "Mrs Dalloway" and Homer's "The Odyssey". It combines:

- Semantic search using embeddings to find similar passages
- Large Language Model analysis to evaluate intertextual relationships
- Structured output for a systematic analysis

## Experimental Design

The experiment follows these steps:

1. **Text Preprocessing**:
   - Chunks both texts into semantically meaningful segments
   - Preserves contextual information in chunk metadata (e.g. page number, chapter number - TBD might not be useful and removed later on)
   - Generate (OpenAI) embeddings for similarity search

2. **Similarity Detection**:
   - Uses semantic search to find potential intertextual connections
   - For each Dalloway passage:
     * Finds top-k most similar Odyssey passages
     * Finds top-k most dissimilar Odyssey passages for contrast
   - Scores passages based on embedding similarity
   - Filters results based on configurable thresholds

3. **Analysis**:
   - Analyzes both similar and dissimilar passage pairs
   - Considers similarity type in the analysis
   - Generates structured analysis with:
     * Initial observations
     * Analytical steps with evidence
     * Counter-arguments
     * Synthesis
     * Textual intersections

4. **Output Generation**:
   - Produces parallel analyses from both prompts for comparison
   - Enables evaluation of how expert knowledge affects:
     - Reference detection accuracy
     - Analysis depth and sophistication

     - Recognition of Woolf's subtle integration techniques
   - Facilitates systematic comparison through structured output

### Pipeline Architecture

```mermaid
graph LR
    %% Data Ingestion & Indexing
    subgraph Indexing
        C[The Odyssey Text] --> D[Preprocessing]
        D --> E[Vector Embedding]
        E --> F[Vector Store]
    end

    %% Query Processing
    subgraph Retrieval
        A[Mrs Dalloway Text] --> B[Preprocessing]
        B --> G[Query Chunk]
        G --> H[Query Embedding]
        H --> I[Semantic Search]
        F --> I
        I --> J[Retrieved Chunks]
    end

    %% Generation
    subgraph Generation
        J --> K[Context Assembly]
        G --> K
        K --> M[Naive System Prompt]
        K --> N[Expert System Prompt]
        M --> O[LLM Analysis]
        N --> O
        O --> P[Intertextual Analysis]
    end

    style Indexing fill:#f0f7ff,stroke:#333
    style Retrieval fill:#fff0f0,stroke:#333
    style Generation fill:#f0fff0,stroke:#333
```

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/woolf-intertextuality.git
    cd woolf-intertextuality
    ```

2. Install dependencies:

    ```bash
    # using pip
    pip install -r requirements.txt
    ```

    ```bash
    # using uv
    uv sync
    ```

3. Set up environment variables

    ```bash
    cp .env.example .env
    # Edit .env with your OpenAI API key
    ```

## Usage

The analysis can be run directly using `main.py`:

```bash
# Run analysis on all chunks
python -m src.main

# Limit analysis to first N chunks (for testing and money saving reasons)
python -m src.main --limit 5
```

The script will:

1. Load and preprocess both texts
2. Index The Odyssey chunks for similarity search
3. Process each Mrs Dalloway chunk to find similar passages
4. Perform intertextual analysis
5. Save results to a timestamped CSV file in `data/results/`

### Output

Results are saved as CSV files with the following information for each analyzed pair:

- Passage texts and metadata
- Similarity scores
- Intertextual reference analysis including:
  - Subtle integration patterns
  - Multiple operational levels (linguistic, structural, etc.)
  - Feminist transformations
  - Homeric elements
- Confidence levels
- Supporting textual evidence
- Detailed reasoning and counter-arguments

Example output path: `data/results/intertextual_analysis_20240315T143022.csv`

Example output:

**To be added**

## Configuration

Key settings can be configured in `src/config/settings.py` or via environment variables (see `.env.example`):

- LLM parameters (model, temperature, max tokens)
- Embedding settings
- Preprocessing parameters (chunk size, overlap)
- File paths and storage locations

### Evaluation Output

The system generates two types of output files:

1. **Analysis Results** (`data/results/`):
   - Raw analysis output from both Naive and Expert prompts
   - Includes similarity scores, textual comparisons, and detailed analyses
   - Format: `intertextual_analysis_{prompt_type}_{model}_{timestamp}.csv`

2. **Annotation Files** (`data/evaluation/`):
   - Anonymized outputs for blind classification
   - Answer key mapping analysis IDs to prompt types
   - Format: 
     - `annotation_ready_{analysis_file}.csv`
     - `answer_key_{analysis_file}.csv`

The annotation CSV facilitates:
- Blind classification of outputs as Naive/Expert
- Documentation of thematic and surface-level observations
- Collection of annotator justifications
- Tracking of inter-annotator agreement

