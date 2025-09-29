from http.server import BaseHTTPRequestHandler
import json
import yt_dlp
import requests
import tempfile
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            video_id = data.get('video_id')
            if not video_id:
                raise ValueError("video_id is required")
            
            # Download audio using yt-dlp
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'extractaudio': True,
                'audioformat': 'mp3',
                'outtmpl': f'/tmp/{video_id}.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
            
            # For now, return a placeholder response
            # In production, you would send the audio to an external Whisper API
            response = {
                "success": True,
                "video_id": video_id,
                "title": title,
                "duration": duration,
                "transcript": "This is a placeholder transcript. Audio downloaded successfully but Whisper processing requires external API.",
                "language": "en",
                "model_used": "external_api",
                "processing_time": 1.0,
                "message": "Audio extraction successful. Connect to external Whisper API for transcription."
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            error_response = {
                "success": False,
                "error": str(e),
                "video_id": data.get('video_id', 'unknown') if 'data' in locals() else 'unknown'
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
