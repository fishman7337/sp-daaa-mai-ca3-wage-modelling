"""Gradient descent implementations used in the MS0240 CA3 report."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

WAGES_COLUMNS = ("Median Age", "Basic Wage ($)")
MODEL3_COLUMNS = (
    "Median Age",
    "Average Overtime Hours per Month",
    "Basic Wage ($)",
)


@dataclass(frozen=True)
class SimpleRegressionResult:
    """Result for a simple linear regression model."""

    intercept: float
    slope: float
    mse: float
    iterations: int


@dataclass(frozen=True)
class MultipleRegressionResult:
    """Result for the multiple regression model."""

    intercept: float
    age_coefficient: float
    overtime_coefficient: float
    mse: float
    iterations: int


def load_wages_data(path: str | Path) -> pd.DataFrame:
    """Load the main Wages 2021 June dataset and validate required columns."""
    return _load_excel_with_columns(path, WAGES_COLUMNS)


def load_model3_data(path: str | Path) -> pd.DataFrame:
    """Load the derived Model 3 dataset and validate required columns."""
    return _load_excel_with_columns(path, MODEL3_COLUMNS)


def mean_squared_error(actual: np.ndarray, predicted: np.ndarray) -> float:
    """Return the average squared prediction error."""
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    if actual.shape != predicted.shape:
        raise ValueError("actual and predicted arrays must have the same shape")
    return float(np.mean((actual - predicted) ** 2))


def model1_without_intercept(
    data: pd.DataFrame,
    *,
    learning_rate: float = 0.0001,
    epsilon: float = 1e-5,
    max_iterations: int = 150,
) -> SimpleRegressionResult:
    """Fit y = bx using the same gradient descent settings as Question 1."""
    x = _column_as_float_array(data, "Median Age")
    y = _column_as_float_array(data, "Basic Wage ($)")

    slope = 0.0
    diff = float("inf")
    iterations = 0

    while diff > epsilon and iterations < max_iterations:
        gradient = -(2 / len(x)) * np.sum(x * (y - slope * x))
        new_slope = slope - learning_rate * gradient
        diff = abs(new_slope - slope)
        slope = float(new_slope)
        iterations += 1

    predicted = slope * x
    return SimpleRegressionResult(
        intercept=0.0,
        slope=slope,
        mse=mean_squared_error(y, predicted),
        iterations=iterations,
    )


def model2_with_intercept(
    data: pd.DataFrame,
    *,
    learning_rate_a: float = 0.05,
    learning_rate_b: float = 0.05,
    epsilon: float = 1e-5,
    max_iterations: int = 1000,
) -> SimpleRegressionResult:
    """Fit y = a + bx using scaled Median Age for stable gradient descent."""
    x = _column_as_float_array(data, "Median Age")
    y = _column_as_float_array(data, "Basic Wage ($)")
    x_scaled, mean_x, std_x = _standardise(x)

    a_scaled = 0.0
    b_scaled = 0.0
    diff = float("inf")
    iterations = 0

    while diff > epsilon and iterations < max_iterations:
        residual = a_scaled + b_scaled * x_scaled - y
        grad_a = (2 / len(x)) * np.sum(residual)
        grad_b = (2 / len(x)) * np.sum(residual * x_scaled)

        new_a_scaled = a_scaled - learning_rate_a * grad_a
        new_b_scaled = b_scaled - learning_rate_b * grad_b
        diff = max(abs(new_a_scaled - a_scaled), abs(new_b_scaled - b_scaled))

        a_scaled = float(new_a_scaled)
        b_scaled = float(new_b_scaled)
        iterations += 1

    slope = b_scaled / std_x
    intercept = a_scaled - (b_scaled * mean_x / std_x)
    predicted = intercept + slope * x
    return SimpleRegressionResult(
        intercept=float(intercept),
        slope=float(slope),
        mse=mean_squared_error(y, predicted),
        iterations=iterations,
    )


def model3_multiple_regression(
    data: pd.DataFrame,
    *,
    learning_rate_a: float = 0.05,
    learning_rate_b: float = 0.05,
    learning_rate_c: float = 0.05,
    epsilon: float = 0.001,
    max_iterations: int = 1000,
) -> MultipleRegressionResult:
    """Fit y = a + bx + cw using scaled age and overtime predictors."""
    age = _column_as_float_array(data, "Median Age")
    overtime = _column_as_float_array(data, "Average Overtime Hours per Month")
    wage = _column_as_float_array(data, "Basic Wage ($)")

    age_scaled, mean_age, std_age = _standardise(age)
    overtime_scaled, mean_overtime, std_overtime = _standardise(overtime)

    a_scaled = 0.0
    b_scaled = 0.0
    c_scaled = 0.0
    diff = float("inf")
    iterations = 0

    while diff > epsilon and iterations < max_iterations:
        residual = a_scaled + b_scaled * age_scaled + c_scaled * overtime_scaled - wage
        grad_a = (2 / len(age)) * np.sum(residual)
        grad_b = (2 / len(age)) * np.sum(residual * age_scaled)
        grad_c = (2 / len(age)) * np.sum(residual * overtime_scaled)

        new_a_scaled = a_scaled - learning_rate_a * grad_a
        new_b_scaled = b_scaled - learning_rate_b * grad_b
        new_c_scaled = c_scaled - learning_rate_c * grad_c
        diff = max(
            abs(new_a_scaled - a_scaled),
            abs(new_b_scaled - b_scaled),
            abs(new_c_scaled - c_scaled),
        )

        a_scaled = float(new_a_scaled)
        b_scaled = float(new_b_scaled)
        c_scaled = float(new_c_scaled)
        iterations += 1

    age_coefficient = b_scaled / std_age
    overtime_coefficient = c_scaled / std_overtime
    intercept = (
        a_scaled - (b_scaled * mean_age / std_age) - (c_scaled * mean_overtime / std_overtime)
    )
    predicted = intercept + age_coefficient * age + overtime_coefficient * overtime
    return MultipleRegressionResult(
        intercept=float(intercept),
        age_coefficient=float(age_coefficient),
        overtime_coefficient=float(overtime_coefficient),
        mse=mean_squared_error(wage, predicted),
        iterations=iterations,
    )


def _load_excel_with_columns(path: str | Path, columns: Iterable[str]) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    data = pd.read_excel(path)
    missing = [column for column in columns if column not in data.columns]
    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"Dataset {path} is missing required columns: {joined}")
    return data


def _column_as_float_array(data: pd.DataFrame, column: str) -> np.ndarray:
    return data[column].to_numpy(dtype=float)


def _standardise(values: np.ndarray) -> tuple[np.ndarray, float, float]:
    mean = float(np.mean(values))
    std = float(np.std(values))
    if std == 0:
        raise ValueError("Cannot standardise a constant predictor")
    return (values - mean) / std, mean, std
