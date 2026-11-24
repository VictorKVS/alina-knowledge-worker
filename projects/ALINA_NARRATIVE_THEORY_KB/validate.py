"""Validate source/page/quote provenance and structure in NARRATIVE THEORY KB.

This checks presence and consistency; it does NOT verify quotes against private PDFs.
Requires Python >=3.10, stdlib only.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
SOURCES = {s["id"]: s for s in DATA["sources"]}
CARDS = sorted((ROOT / "cards").glob("NAR-*.json"))


def validate_card(card):
    required = ("id","name","task","source_id","source_quality","pdf_pages",
                "short_quote","author_claim","engineering_algorithm",
                "required_inputs","output_fields","applicability","limitations",
                "checks","status")
    for field in required:
        assert field in card, f"{card.get('id')}: missing {field}"
    assert re.fullmatch(r"NAR-\d{3}", card["id"])
    assert card["source_id"] in SOURCES
    src = SOURCES[card["source_id"]]
    assert card["source_quality"] == src["quality"]
    assert card["pdf_pages"] and all(
        isinstance(page, int) and 1 <= page <= src["pages"] for page in card["pdf_pages"]
    ), f"{card['id']}: invalid PDF page references"
    assert 0 < len(card["short_quote"].split()) <= 20, f"{card['id']}: overlong quote"
    assert len(card["engineering_algorithm"]) >= 3
    assert card["limitations"] and card["checks"] and card["required_inputs"]
    assert card["status"].endswith("NOT_QUALIFIED")


def main():
    assert len(SOURCES) == len(DATA["sources"]) and len(SOURCES) >= 6
    assert len(CARDS) >= 5, "Expected first batch of methods"
    seen = set()
    for path in CARDS:
        card = json.loads(path.read_text(encoding="utf-8"))
        validate_card(card)
        assert card["id"] not in seen
        seen.add(card["id"])
        print(f"SCHEMA_OK {card['id']} {card['name']}")
    print(f"STRUCTURE_PASS: {len(CARDS)} cards; SOURCE_CONTENT_NOT_VERIFIED / NOT_QUALIFIED")


if __name__ == "__main__":
    main()
