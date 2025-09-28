from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            models_info = {
                "available_models": [
                    {
                        "name": "tiny",
                        "size": "~39 MB",
                        "speed": "Fastest",
                        "accuracy": "Basic",
                        "recommended_for": "Quick tests, very short videos",
                        "vercel_compatible": True
                    },
                    {
                        "name": "base", 
                        "size": "~74 MB",
                        "speed": "Fast",
                        "accuracy": "Good",
                        "recommended_for": "Most use cases (RECOMMENDED)",
                        "vercel_compatible": True
                    },
                    {
                        "name": "small",
                        "size": "~244 MB",
                        "speed": "Medium",
                        "accuracy": "Better",
                        "recommended_for": "Higher quality needs",
                        "vercel_compatible": False,
                        "note": "Too large for Vercel deployment"
                    }
                ],
                "current_model": os.environ.get('WHISPER_MODEL', 'base'),
                "server_limits": {
                    "max_duration": f"{os.environ.get('MAX_AUDIO_DURATION', '300')} seconds",
                    "timeout": "60 seconds (Pro) / 10 seconds (Hobby)",
                    "memory": "3GB (Pro) / 1GB (Hobby)",
                    "deployment": "Vercel Serverless"
                },
                "recommendations": {
                    "model": "Use 'base' for best balance of speed and accuracy",
                    "plan": "Upgrade to Vercel Pro for 60-second timeout",
                    "video_length": "Keep videos under 5 minutes for best performance"
                }
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            self.wfile.write(json.dumps(models_info, indent=2).encode())
            
        except Exception as e:
            error_response = {
                "error": str(e),
                "available_models": []
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
