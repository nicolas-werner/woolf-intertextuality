import pandas as pd
import numpy as np

def create_evaluation_file():
    expert_df = pd.read_csv('./intertextual_analysis_expert_prompt_gpt-4o_20250112T170351.csv')
    naive_df = pd.read_csv('./intertextual_analysis_naive_prompt_gpt-4o_20250112T170242.csv')
    
    expert_df['analysis_id'] = ['E' + str(i+1) for i in range(len(expert_df))]
    expert_df['prompt_type'] = 'expert'
    
    naive_df['analysis_id'] = ['N' + str(i+1) for i in range(len(naive_df))]
    naive_df['prompt_type'] = 'naive'
    
    combined_df = pd.concat([expert_df, naive_df], ignore_index=True)
    
    columns = [
        'analysis_id',
        'prompt_type',
        'dalloway_text',
        'odyssey_text',
        'similarity_score',
        'initial_observations',
        'thinking_steps',
        'connections',
        'evaluation',
        'evidence_quality_score',
        'theoretical_alignment_score',
        'internal_consistency_score',
        'notes'
    ]
    
    combined_df['evidence_quality_score'] = ''
    combined_df['theoretical_alignment_score'] = ''
    combined_df['internal_consistency_score'] = ''
    combined_df['notes'] = ''
    
    evaluation_df = combined_df[columns]
    
    evaluation_df = evaluation_df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    evaluation_df.to_csv('evaluation_template.csv', index=False)
    
    print(f"Created evaluation template with {len(evaluation_df)} analyses")
    print("\nColumns in output file:")
    for col in columns:
        print(f"- {col}")

if __name__ == "__main__":
    create_evaluation_file()