"""Run the regression analysis used in the MS0240 CA3 report."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from ms0240_wages import (  # noqa: E402
    load_model3_data,
    load_wages_data,
    model1_without_intercept,
    model2_with_intercept,
    model3_multiple_regression,
)


def main() -> int:
    wages = load_wages_data(PROJECT_ROOT / "data" / "raw" / "Wages-2021-June.xlsx")
    model3_data = load_model3_data(
        PROJECT_ROOT / "data" / "processed" / "model3_data.xlsx"
    )

    model1 = model1_without_intercept(wages)
    model2 = model2_with_intercept(wages)
    model3 = model3_multiple_regression(model3_data)

    print("MS0240 CA3 Wages Regression Results")
    print("-----------------------------------")
    print(
        "Model 1: "
        f"y_hat = {model1.slope:.6f} * Median Age; "
        f"MSE = {model1.mse:.6f}; iterations = {model1.iterations}"
    )
    print(
        "Model 2: "
        f"y_hat = {model2.intercept:.6f} + {model2.slope:.6f} * Median Age; "
        f"MSE = {model2.mse:.6f}; iterations = {model2.iterations}"
    )
    print(
        "Model 3: "
        f"y_hat = {model3.intercept:.6f} "
        f"+ {model3.age_coefficient:.6f} * Median Age "
        f"+ {model3.overtime_coefficient:.6f} * Avg. Overtime Hours; "
        f"MSE = {model3.mse:.6f}; iterations = {model3.iterations}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
