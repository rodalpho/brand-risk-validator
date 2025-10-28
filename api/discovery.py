from http.server import BaseHTTPRequestHandler
import json

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
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(DISCOVERY_SCHEMA).encode())
    
    def do_POST(self):
        self.do_GET()
