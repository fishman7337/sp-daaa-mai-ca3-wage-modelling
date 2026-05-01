"""Regression utilities for the MS0240 CA3 wages analysis."""

from .regression import (
    MultipleRegressionResult,
    SimpleRegressionResult,
    load_model3_data,
    load_wages_data,
    mean_squared_error,
    model1_without_intercept,
    model2_with_intercept,
    model3_multiple_regression,
)

__all__ = [
    "MultipleRegressionResult",
    "SimpleRegressionResult",
    "load_model3_data",
    "load_wages_data",
    "mean_squared_error",
    "model1_without_intercept",
    "model2_with_intercept",
    "model3_multiple_regression",
]
