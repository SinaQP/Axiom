import pandas as pd
from pathlib import Path

def csv_to_json(input_path: str, output_path: str = None) -> None:
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_path}")
    
    df = pd.read_csv(input_file)
    
    if "question" not in df.columns:
        raise ValueError("CSV must contain a 'question' column")
    
    questions = df["question"].dropna().tolist()
    
    if output_path is None:
        output_path = input_file.with_suffix(".json")
    
    pd.Series(questions).to_json(output_path, orient="values", force_ascii=False, indent=2)
    print(f"✅ JSON file saved at: {output_path}")
    
csv_to_json("workplace_humanize_dataset_cleaned.csv")
csv_to_json("irrelevant_questions_dataset_questions.csv")
csv_to_json("chatbot_training_dataset_cleaned.csv")
