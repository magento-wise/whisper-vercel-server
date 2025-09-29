from http.server import BaseHTTPRequestHandler
import json
import yt_dlp
import requests
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
                self.send_error(400, "Missing video_id")
                return
            
            # Get video info and audio URL
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f'https://www.youtube.com/watch?v={video_id}', download=False)
                title = info.get('title', 'Unknown')
                
                # For now, return a placeholder transcript
                # In production, you'd integrate with a real transcription service
                transcript = f"This is a placeholder transcript for: {title}. The Whisper server is running but needs a transcription service integration."
                
                result = {
                    'success': True,
                    'transcript': transcript,
                    'title': title,
                    'video_id': video_id,
                    'language': 'en',
                    'model_used': 'placeholder',
                    'duration': info.get('duration', 0)
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(result).encode())
                
        except Exception as e:
            error_result = {
                'success': False,
                'error': str(e)
            }
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_result).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
