from __future__ import annotations

from copy import deepcopy
from typing import Any


INJECTION_MARKERS = (
    "ignore previous instructions",
    "ignore all previous instructions",
    "system prompt",
    "developer message",
    "override policy",
    "do not follow",
    "follow these instructions",
    "you are chatgpt",
)


def inspect_source_fragment(fragment: dict[str, Any]) -> dict[str, Any]:
    """Treat all source text as untrusted data, never as control instructions."""
    text = str(fragment.get("text") or "")
    lowered = text.lower()

    markers = [
        marker
        for marker in INJECTION_MARKERS
        if marker in lowered
    ]

    return {
        "fragment_id": fragment.get("fragment_id"),
        "locator": fragment.get("locator"),
        "text": text,
        "content_role": "UNTRUSTED_DATA",
        "instruction_execution_allowed": False,
        "detected_injection_markers": markers,
        "requires_security_review": bool(markers),
        "original_fragment": deepcopy(fragment),
    }


def validate_source_content_policy(result: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if result.get("content_role") != "UNTRUSTED_DATA":
        errors.append("source_content_not_marked_untrusted")

    if result.get("instruction_execution_allowed") is not False:
        errors.append("source_instruction_execution_not_blocked")

    if (
        result.get("detected_injection_markers")
        and result.get("requires_security_review") is not True
    ):
        errors.append("injection_marker_without_security_review")

    return errors
