"""Educational decision helper; accepts pre-reviewed metadata only."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Source:
    id: str
    permission: str = "unknown"
    sensitive: bool = False
    extraction_ok: bool = True
    exact_duplicate: bool = False
    new_revision: bool = False
    syndicated: bool = False
    new_evidence: bool = False
    near_match: bool = False

def classify(s: Source):
    if s.permission == "denied":
        return "REJECT"
    if s.permission != "approved" or s.sensitive:
        return "QUARANTINE"
    if not s.extraction_ok:
        return "REVIEW"
    if s.new_revision:
        return "NEW_VERSION"
    if s.exact_duplicate:
        return "LINK_DUPLICATE"
    if s.syndicated:
        return "RELATED_VARIANT"
    if s.new_evidence:
        return "INGEST_NEW"
    if s.near_match:
        return "REVIEW"
    return "INGEST_NEW"

if __name__ == "__main__":
    for item in [Source("a", "approved"), Source("b", "approved", exact_duplicate=True), Source("c", "approved", new_revision=True)]:
        print(item.id, classify(item))
