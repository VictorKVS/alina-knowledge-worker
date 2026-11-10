from __future__ import annotations

from fastapi import FastAPI, HTTPException

from .application import KnowledgeApplication
from .contracts import CreateKnowledgeJob, RegisterSource
from .events import InMemoryEventBus
from .middleware import CorrelationIdMiddleware
from .repositories import InMemoryJobRepository


jobs = InMemoryJobRepository()
events = InMemoryEventBus()
app_service = KnowledgeApplication(jobs, events)

app = FastAPI(title="AK-01 ALINA Knowledge Architect", version="0.1.0")
app.add_middleware(CorrelationIdMiddleware)


@app.get("/health/live")
def health_live():
    return {"status": "ok"}


@app.get("/health/ready")
def health_ready():
    return {"status": "ready"}


@app.post("/v1/knowledge-jobs")
def create_job(command: CreateKnowledgeJob):
    job = app_service.create_job(
        command.target_agent.model_dump(),
        command.evidence_policy.model_dump(),
    )
    return {"id": job.id, "status": "CREATED"}


@app.post("/v1/knowledge-jobs/{job_id}/sources")
def add_source(job_id: str, command: RegisterSource):
    try:
        return app_service.register_source(job_id, command.model_dump())
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="knowledge job not found") from exc


@app.get("/v1/knowledge-jobs/{job_id}")
def get_job(job_id: str):
    try:
        job = jobs.get(job_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="knowledge job not found") from exc
    return {
        "id": job.id,
        "target": job.target,
        "policy": job.policy,
        "source_count": len(job.sources),
        "unit_count": len(job.units),
    }
