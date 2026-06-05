from http.server import BaseHTTPRequestHandler
import requests, json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        from urllib.parse import urlparse, parse_qs
        query = parse_qs(urlparse(self.path).query)
        api_key = query.get("api_key", [""])[0]
        number = query.get("number", [""])[0]
        
        # 🔥 Apni marzi ki API key set karo
        if api_key != "leekdata":
            self.send_response(401)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status":"error","message":"Invalid API key"}).encode())
            return
        
        if not number or len(number)!=10 or not number.isdigit():
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status":"error","message":"10-digit number required"}).encode())
            return
        
        # Real data fetch original API se
        resp = requests.get(
            "https://number-to-api-team-only.vercel.app/api/index.js",
            params={"api_key": "team6months", "number": number},
            timeout=10
        )
        data = resp.json()
        
        # Clean response
        data.pop("timestamp", None)
        data.pop("count", None)
        data["developer"] = "RedRose Member"
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
