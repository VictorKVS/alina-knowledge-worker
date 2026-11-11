from __future__ import annotations

from collections.abc import Callable
from typing import Any
from urllib.parse import urlencode

from .source_adapters import SourceCandidate, SourceQuery

JsonGetter = Callable[[str, dict[str, str]], dict[str, Any]]


def _default_json_get(url: str, headers: dict[str, str]) -> dict[str, Any]:
    import requests

    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    payload: dict[str, Any] = response.json()
    return payload


class OpenAlexAdapter:
    name = "openalex"

    def __init__(
        self,
        *,
        json_get: JsonGetter | None = None,
        mailto: str | None = None,
    ) -> None:
        self._json_get = json_get or _default_json_get
        self._mailto = mailto

    def search(self, query: SourceQuery) -> list[SourceCandidate]:
        params = {
            "search": query.query_text,
            "per-page": str(query.limit),
        }
        if self._mailto:
            params["mailto"] = self._mailto

        url = "https://api.openalex.org/works?" + urlencode(params)
        payload = self._json_get(url, {"Accept": "application/json"})
        results = payload.get("results", [])

        candidates: list[SourceCandidate] = []
        for item in results[: query.limit]:
            title = str(item.get("display_name") or item.get("title") or "")
            if not title:
                continue

            authors = [
                str(authorship.get("author", {}).get("display_name"))
                for authorship in item.get("authorships", [])
                if authorship.get("author", {}).get("display_name")
            ]

            locator = str(
                item.get("doi")
                or item.get("id")
                or ""
            )
            if not locator:
                continue

            date = item.get("publication_date") or item.get("publication_year")

            candidates.append(
                SourceCandidate(
                    title=title,
                    source_type=query.source_type,
                    authors_or_issuer=authors,
                    publication_or_version_date=(
                        str(date) if date is not None else None
                    ),
                    persistent_identifier_or_official_locator=locator,
                    discovery_channel=self.name,
                    reason_found=f"openalex_search:{query.query_text}",
                    raw_metadata=item,
                )
            )

        return candidates


class CrossrefAdapter:
    name = "crossref"

    def __init__(
        self,
        *,
        json_get: JsonGetter | None = None,
        user_agent: str = "FATHER-AK01/0.1",
    ) -> None:
        self._json_get = json_get or _default_json_get
        self._user_agent = user_agent

    def search(self, query: SourceQuery) -> list[SourceCandidate]:
        params = {
            "query.bibliographic": query.query_text,
            "rows": str(query.limit),
        }
        url = "https://api.crossref.org/works?" + urlencode(params)
        payload = self._json_get(
            url,
            {
                "Accept": "application/json",
                "User-Agent": self._user_agent,
            },
        )

        items = payload.get("message", {}).get("items", [])
        candidates: list[SourceCandidate] = []

        for item in items[: query.limit]:
            titles = item.get("title") or []
            title = str(titles[0]) if titles else ""
            doi = str(item.get("DOI") or "")
            if not title or not doi:
                continue

            authors = [
                " ".join(
                    part
                    for part in [
                        str(author.get("given") or "").strip(),
                        str(author.get("family") or "").strip(),
                    ]
                    if part
                )
                for author in item.get("author", [])
            ]
            authors = [author for author in authors if author]

            published = item.get("published-print") or item.get("published")
            date: str | None = None
            if isinstance(published, dict):
                date_parts = published.get("date-parts") or []
                if date_parts and date_parts[0]:
                    date = "-".join(str(part) for part in date_parts[0])

            candidates.append(
                SourceCandidate(
                    title=title,
                    source_type=query.source_type,
                    authors_or_issuer=authors,
                    publication_or_version_date=date,
                    persistent_identifier_or_official_locator=f"https://doi.org/{doi}",
                    discovery_channel=self.name,
                    reason_found=f"crossref_bibliographic:{query.query_text}",
                    raw_metadata=item,
                )
            )

        return candidates
