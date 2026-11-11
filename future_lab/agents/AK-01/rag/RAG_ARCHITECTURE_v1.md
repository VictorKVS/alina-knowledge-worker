# AK-01 RAG Architecture v1

AK-01 itself requires a private operational RAG distinct from target-agent RAGs.

## AK-01 own knowledge base

1. Knowledge Engineering
- ontology design
- taxonomy
- knowledge graphs
- provenance
- epistemic typing
- contradiction handling
- versioning

2. RAG Engineering
- document ingestion
- chunking
- embeddings
- sparse retrieval
- vector retrieval
- hybrid search
- reranking
- graph RAG
- citation grounding
- retrieval evaluation

3. Agent Engineering
- agent roles
- capabilities
- tool contracts
- memory
- planning
- policies
- human gates
- prompt architecture
- agent evaluation

4. Evidence Engineering
- source hierarchy
- primary vs secondary evidence
- source authority
- uncertainty
- claim-evidence linking
- source freshness

5. Knowledge-to-Agent Engineering
- role decomposition
- task decomposition
- capability mapping
- prerequisite graphs
- knowledge pack design
- prompt generation specifications
- RAG generation specifications

## Retrieval layers

QUERY
→ intent/task classifier
→ target-agent context
→ metadata filter
→ hybrid retrieval
→ graph expansion
→ reranker
→ evidence/trust filter
→ contradiction expansion
→ grounded context bundle

## Mandatory metadata

source_id
source_type
title
author
edition
year
chapter
section
page
topic
knowledge_type
evidence_class
authority
target_agent
task
capability
version
valid_from
valid_to
extraction_status

## Retrieval rule

A high vector similarity score must never override evidence policy.
