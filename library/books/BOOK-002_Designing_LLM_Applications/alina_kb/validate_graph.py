"""Local structural validator for ALINA BOOK-002 knowledge graph.
No network, no LLM evaluation. Run from this directory: python validate_graph.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
graph = json.loads((ROOT / "knowledge_graph.json").read_text(encoding="utf-8"))
gloss = json.loads((ROOT / "glossary.json").read_text(encoding="utf-8"))
algs = json.loads((ROOT / "algorithms.json").read_text(encoding="utf-8"))
roles = json.loads((ROOT / "roles.json").read_text(encoding="utf-8"))

nodes = graph["nodes"]
ids = [n["id"] for n in nodes]
assert len(ids) == len(set(ids)), "Duplicate node IDs"
node_ids = set(ids)
role_ids = {"ROLE-" + r["role"] for r in roles["views"]}
chapter_spans = graph["source"]["chapter_spans"]

for n in nodes:
    assert isinstance(n["definition_ru"], str) and len(n["definition_ru"]) >= 18
    imp = n["weight"]["importance"]
    assert isinstance(imp, int) and 1 <= imp <= 5
    confidence = n["weight"]["confidence"]
    if n["origin"] == "FATHER_ENGINEERING_EXTENSION":
        assert confidence is None
    else:
        assert isinstance(confidence, (int, float)) and 0 <= confidence <= 1
    assert n["chapter"] in chapter_spans
    p1, p2 = n["evidence"]["pdf_pages"]
    ch1, ch2 = chapter_spans[n["chapter"]]
    assert ch1 <= p1 <= p2 <= ch2
    assert all(link in node_ids for link in n["related_ids"])

for edge in graph["edges"]:
    assert edge["from"] in (node_ids | role_ids)
    assert edge["to"] in node_ids
    assert 0 <= edge["weight"] <= 1

assert {g["id"] for g in gloss["terms"]} == node_ids, "Glossary mismatch"
assert all(set(role["filter"]["ids"]).issubset(node_ids) for role in roles["views"])
for alg in algs["algorithms"]:
    assert all("B002-" + key.upper() in node_ids for key in alg["nodes"])
print("STRUCTURAL PASS", len(nodes), "nodes", len(graph["edges"]), "edges")
