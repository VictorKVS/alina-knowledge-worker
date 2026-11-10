# AK-01 — Error Model

## Categories

VALIDATION_ERROR
AUTHORIZATION_ERROR
PROVENANCE_ERROR
SOURCE_INTEGRITY_ERROR
CONFLICT_ERROR
DEPENDENCY_UNAVAILABLE
MODEL_PROVIDER_ERROR
PERSISTENCE_ERROR
INDEX_ERROR
SECURITY_POLICY_ERROR
QUALIFICATION_ERROR
INTERNAL_ERROR

## Error envelope

```json
{
  "error": {
    "code": "PROVENANCE_MISSING",
    "category": "PROVENANCE_ERROR",
    "message": "Source-derived knowledge unit has incomplete provenance",
    "retryable": false,
    "correlation_id": "uuid",
    "details": {}
  }
}
```

## Rules
- no raw secrets in error messages
- retryable flag is explicit
- every 5xx has correlation id
- security/integrity failures emit audit events
- expected domain errors do not become generic 500
