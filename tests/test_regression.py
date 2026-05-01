from pathlib import Path

import pytest

from ms0240_wages import (
    load_model3_data,
    load_wages_data,
    model1_without_intercept,
    model2_with_intercept,
    model3_multiple_regression,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_wages_dataset_shape_and_columns() -> None:
    data = load_wages_data(PROJECT_ROOT / "data/raw/Wages-2021-June.xlsx")

    assert data.shape[0] == 232
    assert {"Median Age", "Basic Wage ($)"}.issubset(data.columns)


def test_model3_dataset_shape_and_columns() -> None:
    data = load_model3_data(PROJECT_ROOT / "data/processed/model3_data.xlsx")

    assert data.shape[0] == 10
    assert {
        "Median Age",
        "Average Overtime Hours per Month",
        "Basic Wage ($)",
    }.issubset(data.columns)


def test_model1_matches_reported_gradient_descent_result() -> None:
    data = load_wages_data(PROJECT_ROOT / "data/raw/Wages-2021-June.xlsx")

    result = model1_without_intercept(data)

    assert result.iterations == 41
    assert result.intercept == 0.0
    assert result.slope == pytest.approx(174.7967072224972)
    assert result.mse == pytest.approx(13925464.984924644)


def test_model2_matches_reported_gradient_descent_result() -> None:
    data = load_wages_data(PROJECT_ROOT / "data/raw/Wages-2021-June.xlsx")

    result = model2_with_intercept(data)

    assert result.iterations == 173
    assert result.intercept == pytest.approx(767.5626075270866)
    assert result.slope == pytest.approx(156.2552942946782)
    assert result.mse == pytest.approx(13891962.698419666)


def test_model3_matches_reported_gradient_descent_result() -> None:
    data = load_model3_data(PROJECT_ROOT / "data/processed/model3_data.xlsx")

    result = model3_multiple_regression(data)

    assert result.iterations == 401
    assert result.intercept == pytest.approx(-4273.116752825248)
    assert result.age_coefficient == pytest.approx(27.26077176350903)
    assert result.overtime_coefficient == pytest.approx(673.5503104554346)
    assert result.mse == pytest.approx(438087.0501700889)
