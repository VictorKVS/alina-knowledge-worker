"""CH05 Tool Use: portable LangChain BaseChatModel + read-only safe tools.

This example makes no real web, trading, booking, code-execution or device calls.
It uses the same ModelAdapter as CH02-CH04.
Run: python examples/ch05_tool_use.py
"""
import json
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from model_adapter import ModelConfig, create_chat_model

MAX_STEPS = 3
MAX_TOOL_CALLS = 4

@tool
def lookup_demo_fact(key: str) -> str:
    """Look up a fixed educational demo fact. Keys: capital_of_france, tallest_mountain.
    This is a STATIC demo dataset, NOT current weather, internet search or live data.
    """
    facts = {
        "capital_of_france": "Paris (static educational example)",
        "tallest_mountain": "Mount Everest (highest above sea level; static example)",
    }
    return facts.get(key.strip().lower(), "NOT_FOUND: no fact in static demo dataset")

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers accurately, e.g. a=125 and b=48."""
    if isinstance(a, bool) or isinstance(b, bool):
        raise ValueError("Boolean values are not accepted")
    if abs(a) > 1_000_000 or abs(b) > 1_000_000:
        raise ValueError("Input exceeds demo bounds")
    return a * b

TOOLS = {item.name: item for item in [lookup_demo_fact, multiply]}

def run_tool_loop(model, request: str, max_steps: int = MAX_STEPS) -> dict:
    """Execute strictly allowlisted tool calls and return a structured outcome.

    tool_call proposal -> local validation/execution -> ToolMessage -> model.
    Each loop iteration makes one LLM call; a final response may require one more
    model call after the last permitted tool round.
    """
    if not request or not request.strip():
        raise ValueError("Request must not be empty")
    if not 1 <= max_steps <= 10:
        raise ValueError("max_steps must be 1..10")
    bound = model.bind_tools(list(TOOLS.values()))
    history = [
        SystemMessage(content=(
            "You are a read-only educational tool-using assistant. "
            "Use lookup_demo_fact only for the two static examples and multiply for "
            "arithmetic. Do not pretend to browse or get current information. "
            "Do not claim actions were performed in real external systems."
        )),
        HumanMessage(content=request.strip()),
    ]
    trace = []
    tool_count = 0
    for step in range(1, max_steps + 2):
        response = bound.invoke(history)
        calls = getattr(response, "tool_calls", []) or []
        invalid_calls = getattr(response, "invalid_tool_calls", []) or []
        if invalid_calls:
            return {"status": "INVALID_TOOL_CALL", "answer": "", "trace": trace,
                    "error": "Model produced malformed tool calls"}
        history.append(response)
        if not calls:
            return {"status": "COMPLETED", "answer": str(response.content), "trace": trace}
        if step > max_steps:
            return {"status": "LIMIT_REACHED", "answer": "", "trace": trace,
                    "error": "Model requested additional tool calls beyond step limit"}
        if tool_count + len(calls) > MAX_TOOL_CALLS:
            return {"status": "LIMIT_REACHED", "answer": "", "trace": trace,
                    "error": "Too many tool calls"}
        for call in calls:
            name = call.get("name", "")
            args = call.get("args", {})
            call_id = call.get("id")
            if not call_id:
                return {"status": "INVALID_TOOL_CALL", "answer": "", "trace": trace,
                        "error": "Tool call ID is missing"}
            if name not in TOOLS:
                return {"status": "DENIED", "answer": "", "trace": trace,
                        "error": f"Tool not allowlisted: {name}"}
            if not isinstance(args, dict):
                return {"status": "INVALID_TOOL_CALL", "answer": "", "trace": trace,
                        "error": "Tool arguments must be an object"}
            try:
                # LangChain @tool validates arguments via its schema.
                result = TOOLS[name].invoke(args)
                payload = {"status": "OK", "result": result}
            except (ValueError, TypeError) as exc:
                payload = {"status": "INVALID_ARGUMENTS", "message": str(exc)[:200]}
            except Exception as exc:
                payload = {"status": "TOOL_ERROR", "message": type(exc).__name__}
            history.append(ToolMessage(
                content=json.dumps(payload, ensure_ascii=False),
                tool_call_id=call_id,
            ))
            trace.append({"step": step, "tool": name, "args": args,
                          "outcome": payload["status"], "call_id": call_id})
            tool_count += 1
    return {"status": "LIMIT_REACHED", "answer": "", "trace": trace}

def main():
    config = ModelConfig.from_env()
    model = create_chat_model(config)
    print(f"ToolUse provider={config.provider} model={config.model}")
    for request in (
        "Use the calculator to multiply 125 by 48.",
        "Use the demo fact lookup to find capital_of_france.",
        "What is the current weather in London? If unavailable, say so.",
    ):
        print(f"\nREQUEST: {request}")
        try:
            result = run_tool_loop(model, request)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except Exception as exc:
            print(f"ERROR: {type(exc).__name__}: {exc}")

if __name__ == "__main__":
    main()
