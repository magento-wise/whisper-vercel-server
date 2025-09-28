from http.server import BaseHTTPRequestHandler
import json
import os
import tempfile
import subprocess
from pathlib import Path

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            video_id = request_data.get('video_id')
            url = request_data.get('url', f'https://www.youtube.com/watch?v={video_id}')
            model_size = request_data.get('model_size', os.environ.get('WHISPER_MODEL', 'base'))
            
            if not video_id:
                raise ValueError("video_id is required")
            
            print(f"🎤 Starting Whisper transcription for video: {video_id}")
            print(f"🤖 Using model: {model_size}")
            
            # Import required libraries
            import whisper
            import yt_dlp
            
            # Load Whisper model
            model = whisper.load_model(model_size)
            print(f"✅ Whisper model '{model_size}' loaded successfully")
            
            # Create temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                audio_path = os.path.join(temp_dir, f"{video_id}.%(ext)s")
                
                # Configure yt-dlp for audio extraction
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': audio_path,
                    'extractaudio': True,
                    'audioformat': 'wav',
                    'audioquality': '192K',
                    'no_warnings': True,
                    'quiet': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'wav',
                        'preferredquality': '192',
                    }]
                }
                
                print(f"📥 Downloading audio from: {url}")
                
                # Download audio
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', f'Video {video_id}')
                    duration = info.get('duration', 0)
                    
                    print(f"📹 Video: {title}")
                    print(f"⏱️ Duration: {duration} seconds")
                    
                    # Check duration limit
                    max_duration = int(os.environ.get('MAX_AUDIO_DURATION', '300'))
                    if duration > max_duration:
                        raise ValueError(f"Video too long: {duration}s > {max_duration}s limit")
                
                # Find the downloaded audio file
                audio_files = list(Path(temp_dir).glob(f"{video_id}.*"))
                if not audio_files:
                    raise FileNotFoundError("Audio file not found after download")
                
                actual_audio_path = str(audio_files[0])
                print(f"🎵 Audio file: {actual_audio_path}")
                
                # Transcribe with Whisper
                print("🎤 Starting Whisper transcription...")
                result = model.transcribe(
                    actual_audio_path,
                    language=None,  # Auto-detect language
                    task="transcribe",
                    verbose=False
                )
                
                transcript_text = result["text"].strip()
                detected_language = result.get("language", "unknown")
                segments_count = len(result.get("segments", []))
                
                print(f"✅ Transcription completed!")
                print(f"📝 Length: {len(transcript_text)} characters")
                print(f"🌐 Language: {detected_language}")
                print(f"📊 Segments: {segments_count}")
                
                if len(transcript_text) < 10:
                    raise ValueError("Transcript too short - possible transcription failure")
                
                # Prepare response
                response = {
                    "success": True,
                    "video_id": video_id,
                    "transcript": transcript_text,
                    "language": detected_language,
                    "model_used": model_size,
                    "segments": segments_count,
                    "duration": duration,
                    "title": title,
                    "source": "whisper_vercel",
                    "server_type": "vercel_serverless"
                }
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                
                self.wfile.write(json.dumps(response).encode())
                
        except Exception as e:
            print(f"❌ Transcription error: {str(e)}")
            
            error_response = {
                "success": False,
                "error": str(e),
                "video_id": request_data.get('video_id', 'unknown') if 'request_data' in locals() else 'unknown',
                "server_type": "vercel_serverless"
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
