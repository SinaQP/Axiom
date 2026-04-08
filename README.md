# AI Dataset Generator for Persian Q&A and Prompt-driven Data Creation

A Python toolkit for generating structured datasets with LLMs, focused on Persian-language question datasets and reusable prompt-based generation workflows. The project is built to support repeatable data generation, deduplication, and CSV/JSON post-processing for chatbot training and related NLP tasks.

## Why this project exists
Building high-quality training data manually is slow, inconsistent, and hard to scale. This repository provides a practical generation pipeline that:
- produces structured outputs via explicit JSON prompts,
- reduces repeated content with hash-based duplicate filtering,
- and keeps generation state saved incrementally to avoid lost progress.

---

## Key features

- **Reusable `DatasetGenerator` core class** with configurable prompt template and output key.
- **Diversity controls** (contexts, variety levels, randomized temperature range).
- **Duplicate prevention** using content hashing.
- **Fault-tolerant generation loop** with retries and progress saving.
- **Response parsing safeguards** for malformed JSON responses.
- **Utility scripts** for cleaning and converting generated question datasets.

---

## Tech stack

- Python 3.10+
- OpenAI-compatible API client (`openai`)
- Pandas for tabular processing
- tqdm for generation progress
- python-dotenv for environment configuration
- Optional LangChain wrappers in `avalai_client.py`

---

## How it works (architecture)

1. `DatasetGenerator` builds a prompt from template variables (`context`, `count`, `data_type`, etc.).
2. The prompt is sent to an OpenAI-compatible endpoint (default: Avalai base URL).
3. The response is parsed to extract JSON payloads.
4. Parsed records are flattened and de-duplicated.
5. Progress is appended and saved incrementally to CSV.

Core logic lives in:
- `main.py` → generation pipeline
- `avalai_client.py` → API client wrapper

---

## Installation

```bash
git clone <REPO_LINK>
cd Axiom
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create env file:

```bash
cp .env.example .env
```

Then set at least:

```env
AVALAI_API_KEY=your_api_key
```

Optional:

```env
AVALAI_BASE_URL=https://api.avalai.ir/v1
AVALAI_MODEL_NAME=gpt-4o-mini
```

---

## Usage

### 1) Use the core generator directly

```python
from main import DatasetGenerator

generator = DatasetGenerator(
    dataset_filename="generated_dataset.csv",
    samples_per_request=25,
    data_key="questions"
)

generator.run(total_samples=100, data_type="سوال", variety_parameter="پیچیدگی")
```

### 2) Run domain-specific generators

- `python system-questions.py`
- `python irrelevant_questions_generator.py`
- `python workplace_humanize.py`

Each script provides an interactive choice for full dataset generation vs test dataset generation.

### 3) Clean and convert datasets

```bash
python clean_questions.py chatbot_training_dataset.csv
python remove-dublicate.py chatbot_training_dataset.csv
python csv-convertor-to-json.py chatbot_training_dataset_cleaned.csv
```

---

## Example I/O

**Input:** prompt template + dataset generation settings.

**Output:** CSV file with generated rows, e.g.:

| question |
|---|
| چگونه وارد سیستم شوم؟ |
| چطور گزارش هفتگی بگیرم؟ |

You can then convert to JSON arrays for downstream model training.

---

## Folder structure

```text
Axiom/
├── main.py                          # Core DatasetGenerator class
├── avalai_client.py                 # OpenAI-compatible API client wrapper
├── system-questions.py              # System-related question generation
├── irrelevant_questions_generator.py# Irrelevant question generation
├── workplace_humanize.py            # Workplace-oriented question generation
├── clean_questions.py               # Extract and deduplicate question column
├── remove-dublicate.py              # General question deduplication utility
├── csv-convertor-to-json.py         # CSV to JSON converter utility
├── requirements.txt
├── .env.example
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## Engineering decisions and challenges solved

- **Robustness over ideal responses:** LLM outputs can be malformed; parser logic includes cleanup and fallback extraction.
- **Data quality controls:** Duplicate detection is built into the generation loop, not only post-processing.
- **Operational safety:** Progress is saved after successful requests to avoid losing long-running generation jobs.
- **Flexibility:** Prompt templates and field instructions are configurable without modifying core generation flow.

---

## Future improvements

- Add automated tests for parsing, deduplication, and save/merge behavior.
- Split scripts into a package with a unified CLI (`argparse`/`typer`).
- Add schema validation (e.g., `pydantic`) for output quality guarantees.
- Add structured logging instead of print statements.
- Add deterministic run mode (seed + config export) for reproducible datasets.

---

## Resume-ready positioning

This project demonstrates practical LLM engineering skills: prompt design, defensive parsing, data-quality enforcement, and automation-oriented data pipelines for NLP dataset creation.
