# C0.2 Database Inventory — GitHub-visible pass

Status: PARTIAL / LOCAL PROBE REQUIRED

The GitHub-visible pass did not provide sufficient authoritative schema discovery for all historical FATHER/ALINA stores. Empty code-search results are therefore treated as UNKNOWN, not as proof that a datastore does not exist.

Known architectural stores from canonical documentation remain candidates to verify: ALINA SQLite/FTS runtime; PostgreSQL/temporal stores; graph stores such as Neo4j/SecGraph; vector stores such as Qdrant/Milvus/pgvector; historical Security KB / OSINT KB instances.

## Safety decision
A read-only local probe is provided. It inventories paths, sizes, hashes, SQLite tables/columns/indexes/foreign keys, and SQL/Compose artifact metadata. It does not read .env secrets or document bodies and does not mutate databases.

## Gate
C0.2 can finish after the local JSON result is returned and merged with repository evidence. Then C0.3 performs schema mapping and C0.4 duplicate detection.
