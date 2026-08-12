# MS0240 CA3 Wages Regression Analysis

Coursework project for Singapore Polytechnic, School of Computing, Diploma in Applied AI & Analytics.

This repository contains the Mathematics for Artificial Intelligence (MS0240) CA3 report and supporting analysis for the Wages 2021 June dataset. The work was completed by Goh Kun Ming, DAAA student, AY2025/2026 Year 2 Semester 2, under Adj. Lect. Tan Lian Kuan.

## Evidence and interpretation

| Evidence-backed measure | Current repository evidence |
| --- | --- |
| Reproducible optimisation | The corrected gradient-descent configuration converges in **173 iterations**. |
| Reported comparison | Tests cover **3 regression models**; Model 3 uses a **10-row derived table**. |

The qualitative outcome is a transparent wage-regression study connecting analytical derivation, Minitab results, reusable code, and a compiled report. Predictive improvement is not claimed without an explicit held-out baseline metric.

## Project Contents

- `report/` - LaTeX report source, figures, bibliography, and Singapore Polytechnic logo asset.
- `data/` - Source Excel dataset and derived Model 3 dataset used by the analysis.
- `notebooks/` - Original Jupyter notebook used during coursework development.
- `src/ms0240_wages/` - Reusable Python implementation of the gradient descent models.
- `scripts/` - Reproduction helpers for the analysis and report build.
- `tests/` - Pytest checks that verify data assumptions and reported model outputs.
- `docs/` - Assignment brief and supporting project documentation.
- `.github/workflows/` - Continuous integration workflow for tests and report compilation.
- `.dist/` - Generated or legacy build artifacts retained for reference.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
python -m pip install -e .
python scripts/run_analysis.py
python -m pytest
```

To build the report PDF on Windows:

```powershell
.\scripts\build_report.ps1
```

The generated submission PDF is written to `.dist/submission/MS0240-CA3-Wages-Regression-Report.pdf`.

## Report Notes

The report source is `report/main.tex`. It expects the figures under `report/figures/`, the logo under `report/assets/`, and the bibliography file `report/references.bib`.

Model 2 has been corrected so the reported iteration count matches the stated gradient descent settings: learning rates of 0.05 for both parameters, scaled Median Age, epsilon of `1e-5`, and zero initial parameters converge in 173 iterations.

## Licensing

Authored code and documentation in this repository are released under the MIT License. Third-party or institution-provided materials, including the Singapore Polytechnic logo, assignment brief, and source datasets, remain subject to their original ownership and usage terms.
