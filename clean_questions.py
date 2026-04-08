"""Extracts and de-duplicates only the `question` column from a CSV file."""

from argparse import ArgumentParser
from pathlib import Path

import pandas as pd


def clean_questions(input_path: str, output_path: str | None = None) -> Path:
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    df = pd.read_csv(input_file)
    if "question" not in df.columns:
        raise ValueError("CSV must contain a 'question' column")

    df_questions = df[["question"]].dropna().drop_duplicates().reset_index(drop=True)

    output_file = Path(output_path) if output_path else input_file.with_name(f"{input_file.stem}_questions.csv")
    df_questions.to_csv(output_file, index=False)
    return output_file


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Input CSV path")
    parser.add_argument("--output", help="Output CSV path")
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    saved_path = clean_questions(args.input, args.output)
    print(f"✅ Cleaned questions saved at: {saved_path}")
