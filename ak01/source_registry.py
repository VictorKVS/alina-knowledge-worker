from __future__ import annotations

from copy import deepcopy
from typing import Any


def _normalize_locator(locator: str) -> str:
    value = locator.strip().lower()
    for prefix in (
        "https://doi.org/",
        "http://doi.org/",
        "doi:",
    ):
        if value.startswith(prefix):
            return f"doi:{value.removeprefix(prefix)}"
    return value


def _candidate_key(candidate: dict[str, Any]) -> str:
    locator = str(
        candidate.get("persistent_identifier_or_official_locator") or ""
    ).strip()
    if locator:
        return _normalize_locator(locator)

    title = " ".join(
        str(candidate.get("title") or "").lower().split()
    )
    date = str(candidate.get("publication_or_version_date") or "")
    return f"title:{title}|date:{date}"


def register_candidates(
    candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    """Deduplicate discovered candidates while preserving provenance."""
    entries: dict[str, dict[str, Any]] = {}

    for candidate in candidates:
        key = _candidate_key(candidate)
        channel = str(candidate.get("discovery_channel") or "unknown")

        if key not in entries:
            entries[key] = {
                "registry_key": key,
                "title": candidate.get("title"),
                "source_type": candidate.get("source_type"),
                "authors_or_issuer": list(
                    candidate.get("authors_or_issuer") or []
                ),
                "publication_or_version_date": candidate.get(
                    "publication_or_version_date"
                ),
                "persistent_identifier_or_official_locator": candidate.get(
                    "persistent_identifier_or_official_locator"
                ),
                "discovery_channels": [channel],
                "discovery_records": [deepcopy(candidate)],
                "merge_count": 1,
                "status": "DISCOVERED_UNQUALIFIED",
            }
            continue

        entry = entries[key]

        if channel not in entry["discovery_channels"]:
            entry["discovery_channels"].append(channel)

        entry["discovery_records"].append(deepcopy(candidate))
        entry["merge_count"] += 1

        known_authors = list(entry.get("authors_or_issuer") or [])
        for author in candidate.get("authors_or_issuer") or []:
            if author not in known_authors:
                known_authors.append(author)
        entry["authors_or_issuer"] = known_authors

    ordered = sorted(entries.values(), key=lambda item: item["registry_key"])

    return {
        "entries": ordered,
        "unique_count": len(ordered),
        "input_count": len(candidates),
        "duplicate_count": len(candidates) - len(ordered),
        "status": "REGISTRY_READY" if ordered else "EMPTY_REGISTRY",
    }


def validate_registry(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    keys: set[str] = set()
    for entry in registry.get("entries", []):
        key = str(entry.get("registry_key") or "")
        if not key:
            errors.append("missing_registry_key")
            continue
        if key in keys:
            errors.append(f"duplicate_registry_key:{key}")
        keys.add(key)

        if not entry.get("discovery_records"):
            errors.append(f"missing_discovery_records:{key}")
        if not entry.get("discovery_channels"):
            errors.append(f"missing_discovery_channels:{key}")
        if entry.get("status") != "DISCOVERED_UNQUALIFIED":
            errors.append(f"invalid_initial_status:{key}")

    if registry.get("unique_count") != len(registry.get("entries", [])):
        errors.append("unique_count_mismatch")

    return errors
