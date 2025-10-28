# Content Safety Validator

API for validating content against prohibited categories for platform compliance.

## Endpoint
POST /api/validate

## Input
{"content": "text to validate"}

## Output
{"is_safe": true, "risk_score": 0, "violations": [], "flagged_terms": []}
