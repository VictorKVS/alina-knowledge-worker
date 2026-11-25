"""Offline tests for CH05 tool-loop; no Ollama/network required."""
import sys
import unittest
from pathlib import Path
from langchain_core.messages import AIMessage
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from ch05_tool_use import run_tool_loop, MAX_TOOL_CALLS

class FakeModel:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.received = []
        self.bound = False
    def bind_tools(self, tools):
        self.bound = True
        self.tool_names = {t.name for t in tools}
        return self
    def invoke(self, messages):
        self.received.append(messages[:])
        return next(self.responses)

def tool_request(name, args, identifier="call-1"):
    return AIMessage(content="", tool_calls=[{"name": name, "args": args, "id": identifier}])

class ToolUseTests(unittest.TestCase):
    def test_multiply_then_final(self):
        model = FakeModel([tool_request("multiply", {"a": 125, "b": 48}), AIMessage(content="6000")])
        result = run_tool_loop(model, "Calculate 125 * 48")
        self.assertTrue(model.bound)
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["answer"], "6000")
        self.assertEqual(result["trace"][0]["outcome"], "OK")
        self.assertIn("6000", model.received[1][-1].content)

    def test_static_fact(self):
        model = FakeModel([tool_request("lookup_demo_fact", {"key": "capital_of_france"}), AIMessage(content="Paris")])
        self.assertEqual(run_tool_loop(model, "capital")["status"], "COMPLETED")

    def test_unknown_tool_denied(self):
        model = FakeModel([tool_request("delete_files", {"path": "/"})])
        self.assertEqual(run_tool_loop(model, "delete everything")["status"], "DENIED")

    def test_no_tool_needed(self):
        model = FakeModel([AIMessage(content="No live data available")])
        result = run_tool_loop(model, "weather")
        self.assertEqual(result["trace"], [])

    def test_invalid_arguments(self):
        model = FakeModel([tool_request("multiply", {"a": "not-an-int", "b": 2}), AIMessage(content="Invalid arguments")])
        result = run_tool_loop(model, "bad multiply")
        self.assertEqual(result["trace"][0]["outcome"], "INVALID_ARGUMENTS")

    def test_tool_call_limit(self):
        msg = AIMessage(content="", tool_calls=[
            {"name": "multiply", "args": {"a": 1, "b": 1}, "id": f"call-{i}"}
            for i in range(MAX_TOOL_CALLS + 1)
        ])
        self.assertEqual(run_tool_loop(FakeModel([msg]), "many")["status"], "LIMIT_REACHED")

    def test_empty_request(self):
        with self.assertRaises(ValueError):
            run_tool_loop(FakeModel([]), "")

if __name__ == "__main__":
    unittest.main()
