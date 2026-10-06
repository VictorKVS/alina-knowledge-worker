"""Structured work-process registry and run state for Alina Analyst."""
from __future__ import annotations

import json
from pathlib import Path
import time
import uuid

TERMINAL = {"DONE", "BLOCKED", "NOT_APPLICABLE", "REVIEW_REQUIRED"}
STEP_STATES = {"PENDING", "READY", "IN_PROGRESS", *TERMINAL}
RUN_STATES = {"READY", "IN_PROGRESS", "DONE", "BLOCKED", "REVIEW_REQUIRED"}


def init(db, base: Path) -> None:
    db.executescript("""
    CREATE TABLE IF NOT EXISTS process_definitions(
      process_id TEXT PRIMARY KEY,
      version TEXT NOT NULL,
      title TEXT NOT NULL,
      domain TEXT,
      agent_role TEXT,
      schema_name TEXT NOT NULL,
      body TEXT NOT NULL,
      active INTEGER NOT NULL DEFAULT 1,
      updated REAL NOT NULL
    );

    CREATE TABLE IF NOT EXISTS process_steps(
      process_id TEXT NOT NULL,
      step_id TEXT NOT NULL,
      step_order INTEGER NOT NULL,
      title TEXT NOT NULL,
      mode TEXT,
      required INTEGER NOT NULL DEFAULT 1,
      body TEXT NOT NULL,
      PRIMARY KEY(process_id, step_id),
      FOREIGN KEY(process_id) REFERENCES process_definitions(process_id)
    );

    CREATE TABLE IF NOT EXISTS work_runs(
      run_id TEXT PRIMARY KEY,
      process_id TEXT NOT NULL,
      status TEXT NOT NULL,
      context TEXT NOT NULL,
      created REAL NOT NULL,
      updated REAL NOT NULL,
      completed REAL,
      FOREIGN KEY(process_id) REFERENCES process_definitions(process_id)
    );

    CREATE TABLE IF NOT EXISTS work_step_runs(
      run_id TEXT NOT NULL,
      step_id TEXT NOT NULL,
      step_order INTEGER NOT NULL,
      status TEXT NOT NULL,
      result TEXT,
      evidence TEXT,
      note TEXT,
      started REAL,
      finished REAL,
      PRIMARY KEY(run_id, step_id),
      FOREIGN KEY(run_id) REFERENCES work_runs(run_id)
    );
    """)
    seed_directory(db, base / "processes")


def seed_directory(db, folder: Path) -> None:
    if not folder.is_dir():
        return
    for path in sorted(folder.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
            register_process(db, payload)
        except Exception:
            # Bad process definitions must not prevent the document library from starting.
            continue


def register_process(db, payload: dict) -> None:
    process_id = payload.get("id")
    title = payload.get("title")
    schema_name = payload.get("schema")
    if not process_id or not title or not schema_name:
        raise ValueError("process requires id, title and schema")
    steps = payload.get("steps") or []
    if not steps:
        raise ValueError("process requires at least one step")

    orders = [int(step.get("order", i)) for i, step in enumerate(steps)]
    if len(set(orders)) != len(orders):
        raise ValueError("duplicate process step order")

    now = time.time()
    db.execute(
        """INSERT INTO process_definitions
           (process_id,version,title,domain,agent_role,schema_name,body,active,updated)
           VALUES(?,?,?,?,?,?,?,?,?)
           ON CONFLICT(process_id) DO UPDATE SET
             version=excluded.version,title=excluded.title,domain=excluded.domain,
             agent_role=excluded.agent_role,schema_name=excluded.schema_name,
             body=excluded.body,active=1,updated=excluded.updated""",
        (
            process_id,
            str(payload.get("version", "1")),
            title,
            payload.get("domain_id") or payload.get("domain"),
            payload.get("agent_role"),
            schema_name,
            json.dumps(payload, ensure_ascii=False),
            1,
            now,
        ),
    )
    db.execute("DELETE FROM process_steps WHERE process_id=?", (process_id,))
    for index, step in enumerate(sorted(steps, key=lambda x: int(x.get("order", 0)))):
        step_id = step.get("id")
        if not step_id:
            raise ValueError("process step requires id")
        db.execute(
            """INSERT INTO process_steps
               (process_id,step_id,step_order,title,mode,required,body)
               VALUES(?,?,?,?,?,?,?)""",
            (
                process_id,
                step_id,
                int(step.get("order", index)),
                step.get("title", step_id),
                step.get("mode"),
                1 if step.get("required", True) else 0,
                json.dumps(step, ensure_ascii=False),
            ),
        )


def list_processes(db) -> list[dict]:
    rows = db.execute(
        """SELECT p.process_id,p.version,p.title,p.domain,p.agent_role,p.active,p.updated,
                  COUNT(s.step_id) steps
           FROM process_definitions p
           LEFT JOIN process_steps s ON s.process_id=p.process_id
           WHERE p.active=1
           GROUP BY p.process_id
           ORDER BY p.title"""
    ).fetchall()
    return [dict(row) for row in rows]


def get_process(db, process_id: str) -> dict | None:
    row = db.execute(
        "SELECT body FROM process_definitions WHERE process_id=? AND active=1",
        (process_id,),
    ).fetchone()
    return json.loads(row[0]) if row else None


def create_run(db, process_id: str, context: dict | None = None) -> dict:
    process = get_process(db, process_id)
    if not process:
        raise ValueError("unknown process")
    run_id = "RUN-" + uuid.uuid4().hex[:16].upper()
    now = time.time()
    db.execute(
        "INSERT INTO work_runs VALUES(?,?,?,?,?,?,NULL)",
        (run_id, process_id, "READY", json.dumps(context or {}, ensure_ascii=False), now, now),
    )
    steps = sorted(process.get("steps", []), key=lambda x: int(x.get("order", 0)))
    for index, step in enumerate(steps):
        db.execute(
            "INSERT INTO work_step_runs VALUES(?,?,?,?,NULL,NULL,NULL,NULL,NULL)",
            (
                run_id,
                step["id"],
                int(step.get("order", index)),
                "READY" if index == 0 else "PENDING",
            ),
        )
    return run_status(db, run_id)


def run_status(db, run_id: str) -> dict | None:
    run = db.execute("SELECT * FROM work_runs WHERE run_id=?", (run_id,)).fetchone()
    if not run:
        return None
    steps = [
        dict(row)
        for row in db.execute(
            """SELECT step_id,step_order,status,result,evidence,note,started,finished
               FROM work_step_runs WHERE run_id=? ORDER BY step_order""",
            (run_id,),
        ).fetchall()
    ]
    for step in steps:
        for key in ("result", "evidence"):
            if step[key]:
                try:
                    step[key] = json.loads(step[key])
                except json.JSONDecodeError:
                    pass
    total = len(steps)
    terminal = sum(1 for step in steps if step["status"] in TERMINAL)
    return {
        **dict(run),
        "context": json.loads(run["context"]),
        "steps": steps,
        "progress": round(100 * terminal / total, 1) if total else 0.0,
        "terminal_steps": terminal,
        "total_steps": total,
    }


def next_step(db, run_id: str) -> dict | None:
    row = db.execute(
        """SELECT w.step_id,w.step_order,w.status,s.title,s.mode,s.required,s.body
           FROM work_step_runs w
           JOIN work_runs r ON r.run_id=w.run_id
           JOIN process_steps s ON s.process_id=r.process_id AND s.step_id=w.step_id
           WHERE w.run_id=? AND w.status IN ('READY','IN_PROGRESS')
           ORDER BY w.step_order LIMIT 1""",
        (run_id,),
    ).fetchone()
    if not row:
        return None
    result = dict(row)
    result["definition"] = json.loads(result.pop("body"))
    return result


def update_step(
    db,
    run_id: str,
    step_id: str,
    status: str,
    result: dict | None = None,
    evidence: list | dict | None = None,
    note: str | None = None,
) -> dict:
    if status not in STEP_STATES:
        raise ValueError("invalid step status")

    row = db.execute(
        "SELECT step_order,status FROM work_step_runs WHERE run_id=? AND step_id=?",
        (run_id, step_id),
    ).fetchone()
    if not row:
        raise ValueError("unknown run step")

    now = time.time()
    started = now if status == "IN_PROGRESS" else None
    finished = now if status in TERMINAL else None
    db.execute(
        """UPDATE work_step_runs
           SET status=?,result=?,evidence=?,note=?,
               started=COALESCE(started,?),finished=?
           WHERE run_id=? AND step_id=?""",
        (
            status,
            json.dumps(result, ensure_ascii=False) if result is not None else None,
            json.dumps(evidence, ensure_ascii=False) if evidence is not None else None,
            note,
            started,
            finished,
            run_id,
            step_id,
        ),
    )

    if status in TERMINAL:
        next_row = db.execute(
            """SELECT step_id FROM work_step_runs
               WHERE run_id=? AND step_order>? AND status='PENDING'
               ORDER BY step_order LIMIT 1""",
            (run_id, row["step_order"]),
        ).fetchone()
        if next_row:
            db.execute(
                "UPDATE work_step_runs SET status='READY' WHERE run_id=? AND step_id=?",
                (run_id, next_row["step_id"]),
            )

    _refresh_run(db, run_id)
    return run_status(db, run_id)


def _refresh_run(db, run_id: str) -> None:
    rows = db.execute(
        "SELECT status FROM work_step_runs WHERE run_id=? ORDER BY step_order",
        (run_id,),
    ).fetchall()
    statuses = [row[0] for row in rows]
    now = time.time()

    if statuses and all(status in TERMINAL for status in statuses):
        final = "REVIEW_REQUIRED" if "REVIEW_REQUIRED" in statuses else (
            "BLOCKED" if "BLOCKED" in statuses else "DONE"
        )
        db.execute(
            "UPDATE work_runs SET status=?,updated=?,completed=? WHERE run_id=?",
            (final, now, now, run_id),
        )
    else:
        active = "IN_PROGRESS" if any(status in {"IN_PROGRESS", *TERMINAL} for status in statuses) else "READY"
        db.execute(
            "UPDATE work_runs SET status=?,updated=? WHERE run_id=?",
            (active, now, run_id),
        )


def summary(db) -> dict:
    definitions = db.execute(
        "SELECT COUNT(*) FROM process_definitions WHERE active=1"
    ).fetchone()[0]
    runs = dict(
        db.execute("SELECT status,COUNT(*) FROM work_runs GROUP BY status").fetchall()
    )
    active = db.execute(
        """SELECT run_id,process_id,status,updated
           FROM work_runs WHERE status NOT IN ('DONE','BLOCKED')
           ORDER BY updated DESC LIMIT 10"""
    ).fetchall()
    return {
        "definitions": definitions,
        "runs": runs,
        "active_runs": [dict(row) for row in active],
    }
