import pandas as pd
from pathlib import Path

def remove_duplicates(input_path: str, output_path: str = None) -> None:
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_path}")
    
    df = pd.read_csv(input_file, header=None, names=["question"])
    df_unique = df.drop_duplicates(subset=["question"])
    
    if output_path is None:
        output_path = input_file.with_name(f"{input_file.stem}_cleaned.csv")
    
    df_unique.to_csv(output_path, index=False, header=False)
    print(f"✅ Cleaned file saved at: {output_path}")
    
remove_duplicates("chatbot_training_dataset.csv")