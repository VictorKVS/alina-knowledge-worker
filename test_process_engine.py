import sqlite3
import unittest

import process_engine


class ProcessEngineTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.row_factory = sqlite3.Row
        process_engine.init(self.db, __import__("pathlib").Path("__missing__"))
        self.definition = {
            "schema": "father.agent_work_process.v1",
            "id": "PROC-TEST",
            "version": "1",
            "title": "Synthetic process",
            "domain": "design",
            "agent_role": "TEST",
            "steps": [
                {"id": "S0", "order": 0, "title": "First", "required": True},
                {"id": "S1", "order": 1, "title": "Second", "required": True},
            ],
        }
        process_engine.register_process(self.db, self.definition)

    def tearDown(self):
        self.db.close()

    def test_registered_process_is_listed(self):
        rows = process_engine.list_processes(self.db)
        self.assertEqual(rows[0]["process_id"], "PROC-TEST")
        self.assertEqual(rows[0]["steps"], 2)

    def test_run_is_strictly_sequential(self):
        run = process_engine.create_run(self.db, "PROC-TEST", {"goal": "test"})
        run_id = run["run_id"]
        self.assertEqual(run["steps"][0]["status"], "READY")
        self.assertEqual(run["steps"][1]["status"], "PENDING")

        with self.assertRaises(ValueError):
            process_engine.update_step(self.db, run_id, "S1", "DONE")

        updated = process_engine.update_step(
            self.db, run_id, "S0", "DONE", result={"ok": True}, evidence=["E-1"]
        )
        self.assertEqual(updated["steps"][1]["status"], "READY")

        completed = process_engine.update_step(
            self.db, run_id, "S1", "DONE", result={"ok": True}, evidence=["E-2"]
        )
        self.assertEqual(completed["status"], "DONE")
        self.assertEqual(completed["progress"], 100.0)

    def test_non_done_terminal_state_requires_reason(self):
        run = process_engine.create_run(self.db, "PROC-TEST")
        with self.assertRaises(ValueError):
            process_engine.update_step(
                self.db, run["run_id"], "S0", "NOT_APPLICABLE"
            )
        result = process_engine.update_step(
            self.db,
            run["run_id"],
            "S0",
            "NOT_APPLICABLE",
            note="Synthetic reason",
        )
        self.assertEqual(result["steps"][0]["status"], "NOT_APPLICABLE")

    def test_terminal_step_cannot_be_silently_rewritten(self):
        run = process_engine.create_run(self.db, "PROC-TEST")
        process_engine.update_step(self.db, run["run_id"], "S0", "DONE")
        with self.assertRaises(ValueError):
            process_engine.update_step(
                self.db,
                run["run_id"],
                "S0",
                "REVIEW_REQUIRED",
                note="late change",
            )


if __name__ == "__main__":
    unittest.main()
