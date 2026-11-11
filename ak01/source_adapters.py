from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass
class SourceQuery:
    query_id: str
    query_text: str
    source_type: str
    limit: int = 10


@dataclass
class SourceCandidate:
    title: str
    source_type: str
    authors_or_issuer: list[str]
    publication_or_version_date: str | None
    persistent_identifier_or_official_locator: str
    discovery_channel: str
    reason_found: str
    raw_metadata: dict[str, Any]


class SourceAdapter(Protocol):
    name: str

    def search(self, query: SourceQuery) -> list[SourceCandidate]:
        ...


class FixtureSourceAdapter:
    """Deterministic adapter for contract and regression tests."""

    name = "fixture"

    def __init__(self, fixtures: list[dict[str, Any]]) -> None:
        self._fixtures = deepcopy(fixtures)

    def search(self, query: SourceQuery) -> list[SourceCandidate]:
        results: list[SourceCandidate] = []

        for item in self._fixtures:
            haystack = " ".join([
                str(item.get("title", "")),
                str(item.get("abstract", "")),
                " ".join(item.get("keywords", [])),
            ]).lower()

            if query.query_text.lower() not in haystack:
                continue

            results.append(
                SourceCandidate(
                    title=str(item["title"]),
                    source_type=str(item.get("source_type", query.source_type)),
                    authors_or_issuer=list(item.get("authors_or_issuer", [])),
                    publication_or_version_date=(
                        str(item["publication_or_version_date"])
                        if item.get("publication_or_version_date") is not None
                        else None
                    ),
                    persistent_identifier_or_official_locator=str(
                        item["persistent_identifier_or_official_locator"]
                    ),
                    discovery_channel=self.name,
                    reason_found=f"fixture_match:{query.query_text}",
                    raw_metadata=deepcopy(item),
                )
            )

            if len(results) >= query.limit:
                break

        return results


def candidate_to_dict(candidate: SourceCandidate) -> dict[str, Any]:
    return {
        "title": candidate.title,
        "source_type": candidate.source_type,
        "authors_or_issuer": list(candidate.authors_or_issuer),
        "publication_or_version_date": candidate.publication_or_version_date,
        "persistent_identifier_or_official_locator": (
            candidate.persistent_identifier_or_official_locator
        ),
        "discovery_channel": candidate.discovery_channel,
        "reason_found": candidate.reason_found,
        "raw_metadata": deepcopy(candidate.raw_metadata),
    }


def run_discovery_queries(
    *,
    adapter: SourceAdapter,
    queries: list[SourceQuery],
) -> dict[str, Any]:
    runs: list[dict[str, Any]] = []
    all_candidates: list[dict[str, Any]] = []

    for query in queries:
        results = adapter.search(query)
        serialized = [candidate_to_dict(item) for item in results]
        runs.append({
            "query_id": query.query_id,
            "query_text": query.query_text,
            "source_type": query.source_type,
            "adapter": adapter.name,
            "result_count": len(serialized),
            "candidates": serialized,
        })
        all_candidates.extend(serialized)

    return {
        "adapter": adapter.name,
        "query_runs": runs,
        "candidates": all_candidates,
        "status": "CANDIDATES_READY" if all_candidates else "NO_CANDIDATES",
    }
