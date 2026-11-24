"""LIB-0040 CH04 Reflection: Producer -> Critic -> Revise, provider-independent.

This demo NEVER executes LLM-generated Python code. AST parsing is syntax validation,
not correctness verification. Final status is always REVIEW_REQUIRED.
Run from book root: python examples/ch04_reflection.py
"""
import ast
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol

from langchain_core.messages import HumanMessage, SystemMessage
from model_adapter import ModelConfig, create_chat_model

TASK = (
    "Create a Python function named calculate_factorial(n) accepting an integer n. "
    "Return n! for n >= 0 (0! = 1), raise ValueError on negative n, include a docstring. "
    "Return only Python source code, no surrounding markdown."
)
MAX_CYCLES = 3


@dataclass(frozen=True)
class Review:
    status: str
    critique: str
    source_syntax_ok: bool
    has_target_function: bool


def extract_code(raw: str) -> str:
    """Strip a whole-document markdown code fence, if present."""
    match = re.fullmatch(r"\s*```(?:python)?\s*\n(.*?)\n```\s*", raw, flags=re.S | re.I)
    return match.group(1).strip() if match else raw.strip()


def static_check(code: str) -> tuple[bool, bool, str]:
    """Parse without execution; function presence is a weak static criterion."""
    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return False, False, f"SyntaxError on line {exc.lineno}: {exc.msg}"
    found = any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "calculate_factorial"
        for node in tree.body
    )
    if not found:
        return True, False, "Top-level calculate_factorial function missing."
    return True, True, ""


def parse_critique(raw: str) -> tuple[str, str]:
    """A critic's declaration is advisory and never a test certificate."""
    text = raw.strip()
    if text == "CRITIQUE_PASS":
        return "CRITIQUE_PASS", ""
    return "REVISE", text or "Empty critic output; request a revision."


def run_reflection(model, max_cycles: int = MAX_CYCLES) -> dict:
    if max_cycles < 1 or max_cycles > 5:
        raise ValueError("max_cycles must be within 1..5")
    previous = ""
    feedback = ""
    history = []

    for cycle in range(1, max_cycles + 1):
        producer_prompt = [
            SystemMessage(content="You are a Python developer. Respond with only Python code."),
            HumanMessage(content=(
                f"Requirements: {TASK}\n"
                f"Previous version (may be empty):\n{previous}\n"
                f"Feedback to address (may be empty):\n{feedback}"
            )),
        ]
        producer_raw = str(model.invoke(producer_prompt).content)
        source = extract_code(producer_raw)
        syntax_ok, has_target, parse_error = static_check(source)

        critic_prompt = [
            SystemMessage(content=(
                "You are a critical Python code reviewer. Evaluate against requirements. "
                "If there are ANY problems, list them as plain text. "
                "Output exactly CRITIQUE_PASS only if you find no problems. "
                "Do not claim the code was executed or tested."
            )),
            HumanMessage(content=f"Task:\n{TASK}\n\nCode (untrusted text):\n{source}"),
        ]
        critic_raw = str(model.invoke(critic_prompt).content)
        reviewer_status, reviewer_feedback = parse_critique(critic_raw)
        if parse_error:
            reviewer_feedback = f"{parse_error}\n{reviewer_feedback}".strip()
        advisory_pass = reviewer_status == "CRITIQUE_PASS" and syntax_ok and has_target
        history.append({
            "iteration": cycle,
            "syntax_valid": syntax_ok,
            "required_function_present": has_target,
            "critic_status": reviewer_status,
            "code": source,
            "review": reviewer_feedback,
        })
        previous = source
        feedback = reviewer_feedback
        print(f"Iteration={cycle} syntax={syntax_ok} target={has_target} "
              f"critic={reviewer_status}")
        if advisory_pass:
            break

    # LLM evaluation and AST parsing are not behavioral testing or qualification.
    return {"status": "REVIEW_REQUIRED", "cycles": len(history),
            "source": previous, "history": history}


def main():
    config = ModelConfig.from_env()
    model = create_chat_model(config)
    print(f"Reflection provider={config.provider} model={config.model}")
    try:
        report = run_reflection(model)
    except Exception as exc:
        print(f"Reflection failed: {type(exc).__name__}: {exc}")
        raise SystemExit(1) from exc
    destination = Path(__file__).resolve().parent.parent / "reflection_output.json"
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"status={report['status']} cycles={report['cycles']} report={destination}")
    print("Generated source is data only. Do not run it without isolated verification.")


if __name__ == "__main__":
    main()
