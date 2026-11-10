-- AK-01 initial PostgreSQL schema baseline

CREATE TABLE IF NOT EXISTS knowledge_jobs (
    id VARCHAR(64) PRIMARY KEY,
    target JSONB NOT NULL,
    policy JSONB NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'CREATED',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS sources (
    id VARCHAR(64) PRIMARY KEY,
    job_id VARCHAR(64) NOT NULL REFERENCES knowledge_jobs(id),
    title VARCHAR(512) NOT NULL,
    version VARCHAR(64) NOT NULL,
    content TEXT NOT NULL,
    content_hash VARCHAR(64) NOT NULL,
    locator VARCHAR(512) NOT NULL DEFAULT 'body',
    quarantined BOOLEAN NOT NULL DEFAULT false,
    stale BOOLEAN NOT NULL DEFAULT false,
    UNIQUE(job_id, content_hash, version)
);

CREATE TABLE IF NOT EXISTS knowledge_units (
    id VARCHAR(64) PRIMARY KEY,
    job_id VARCHAR(64) NOT NULL REFERENCES knowledge_jobs(id),
    text TEXT NOT NULL,
    unit_type VARCHAR(64) NOT NULL,
    state VARCHAR(32) NOT NULL,
    scope_layer VARCHAR(32) NOT NULL,
    provenance JSONB NOT NULL,
    canonical_id VARCHAR(256)
);

CREATE TABLE IF NOT EXISTS capsule_versions (
    id BIGSERIAL PRIMARY KEY,
    capsule_id VARCHAR(64) NOT NULL,
    version VARCHAR(32) NOT NULL,
    payload JSONB NOT NULL,
    released BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS outbox_events (
    id VARCHAR(64) PRIMARY KEY,
    event_type VARCHAR(128) NOT NULL,
    payload JSONB NOT NULL,
    delivered BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
