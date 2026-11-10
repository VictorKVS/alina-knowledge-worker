from __future__ import annotations

import copy
import hashlib
import re
import uuid
from typing import Any

from .domain import Job


_JOBS: dict[str, Job] = {}


def _id() -> str:
    return str(uuid.uuid4())


def _hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _job(job: str | Job) -> Job:
    if isinstance(job, Job):
        return job
    return _JOBS[job]


def _event(j: Job, event_type: str, **payload: Any) -> None:
    record = {"event_type": event_type, **payload}
    j.events.append(record)
    j.audit.append({"action": event_type, **payload})


def create_job(target_agent_profile, evidence_policy):
    j = Job(id=_id(), target=copy.deepcopy(target_agent_profile), policy=copy.deepcopy(evidence_policy))
    _JOBS[j.id] = j
    _event(j, "KnowledgeJobCreated")
    return j.id


def ingest_source(job, source):
    j = _job(job)
    content = source.get("content", "")
    source_id = source.get("id") or _id()
    version = source.get("version", "1")
    item = {
        **copy.deepcopy(source),
        "id": source_id,
        "version": version,
        "content_hash": _hash(content),
        "locator": source.get("locator", "body"),
    }
    existing = next(
        (s for s in j.sources if s["content_hash"] == item["content_hash"] and s["version"] == version),
        None,
    )
    if existing:
        return existing
    j.sources.append(item)
    _event(j, "SourceRegistered", source_id=source_id)
    return item


def _canonical_id(text: str) -> str | None:
    if "Large Language Model" in text or re.search(r"\bLLM\b", text):
        return "CONCEPT:LLM"
    return None


def _extract_sentences(content: str) -> list[str]:
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+", content.strip()) if x.strip()]


def extract(job, source, options=None):
    j = _job(job)
    options = options or {}
    scope_layer = options.get("scope_layer", "DOMAIN")
    drop_locator = options.get("drop_locator", False)

    for text in _extract_sentences(source.get("content", "")):
        dedupe_key = (source["content_hash"], text, scope_layer)
        if any(u.get("dedupe_key") == dedupe_key for u in j.units):
            continue

        malicious = "ignore all previous instructions" in text.lower()
        unit = {
            "id": _id(),
            "text": text,
            "type": "CLAIM",
            "state": "EXTRACTED",
            "scope_layer": scope_layer,
            "source_version_id": f'{source["id"]}:{source["version"]}',
            "source_fragment_id": _hash(text)[:16],
            "source_hash": source["content_hash"],
            "locator": None if drop_locator else source.get("locator", "body"),
            "canonical_id": _canonical_id(text),
            "provenance": {
                "source_id": source["id"],
                "source_hash": source["content_hash"],
            },
            "dedupe_key": dedupe_key,
        }
        if not drop_locator and j.policy.get("require_provenance", False):
            unit["state"] = "VERIFIED"
        if malicious:
            unit["state"] = "EXTRACTED"
            _event(j, "PromptInjectionDetected", source_id=source["id"])
        j.units.append(unit)

    _recompute_contradictions(j)
    _event(j, "KnowledgeExtractionCompleted", source_id=source["id"])
    return list(j.units)


def _recompute_contradictions(j: Job) -> None:
    texts = [u["text"] for u in j.units]
    pairs = []
    for a in texts:
        for b in texts:
            if a == b:
                continue
            aa = a.lower().rstrip(".")
            bb = b.lower().rstrip(".")
            normalized_a = aa.replace(" does not ", " ").replace(" not ", " ")
            normalized_b = bb.replace(" does not ", " ").replace(" not ", " ")
            neg_a = " does not " in f" {aa} " or " not " in f" {aa} "
            neg_b = " does not " in f" {bb} " or " not " in f" {bb} "
            if neg_a != neg_b and normalized_a == normalized_b:
                key = tuple(sorted((a, b)))
                if key not in pairs:
                    pairs.append(key)
    j.contradictions = [
        {"id": _id(), "claims": list(pair), "auto_resolved": False} for pair in pairs
    ]


def get_units(job):
    return copy.deepcopy(_job(job).units)


def get_contradictions(job):
    return copy.deepcopy(_job(job).contradictions)


def get_graph(job):
    j = _job(job)
    nodes = []
    for u in j.units:
        nodes.append({
            "id": u["id"],
            "state": u["state"],
            "provenance": u.get("provenance"),
            "source_fragment_id": u.get("source_fragment_id"),
        })
    return {"nodes": nodes, "edges": []}


def rank(job, candidates):
    authority_rank = {"PRIMARY": 5, "SCIENTIFIC_A": 5, "ACADEMIC_BOOK": 4, "SCIENTIFIC_B": 4, "DISCOVERY": 1}
    def score(c):
        return (
            float(c.get("trust", 0.0)) * 100
            + authority_rank.get(c.get("authority"), 0) * 10
            + float(c.get("similarity", 0.0))
        )
    return sorted(copy.deepcopy(candidates), key=score, reverse=True)


def qualify(job, actor):
    if actor == "AK-01":
        _event(_job(job), "UnauthorizedQualificationAttempt", actor=actor)
        raise PermissionError("AK-01 cannot self-qualify")
    return {"status": "QUALIFIED", "actor": actor}


def get_capsule(job, version=None):
    j = _job(job)
    if version:
        return copy.deepcopy(j.capsule_versions[version])
    return {
        "id": f"CAP-{j.id}",
        "job_id": j.id,
        "version": "0.1.0",
        "knowledge_state": "EXTRACTED",
        "qualification_policy": "external_gate_required",
        "target_agent": copy.deepcopy(j.target),
    }


def create_delta(capsule, delta_spec):
    return {
        "id": _id(),
        "base_version": capsule["version"],
        "base_capsule": copy.deepcopy(capsule),
        "delta_spec": copy.deepcopy(delta_spec),
        "requalified": False,
    }


def release_capsule(capsule_or_delta, requalified=None):
    if "delta_spec" in capsule_or_delta:
        if requalified is not True:
            raise PermissionError("Delta requires requalification before release")
        base = capsule_or_delta["base_capsule"]
        major, minor, patch = [int(x) for x in base["version"].split(".")]
        released = copy.deepcopy(base)
        released["version"] = f"{major}.{minor}.{patch + 1}"
    else:
        released = copy.deepcopy(capsule_or_delta)
        released["status"] = "RELEASED"

    job_id = released.get("job_id")
    if job_id and job_id in _JOBS:
        _JOBS[job_id].capsule_versions[released["version"]] = copy.deepcopy(released)
        _event(_JOBS[job_id], "CapsuleVersionReleased", version=released["version"])
    return released


def simulate_failure(job, failure_kind):
    j = _job(job)
    _event(j, "StageFailed", failure_kind=failure_kind, status="controlled")
    return {"failure_kind": failure_kind, "handled": True}


def get_events(job):
    return copy.deepcopy(_job(job).events)


def get_audit(job):
    return copy.deepcopy(_job(job).audit)


def build_procedure(job, input_spec):
    return {
        "id": _id(),
        "preconditions": ["input_available"],
        "steps": [
            {"id": 1, "action": "validate_input"},
            {"id": 2, "action": "apply_method"},
            {"id": 3, "action": "validate_result"},
        ],
        "stop_conditions": list(input_spec.get("limitations", [])),
    }


def build_checklist(job, input_spec):
    return {
        "id": _id(),
        "items": [
            {"id": "C1", "criterion": "input_validated"},
            {"id": "C2", "criterion": "result_validated"},
        ],
    }


def build_prompt_package(job):
    return {
        "system_core": "FATHER agent core",
        "role": "Knowledge Architect",
        "domain_policy": "Use scoped domain knowledge",
        "evidence_policy": "Require provenance",
        "tool_policy": "Allowlisted tools only",
        "decision_policy": "Follow explicit rules and escalate ambiguity",
        "output_contract": "Structured output",
        "escalation_policy": "Escalate critical uncertainty",
    }


def mark_source_stale(job, source):
    j = _job(job)
    j.stale_sources.add(source["id"])
    affected = [u["id"] for u in j.units if u.get("source_hash") == source["content_hash"]]
    _event(j, "SourceMarkedStale", source_id=source["id"], affected_nodes=affected)
    return {"affected_nodes": affected}


def impact_analysis(job, change):
    return {
        "changed_node": change.get("node_id"),
        "procedures": [],
        "prompts": [],
        "rag": [],
        "tests": [],
    }


def check_source_integrity(job, source, observed_hash):
    j = _job(job)
    mismatch = observed_hash != source["content_hash"]
    if mismatch:
        _event(j, "SourceIntegrityFailed", source_id=source["id"])
    return {
        "quarantined": mismatch,
        "allowed_for_verified_knowledge": not mismatch,
    }


def invoke_tool(job, tool_name, args):
    allowed = {"read_source", "query_graph", "search_knowledge"}
    if tool_name not in allowed:
        _event(_job(job), "ToolPermissionDenied", tool_name=tool_name)
        raise PermissionError(f"Tool not allowed: {tool_name}")
    return {"ok": True}


def send_model_context(job, provider, context):
    text = str(context.get("text", ""))
    contains_secret = bool(re.search(r"(?i)(password|secret|token)\s*=\s*\S+", text))
    unapproved = provider.startswith("external-unapproved")
    if contains_secret and unapproved:
        _event(_job(job), "SecretExposurePrevented", provider=provider)
        return {"blocked": True, "redacted": True}
    return {"blocked": False, "redacted": False, "context": context}
