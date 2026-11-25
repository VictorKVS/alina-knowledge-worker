"""Offline regression tests; no API/network."""
import unittest
from dual_agents import World, run_episode, choose_rule, score

class DualAgentsTests(unittest.TestCase):
    def test_story_baseline(self):
        result = run_episode("story", "balanced")
        self.assertTrue(result["success"])
        self.assertEqual(result["final"]["facts"], ["clue", "establish", "reveal"])
        self.assertEqual(len(result["trace"]), 3)
    def test_game_reaches_goal(self):
        result = run_episode("game", "balanced")
        self.assertTrue(result["success"])
        self.assertEqual(result["final"]["position"], 2)
        self.assertGreater(result["final"]["hp"], 0)
    def test_careful_game_scouts(self):
        result = run_episode("game", "careful")
        self.assertEqual(result["trace"][0]["chosen"]["name"], "scout")
    def test_rush_rejected_as_unsafe(self):
        w = World("game")
        self.assertEqual(score(next(a for a in w.available() if a.name == "rush"),w,"fast"),float("-inf"))
    def test_no_reveal_without_clue(self):
        w = World("story")
        self.assertNotIn("reveal", {a.name for a in w.available()})
    def test_illegal_action_blocked(self):
        w=World("story")
        from dual_agents import Option
        with self.assertRaises(ValueError):
            w.step(Option("reveal","illegal",1,0,10))
    def test_budget_finite(self):
        for kind in ("story","game"):
            for strategy in ("fast","balanced","careful"):
                result=run_episode(kind,strategy)
                self.assertGreaterEqual(result["final"]["budget"],0)
                self.assertLessEqual(len(result["trace"]),4)

if __name__ == "__main__":
    unittest.main()
