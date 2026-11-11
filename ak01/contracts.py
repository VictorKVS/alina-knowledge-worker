from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class TargetAgentProfile(BaseModel):
    id: str
    role: str
    tasks: list[str] = Field(default_factory=list)
    required_capabilities: list[str] = Field(default_factory=list)


class EvidencePolicy(BaseModel):
    minimum_state_for_runtime_use: str = "VERIFIED"
    wikipedia_only_for_qualification: bool = False
    require_provenance: bool = True


class CreateKnowledgeJob(BaseModel):
    target_agent: TargetAgentProfile
    evidence_policy: EvidencePolicy


class RegisterSource(BaseModel):
    title: str
    version: str = "1"
    content: str
    source_type: str = "TEXT"
    locator: str = "body"


class KnowledgeUnitView(BaseModel):
    id: str
    text: str
    type: str
    state: str
    scope_layer: str
    source_version_id: str | None = None
    source_fragment_id: str | None = None
    source_hash: str | None = None
    locator: str | None = None
    canonical_id: str | None = None


class ErrorEnvelope(BaseModel):
    code: str
    category: str
    message: str
    retryable: bool
    correlation_id: str
    details: dict[str, Any] = Field(default_factory=dict)
