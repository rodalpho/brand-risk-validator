# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Brand Risk Validator** is a content safety validation service deployed on Vercel that integrates with the Opal Tool Registry. It validates text content against prohibited categories to ensure platform compliance and brand safety.

### Architecture

The project follows a serverless architecture with Vercel, using Python HTTP request handlers:

- **`api/validate.py`** - Main handler for POST `/api/validate` endpoint that performs keyword-based content validation. Returns `is_safe` boolean, `risk_score` (0-100), `violations` array (categories found), and `flagged_terms` array (specific keywords matched). Uses word-boundary regex matching against prohibited keyword lists organized by category (gambling, cryptocurrency, adult_content, medical_claims, financial_advice).

- **`api/discovery.py`** - Serves Opal Tool Registry discovery schema at GET `/api/discovery`. Returns JSON describing the validateContent function for tool integration.

- **`api/discovery/api/validate.py`** - Mirrors `api/discovery.py`, also returns discovery schema (appears to be a redundant/alternative implementation).

- **`api/discovery.json`** - OpenAPI 3.0 specification document that formally documents the `/api/validate` endpoint with request/response schemas.

- **`vercel.json`** - Vercel deployment configuration that maps Python handler files to routes and defines the build process using `@vercel/python`.

### Key Design Decisions

1. **Keyword-based approach** - Content validation uses word-boundary regex matching against static prohibited keyword lists. This is performant but limited to known keywords.

2. **Risk scoring** - Each flagged term adds 25 points (capped at 100), providing a quantified risk level.

3. **Multiple discovery endpoints** - The project has three discovery implementations (validate.py, discovery.py, and discovery.json), suggesting either migration/consolidation opportunity or support for multiple tool registry formats.

4. **Stateless, serverless design** - No external dependencies or database, making it lightweight and scalable.

## Commands

### Local Development

```bash
# Test content validation locally (requires Python 3)
python3 -c "
from api.validate import handler, PROHIBITED_KEYWORDS
import json

# Test input
test_content = {'content': 'check for casino keywords'}
result = json.dumps(test_content)
print(f'Prohibited keywords available: {list(PROHIBITED_KEYWORDS.keys())}')
"

# Start local HTTP server (Vercel CLI provides better local experience)
python3 -m http.server 8000 --directory .
```

### Testing Endpoints

```bash
# Test validation endpoint
curl -X POST http://localhost:3000/api/validate \
  -H "Content-Type: application/json" \
  -d '{"content":"This mentions bitcoin and slots"}'

# Test discovery endpoint
curl -X GET http://localhost:3000/api/discovery

# Test health check
curl -X GET http://localhost:3000/api/health
```

### Deployment

```bash
# Deploy to Vercel (requires Vercel CLI)
vercel deploy

# Deploy to production
vercel deploy --prod
```

## Important Code Locations

- **Prohibited keywords definition** - `api/validate.py:5-12`
- **Risk calculation logic** - `api/validate.py:75`
- **Keyword matching regex** - `api/validate.py:70` (uses word boundaries to avoid partial matches)
- **Discovery schema** - `api/validate.py:15-32` and `api/discovery.py:4-21`

## Development Notes

- The `requirements.txt` appears to be mostly empty (Flask commented out), as the project uses only Python standard library (`http.server`, `json`, `re`).
- Adding new prohibited keywords should be done in the `PROHIBITED_KEYWORDS` dict in `api/validate.py`.
- Discovery schema is duplicated across multiple files - consider consolidating before scaling.
- CORS headers (`Access-Control-Allow-Origin: *`) are set on responses to allow cross-origin integration with Opal registry.
- Content validation is case-insensitive (lowercased before matching).
- Duplicate flagged terms are removed using `set()` in the response.

## Files to Know

- `vercel.json` - Defines build and routing configuration
- `api/discovery.json` - OpenAPI specification for API documentation
