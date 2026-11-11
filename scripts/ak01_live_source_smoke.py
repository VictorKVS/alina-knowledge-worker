from __future__ import annotations

import json
import sys

from ak01.live_source_adapters import CrossrefAdapter, OpenAlexAdapter
from ak01.source_adapters import SourceQuery


def _check(name: str, adapter, query_text: str) -> dict[str, object]:
    results = adapter.search(
        SourceQuery(
            query_id=f"smoke:{name}",
            query_text=query_text,
            source_type="primary_research",
            limit=2,
        )
    )
    if not results:
        raise RuntimeError(f"{name}: no candidates returned")

    first = results[0]
    if not first.persistent_identifier_or_official_locator:
        raise RuntimeError(f"{name}: candidate has no persistent locator")

    return {
        "adapter": name,
        "count": len(results),
        "first_title": first.title,
        "first_locator": first.persistent_identifier_or_official_locator,
    }


def main() -> int:
    checks = [
        _check("openalex", OpenAlexAdapter(), "retrieval augmented generation"),
        _check("crossref", CrossrefAdapter(), "retrieval augmented generation"),
    ]
    print(json.dumps({"status": "PASS", "checks": checks}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(
            json.dumps(
                {
                    "status": "FAIL",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        raise
