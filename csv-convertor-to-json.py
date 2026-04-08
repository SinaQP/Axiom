"""Convert question CSV rows into a JSON array."""

from argparse import ArgumentParser
from pathlib import Path
import json

import pandas as pd


def csv_to_json(input_path: str, output_path: str | None = None) -> Path:
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"File not found: {input_path}")

    df = pd.read_csv(input_file)
    if "question" not in df.columns:
        raise ValueError("CSV must contain a 'question' column")

    questions = df["question"].dropna().tolist()
    output_file = Path(output_path) if output_path else input_file.with_suffix(".json")

    output_file.write_text(json.dumps(questions, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_file


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Input CSV path")
    parser.add_argument("--output", help="Output JSON path")
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    saved_path = csv_to_json(args.input, args.output)
    print(f"✅ JSON file saved at: {saved_path}")
