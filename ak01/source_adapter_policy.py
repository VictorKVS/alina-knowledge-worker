from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    retryable_statuses: tuple[int, ...] = (408, 429, 500, 502, 503, 504)
    base_backoff_seconds: float = 0.5


def classify_adapter_failure(
    *,
    status_code: int | None = None,
    exception_name: str | None = None,
) -> dict[str, Any]:
    if status_code == 429:
        return {
            "failure_class": "RATE_LIMIT",
            "retryable": True,
            "action": "BACKOFF_AND_RETRY",
        }

    if status_code in {500, 502, 503, 504}:
        return {
            "failure_class": "UPSTREAM_UNAVAILABLE",
            "retryable": True,
            "action": "BACKOFF_AND_RETRY",
        }

    if status_code in {401, 403}:
        return {
            "failure_class": "AUTHORIZATION",
            "retryable": False,
            "action": "ESCALATE_CONFIGURATION",
        }

    if status_code == 404:
        return {
            "failure_class": "NOT_FOUND",
            "retryable": False,
            "action": "RECORD_AND_CONTINUE",
        }

    if exception_name in {"TimeoutError", "ConnectTimeout", "ReadTimeout"}:
        return {
            "failure_class": "TIMEOUT",
            "retryable": True,
            "action": "BACKOFF_AND_RETRY",
        }

    if exception_name:
        return {
            "failure_class": "ADAPTER_EXCEPTION",
            "retryable": False,
            "action": "QUARANTINE_RUN",
        }

    return {
        "failure_class": "UNKNOWN",
        "retryable": False,
        "action": "INVESTIGATE",
    }
