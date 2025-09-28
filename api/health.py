from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Check if Whisper can be imported
            import whisper
            model_name = os.environ.get('WHISPER_MODEL', 'base')
            
            response = {
                "status": "healthy",
                "service": "whisper-vercel-server",
                "model": model_name,
                "model_loaded": True,
                "server_type": "vercel_serverless",
                "python_version": "3.9",
                "max_duration": os.environ.get('MAX_AUDIO_DURATION', '300'),
                "timestamp": "2025-09-28"
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {
                "status": "error",
                "service": "whisper-vercel-server",
                "error": str(e),
                "model_loaded": False
            }
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(error_response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
