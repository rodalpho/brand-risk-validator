# Brand Risk Validator

A lightweight, serverless content safety validation service that checks text against prohibited categories to ensure platform compliance and brand safety.

## Features

- **Real-time Content Validation** - Instant keyword-based scanning against prohibited categories
- **Risk Scoring** - Quantified risk assessment (0-100) for nuanced content evaluation
- **Multiple Categories** - Validates against gambling, cryptocurrency, adult content, medical claims, and financial advice
- **Serverless Architecture** - Deployed on Vercel for automatic scaling and high availability
- **Opal Tool Registry Integration** - Discoverable schema for seamless tool integration
- **Zero Dependencies** - Uses only Python standard library for minimal overhead

## Quick Start

### Test the API

```bash
curl -X POST https://your-deployment.vercel.app/api/validate \
  -H "Content-Type: application/json" \
  -d '{"content":"Check this text for safety"}'
```

Response:
```json
{
  "is_safe": true,
  "risk_score": 0,
  "violations": [],
  "flagged_terms": []
}
```

## API Documentation

### POST `/api/validate`

Validates text content against prohibited keyword categories.

**Request:**
```json
{
  "content": "Text to validate (required, string)"
}
```

**Response:**
```json
{
  "is_safe": boolean,
  "risk_score": number,
  "violations": string[],
  "flagged_terms": string[]
}
```

**Response Fields:**

- `is_safe` - `true` if no prohibited keywords found, `false` otherwise
- `risk_score` - Numeric score 0-100 (25 points per flagged term, capped at 100)
- `violations` - Array of categories where violations occurred
- `flagged_terms` - Specific keywords that were matched

**Categories:**

- `gambling` - Casino, betting, slots keywords
- `cryptocurrency` - Crypto trading and investment terms
- `adult_content` - Adult/NSFW content indicators
- `medical_claims` - Unverified health claims
- `financial_advice` - Investment advice and financial promises

**Examples:**

Safe content:
```bash
curl -X POST https://your-deployment.vercel.app/api/validate \
  -H "Content-Type: application/json" \
  -d '{"content":"Welcome to our platform"}'
# Response: {"is_safe": true, "risk_score": 0, "violations": [], "flagged_terms": []}
```

Flagged content:
```bash
curl -X POST https://your-deployment.vercel.app/api/validate \
  -H "Content-Type: application/json" \
  -d '{"content":"Play slots and win bitcoin prizes"}'
# Response: {"is_safe": false, "risk_score": 50, "violations": ["gambling", "cryptocurrency"], "flagged_terms": ["slots", "bitcoin"]}
```

### GET `/api/discovery`

Returns the Opal Tool Registry discovery schema for tool integration. This endpoint enables automatic tool discovery and integration with platforms that support the Opal Tool Registry format.

**Request:**
```bash
curl https://your-deployment.vercel.app/api/discovery
```

**Response:**
```json
{
  "functions": [
    {
      "name": "validateContent",
      "description": "Validates content against prohibited categories (gambling, cryptocurrency, adult content, medical claims, financial advice) to ensure platform compliance and brand safety before publication",
      "parameters": [
        {
          "name": "content",
          "type": "string",
          "description": "Text content to validate for brand risk",
          "required": true
        }
      ],
      "endpoint": "/api/validate",
      "httpmethod": "POST"
    }
  ]
}
```

**Schema Fields:**

- `functions` - Array of available validation functions
  - `name` - Function identifier (`validateContent`)
  - `description` - Human-readable description of the validation capabilities
  - `parameters` - Array of function parameters
    - `name` - Parameter name
    - `type` - Data type (string)
    - `description` - Parameter description
    - `required` - Whether parameter is required (true)
  - `endpoint` - API endpoint path to call (`/api/validate`)
  - `httpmethod` - HTTP method to use (POST)

**Integration:**

This endpoint allows tools and platforms to automatically discover and integrate the brand risk validation service without manual configuration. The discovery schema follows the Opal Tool Registry format for standardized tool discovery.

See `api/discovery.py:4-21` for the discovery schema definition.

### GET `/api/health`

Health check endpoint (returns 200 OK if service is running).

## Architecture

```
brand-risk-validator/
├── api/
│   ├── validate.py          # Main validation handler
│   ├── discovery.py         # Tool registry schema
│   └── discovery.json       # OpenAPI specification
├── vercel.json              # Deployment configuration
└── README.md
```

**Key Components:**

- **`api/validate.py`** - Core validation logic using word-boundary regex matching
- **`api/discovery.py`** - Opal Tool Registry integration schema
- **`vercel.json`** - Routes and build configuration for Vercel

**Validation Algorithm:**

1. Convert input text to lowercase for case-insensitive matching
2. Apply word-boundary regex patterns for each prohibited keyword
3. Track matched categories and specific terms
4. Calculate risk score (25 points per unique flagged term, max 100)
5. Return validation result with detailed breakdown

## Local Development

### Prerequisites

- Python 3.7+
- Vercel CLI (optional, for local testing)

### Run Locally with Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Start local dev server
vercel dev
```

The API will be available at `http://localhost:3000`

### Test Validation Logic

```python
# Test in Python REPL
python3 -c "
from api.validate import handler, PROHIBITED_KEYWORDS
import json

# View available categories
print('Categories:', list(PROHIBITED_KEYWORDS.keys()))

# Simulate validation
class MockRequest:
    def get_json(self):
        return {'content': 'test casino and bitcoin'}

result = handler(MockRequest())
print(result)
"
```

## Deployment

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

### Environment Variables

No environment variables required - the service uses static keyword lists.

## Customization

### Adding Prohibited Keywords

Edit `api/validate.py` and add terms to the `PROHIBITED_KEYWORDS` dictionary:

```python
PROHIBITED_KEYWORDS = {
    'gambling': ['casino', 'slots', 'betting', ...],
    'cryptocurrency': ['bitcoin', 'crypto', ...],
    'your_category': ['keyword1', 'keyword2', ...],
    # Add more categories as needed
}
```

See `api/validate.py:5-12` for the current keyword definitions.

### Adjusting Risk Scoring

Modify the risk calculation in `api/validate.py:75`:

```python
# Current: 25 points per term, capped at 100
risk_score = min(len(flagged_terms) * 25, 100)

# Example: 20 points per term, capped at 80
risk_score = min(len(flagged_terms) * 20, 80)
```

## Technical Details

- **Language:** Python 3
- **Framework:** Serverless functions (Vercel)
- **Validation Method:** Word-boundary regex matching
- **CORS:** Enabled (`Access-Control-Allow-Origin: *`)
- **Response Format:** JSON
- **Matching:** Case-insensitive with word boundaries to prevent partial matches

## Limitations

- Keyword-based detection only (no ML/AI semantic analysis)
- Static keyword lists require manual updates
- May produce false positives with legitimate content containing flagged words
- No context-aware or intent-based analysis

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Support

For issues and questions, please [create an issue](https://github.com/your-org/brand-risk-validator/issues).
