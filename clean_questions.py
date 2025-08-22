import pandas as pd
from pathlib import Path

def clean_questions(input_path: str, output_path: str = None) -> None:
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_path}")
    
    df = pd.read_csv(input_file)
    
    if "question" not in df.columns:
        raise ValueError("CSV must contain a 'question' column")
    
    df_questions = df[["question"]].drop_duplicates()
    
    if output_path is None:
        output_path = input_file.with_name(f"{input_file.stem}_questions.csv")
    
    df_questions.to_csv(output_path, index=False)
    print(f"✅ Cleaned questions saved at: {output_path}")
    
clean_questions("irrelevant_questions_dataset.csv")