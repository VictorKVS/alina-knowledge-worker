"""Offline reflection tests with a fake LLM, no Ollama/API calls."""
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from ch04_reflection import extract_code, static_check, parse_critique, run_reflection


class ScriptedModel:
    def __init__(self, replies):
        self.replies = iter(replies)
    def invoke(self, messages):
        return SimpleNamespace(content=next(self.replies))


VALID_CODE = '''def calculate_factorial(n):
    """Calculate factorial."""
    if n < 0:
        raise ValueError("negative")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
'''


class ReflectionTests(unittest.TestCase):
    def test_strip_markdown(self):
        self.assertEqual(extract_code("```python\n" + VALID_CODE + "```"), VALID_CODE.strip())

    def test_static_check(self):
        self.assertEqual(static_check(VALID_CODE)[:2], (True, True))
        self.assertFalse(static_check("def nope(:")[0])
        self.assertEqual(static_check("def other(): pass")[:2], (True, False))

    def test_critic_is_strict(self):
        self.assertEqual(parse_critique("CRITIQUE_PASS")[0], "CRITIQUE_PASS")
        self.assertEqual(parse_critique("CRITIQUE_PASS.")[0], "REVISE")

    def test_two_cycles(self):
        fake = ScriptedModel([
            "def calculate_factorial(n):\n    return n",
            "Missing negative case, 0!, docstring.",
            VALID_CODE,
            "CRITIQUE_PASS",
        ])
        report = run_reflection(fake)
        self.assertEqual(report["cycles"], 2)
        self.assertEqual(report["status"], "REVIEW_REQUIRED")

    def test_max_cycles_not_pass(self):
        fake = ScriptedModel(["broken", "Needs changes"])
        report = run_reflection(fake, max_cycles=1)
        self.assertEqual(report["status"], "REVIEW_REQUIRED")

    def test_false_critic_pass_not_accepted(self):
        fake = ScriptedModel(["bad python ::", "CRITIQUE_PASS"])
        report = run_reflection(fake, max_cycles=1)
        self.assertFalse(report["history"][0]["syntax_valid"])
        self.assertEqual(report["status"], "REVIEW_REQUIRED")

if __name__ == "__main__":
    unittest.main()
