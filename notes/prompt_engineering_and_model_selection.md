# Prompt Engineering and Model Selection for Intertextuality Analysis

## Prompt Template Design

1. Use Jinja2 for flexible and maintainable prompt templates
2. Implement Chain of Thought (CoT) prompting technique

### Example CoT Prompt Template:

```jinja2
You are an AI assistant and expert in intertextual analysis between Virginia Woolf's "Mrs Dalloway" and Homer's "The Odyssey" that uses a Chain of Thought (CoT) approach with reflection to answer queries. Follow these steps:
1. Think through the problem step by step within the <thinking> tags.
2. Self-criticize your thinking to check for any errors or improvements within the <self-doubt> tags.
3. Reflect on your thinking to check for any errors or improvements within the <reflection> tags.
4. Make any necessary adjustments based on your reflection.
5. Provide your final, concise answer within the <output> tags.
Important: The <thinking> and <reflection> sections are for your internal reasoning process only.
Do not include any part of the final answer in these sections.
The actual response to the query must be entirely contained within the <output> tags.
Mrs Dalloway chunk:
{{ dalloway_chunk }}
The Odyssey chunk:
{{ odyssey_chunk }}
Use the following format for your response:
<thinking>
[Your step-by-step reasoning goes here. This is your internal thought process, not the final answer.]
<reflection>
[Your reflection on your reasoning, checking for errors or improvements]
</reflection>
[Any adjustments to your thinking based on your reflection]
</thinking>
<output>
[Your final, concise answer to the query. This is the only part that will be shown to the user.]
</output>
```

Reference: https://github.com/codelion/optillm/tree/main/optillm
## Model Selection and Comparison

1. Primary models for comparison:
   - GPT-4 (OpenAI)
   - LLaMA 2 70B (Meta)

2. Rationale for model selection:
   - Both models are widely used and well-documented
   - Allows for comparison between proprietary (GPT-4) and open-source (LLaMA 2) models
   - Comparable in terms of parameter count and general capabilities

3. Note on OpenAI's O1 model:
   - Acknowledge awareness of the new O1 model and its potential capabilities
   - Justify exclusion:
     * Lack of widespread availability and documentation at the time of the study
     * Potential for rapid changes in model architecture and capabilities
     * Focus on comparing more established models for better reproducibility and comparability of results
   - Mention that while aware of O1's capabilities, using normal generative AI LLMs is better for comparability in this study

4. Comparative analysis:
   - Evaluate performance of GPT-4 and LLaMA 2 on intertextuality detection tasks
   - Assess differences in:
     * Accuracy of detected intertextual references
     * Depth and nuance of literary analysis
     * Handling of contextual information provided in chunk headers
   - Discuss implications of using proprietary vs. open-source models for academic research

5. Future considerations:
   - Mention potential for including newer models (like O1 or its open-source equivalents) in future studies
   - Emphasize importance of maintaining comparability and reproducibility in model selection for academic research

By focusing on established models like GPT-4 and LLaMA 2, the study aims to provide a robust and reproducible comparison of intertextuality detection capabilities, while acknowledging the rapid advancements in the field and potential for future studies with newer models.