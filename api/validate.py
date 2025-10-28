from http.server import BaseHTTPRequestHandler
import json
import re

# Prohibited keyword lists
PROHIBITED_KEYWORDS = {
    "gambling": ["casino", "poker", "betting", "slots", "jackpot", "roulette", "blackjack", "wager"],
    "cryptocurrency": ["bitcoin", "crypto", "ethereum", "blockchain", "nft", "altcoin", "mining", "defi"],
    "adult_content": ["porn", "xxx", "adult", "explicit"],
    "medical_claims": ["cure cancer", "treat disease", "fda approved", "medical miracle"],
    "financial_advice": ["guaranteed returns", "investment opportunity", "get rich quick"]
}

# Opal Tool Registry Discovery Schema
DISCOVERY_SCHEMA = {
    "functions": [
        {
            "name": "validateContent",
            "description": "Validates content against prohibited categories (gambling, cryptocurrency, adult content, medical claims, financial advice) to ensure platform compliance and brand safety before publication",
            "parameters": [
                {
                    "name": "content",
                    "type": "string",
                    "description": "Text content to validate for brand risk",
                    "required": True
                }
            ],
            "endpoint": "/api/validate",
            "httpmethod": "POST"
        }
    ]
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/discovery':
            # Return Opal tool registry format
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(DISCOVERY_SCHEMA).encode())
        
        elif self.path == '/api/health':
            # Health check endpoint
            response = {"status": "healthy", "service": "Brand Risk Validator"}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/validate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            content = data.get('content', '').lower()
            
            violations = []
            flagged_terms = []
            
            # Check content against all prohibited keywords
            for category, keywords in PROHIBITED_KEYWORDS.items():
                for keyword in keywords:
                    if re.search(r'\b' + re.escape(keyword) + r'\b', content):
                        if category not in violations:
                            violations.append(category)
                        flagged_terms.append(keyword)
            
            risk_score = min(len(flagged_terms) * 25, 100)
            is_safe = len(violations) == 0
            
            response = {
                "is_safe": is_safe,
                "risk_score": risk_score,
                "violations": violations,
                "flagged_terms": list(set(flagged_terms)),
                "message": "Content is safe for all platforms" if is_safe else "Content violates platform policies"
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
