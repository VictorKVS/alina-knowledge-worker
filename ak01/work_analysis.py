from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


ALLOWED_NODE_TYPES = {
    "PROCESS", "SUBPROCESS", "ACTIVITY", "TASK", "DECISION",
    "ATOMIC_OPERATION", "METHOD", "ALGORITHM", "RULE",
    "KNOWLEDGE_REQUIREMENT", "EVIDENCE_REQUIREMENT", "OUTPUT",
    "QUALITY_CRITERION",
}


@dataclass
class TraceNode:
    id: str
    type: str
    label: str
    derived_from: list[str]
    rationale: str
    confidence: str = "MEDIUM"
    status: str = "DRAFT"


def decompose_work(work_object: dict[str, Any]) -> dict[str, Any]:
    """First conservative AK-01 decomposition MVP.

    It does not invent domain algorithms. It decomposes declared outcomes and
    tasks, records provenance, and reports where a method/decision is missing.
    """
    trace_id = str(work_object.get("id", "WORK")) + ":TRACE"
    source_ref = str(work_object.get("id", "WORK"))

    nodes: list[dict[str, Any]] = [
        asdict(TraceNode(
            id="P1",
            type="PROCESS",
            label=str(work_object.get("goal", "perform work")),
            derived_from=[source_ref],
            rationale="Top-level process is derived from the declared work goal.",
            confidence="HIGH" if work_object.get("goal") else "LOW",
        ))
    ]
    edges: list[dict[str, str]] = []
    findings: list[dict[str, str]] = []

    tasks = work_object.get("tasks") or []
    if not tasks:
        findings.append({
            "type": "MISSING_STEP",
            "node_id": "P1",
            "message": "No explicit tasks are supplied; task discovery is required.",
        })

    for i, task in enumerate(tasks, start=1):
        task_id = f"T{i}"
        if isinstance(task, str):
            task_data = {"label": task}
        else:
            task_data = dict(task)

        nodes.append(asdict(TraceNode(
            id=task_id,
            type="TASK",
            label=str(task_data.get("label", f"task {i}")),
            derived_from=[source_ref],
            rationale="Task is explicitly present in the work object.",
            confidence="HIGH",
        )))
        edges.append({"from": "P1", "to": task_id, "type": "CONTAINS"})

        decisions = task_data.get("decisions") or []
        method = task_data.get("method")
        algorithm = task_data.get("algorithm")

        if not decisions and not method and not algorithm:
            findings.append({
                "type": "MISSING_METHOD",
                "node_id": task_id,
                "message": "Task has no declared decision, method or algorithm.",
            })

        for j, decision in enumerate(decisions, start=1):
            decision_id = f"{task_id}.D{j}"
            nodes.append(asdict(TraceNode(
                id=decision_id,
                type="DECISION",
                label=str(decision),
                derived_from=[task_id],
                rationale="Decision was declared as necessary for the task.",
                confidence="HIGH",
            )))
            edges.append({"from": task_id, "to": decision_id, "type": "DECIDES"})
            findings.append({
                "type": "MISSING_DECISION_RULE",
                "node_id": decision_id,
                "message": "Decision exists but no rule/evidence has yet been attached.",
            })

        if method:
            method_id = f"{task_id}.M1"
            nodes.append(asdict(TraceNode(
                id=method_id,
                type="METHOD",
                label=str(method),
                derived_from=[task_id],
                rationale="Method was explicitly supplied with the task.",
                confidence="HIGH",
            )))
            edges.append({"from": task_id, "to": method_id, "type": "REQUIRES"})

        if algorithm:
            algorithm_id = f"{task_id}.A1"
            nodes.append(asdict(TraceNode(
                id=algorithm_id,
                type="ALGORITHM",
                label=str(algorithm),
                derived_from=[task_id],
                rationale="Algorithm was explicitly supplied with the task.",
                confidence="HIGH",
            )))
            edges.append({"from": task_id, "to": algorithm_id, "type": "REQUIRES"})

    return {
        "trace_id": trace_id,
        "work_object": work_object,
        "nodes": nodes,
        "edges": edges,
        "findings": findings,
    }


def validate_trace(trace: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    node_ids: set[str] = set()

    for node in trace.get("nodes", []):
        node_id = node.get("id")
        if not node_id:
            errors.append("node_missing_id")
            continue
        if node_id in node_ids:
            errors.append(f"duplicate_node:{node_id}")
        node_ids.add(node_id)
        if node.get("type") not in ALLOWED_NODE_TYPES:
            errors.append(f"invalid_node_type:{node_id}")
        if not node.get("derived_from"):
            errors.append(f"missing_derivation:{node_id}")
        if not node.get("rationale"):
            errors.append(f"missing_rationale:{node_id}")

    for edge in trace.get("edges", []):
        if edge.get("from") not in node_ids:
            errors.append(f"edge_missing_source:{edge.get('from')}")
        if edge.get("to") not in node_ids:
            errors.append(f"edge_missing_target:{edge.get('to')}")

    return errors


def find_problems(trace: dict[str, Any]) -> dict[str, Any]:
    validation_errors = validate_trace(trace)
    findings = list(trace.get("findings", []))
    critical_types = {
        "MISSING_INPUT", "CONTRADICTION", "MISSING_EVIDENCE",
        "MISSING_DECISION_RULE",
    }
    critical = [f for f in findings if f.get("type") in critical_types]

    return {
        "valid_trace": not validation_errors,
        "validation_errors": validation_errors,
        "findings": findings,
        "critical_findings": critical,
        "ready_for_promotion": not validation_errors and not critical,
    }
