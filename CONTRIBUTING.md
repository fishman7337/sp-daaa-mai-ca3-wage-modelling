# Contributing

This repository is primarily a coursework submission package. Contributions should preserve reproducibility, academic integrity, and the report results.

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pip install -e .
```

## Checks Before Submission

```powershell
python scripts/run_analysis.py
python -m pytest
.\scripts\build_report.ps1
```

## Change Guidelines

- Keep source data in `data/raw/` unchanged unless the source file itself is intentionally replaced.
- Put derived datasets in `data/processed/` and document how they were produced.
- Keep report figures under `report/figures/` and update captions when figures change.
- Update tests when changing model settings, stopping criteria, or expected output values.
- Do not commit secrets, local virtual environments, or generated LaTeX intermediates.
