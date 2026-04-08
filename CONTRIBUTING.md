# Contributing

Thanks for considering a contribution.

## Development setup

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy environment template and set secrets:
   ```bash
   cp .env.example .env
   ```

## Coding guidelines

- Follow PEP 8 and use descriptive snake_case names.
- Keep prompts and field instructions explicit and testable.
- Prefer small, composable functions over long procedural blocks.
- Avoid writing generated CSV/JSON datasets into source-control by default.

## Running checks

```bash
python -m compileall .
```

If you add tests, include command(s) needed to run them in your PR.

## Pull request checklist

- [ ] Code runs locally
- [ ] README and usage docs are updated when behavior changes
- [ ] No secrets are committed
- [ ] Generated datasets are excluded from commits
