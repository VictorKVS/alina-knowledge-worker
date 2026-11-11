"""FATHER Future Lab — reproducible forecasting baselines.

Scientific basis:
- Hyndman & Athanasopoulos, Forecasting: Principles and Practice (3rd ed.)
  https://otexts.com/fpp3/
- Method choice, evaluation and refinement:
  https://otexts.com/fpp3/intro.html

These functions are deliberately dependency-free reference implementations.
They are not automatic model selectors and do not claim suitability for every task.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Iterable, Sequence


@dataclass(frozen=True)
class ForecastResult:
    method_id: str
    forecast: list[float]
    assumptions: list[str]
    source_ids: list[str]


def _series(values: Iterable[float]) -> list[float]:
    xs = [float(v) for v in values]
    if not xs:
        raise ValueError("series must contain at least one observation")
    return xs


def naive(values: Iterable[float], horizon: int = 1) -> ForecastResult:
    """Forecast every future observation as the last observed value."""
    xs = _series(values)
    if horizon < 1:
        raise ValueError("horizon must be >= 1")
    return ForecastResult(
        method_id="TS-NAIVE-01",
        forecast=[xs[-1]] * horizon,
        assumptions=["the latest observed level is a useful baseline"],
        source_ids=["SRC-HYNDMAN-FPP3"],
    )


def historical_mean(values: Iterable[float], horizon: int = 1) -> ForecastResult:
    """Forecast future observations using the historical arithmetic mean."""
    xs = _series(values)
    if horizon < 1:
        raise ValueError("horizon must be >= 1")
    level = sum(xs) / len(xs)
    return ForecastResult(
        method_id="TS-MEAN-01",
        forecast=[level] * horizon,
        assumptions=["the process has a stable long-run level"],
        source_ids=["SRC-HYNDMAN-FPP3"],
    )


def drift(values: Sequence[float], horizon: int = 1) -> ForecastResult:
    """Random-walk-with-drift style linear extrapolation from first to last point."""
    xs = _series(values)
    if len(xs) < 2:
        raise ValueError("drift requires at least two observations")
    if horizon < 1:
        raise ValueError("horizon must be >= 1")
    slope = (xs[-1] - xs[0]) / (len(xs) - 1)
    fc = [xs[-1] + slope * h for h in range(1, horizon + 1)]
    return ForecastResult(
        method_id="TS-DRIFT-01",
        forecast=fc,
        assumptions=["average historical drift is informative for the forecast horizon"],
        source_ids=["SRC-HYNDMAN-FPP3"],
    )


def simple_exponential_smoothing(
    values: Iterable[float], alpha: float, horizon: int = 1
) -> ForecastResult:
    """Simple exponential smoothing with explicit alpha supplied by caller."""
    xs = _series(values)
    if not 0 < alpha <= 1:
        raise ValueError("alpha must be in (0, 1]")
    if horizon < 1:
        raise ValueError("horizon must be >= 1")
    level = xs[0]
    for value in xs[1:]:
        level = alpha * value + (1.0 - alpha) * level
    return ForecastResult(
        method_id="TS-SES-01",
        forecast=[level] * horizon,
        assumptions=["no material trend or seasonality", "alpha is externally selected or fitted"],
        source_ids=["SRC-HYNDMAN-FPP3"],
    )


def mae(actual: Sequence[float], predicted: Sequence[float]) -> float:
    if len(actual) != len(predicted) or not actual:
        raise ValueError("actual and predicted must have same non-zero length")
    return sum(abs(float(a) - float(p)) for a, p in zip(actual, predicted)) / len(actual)


def rmse(actual: Sequence[float], predicted: Sequence[float]) -> float:
    if len(actual) != len(predicted) or not actual:
        raise ValueError("actual and predicted must have same non-zero length")
    return sqrt(
        sum((float(a) - float(p)) ** 2 for a, p in zip(actual, predicted)) / len(actual)
    )
