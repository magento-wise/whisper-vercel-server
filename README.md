# 🎤 Whisper Vercel Server

OpenAI Whisper transcription server deployed on Vercel for 24/7 availability.

## 🚀 Features

- ✅ **OpenAI Whisper AI** for high-quality transcription
- ✅ **Serverless deployment** on Vercel
- ✅ **Auto-scaling** based on demand
- ✅ **Global CDN** for fast response times
- ✅ **RESTful API** for easy integration

## � API hEndpoints

### Health Check
```
GET /api/health
```

### Transcribe Video
```
POST /api/transcribe
Content-Type: application/json

{
  "video_id": "dQw4w9WgXcQ",
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

### Available Models
```
GET /api/models
```

## 🧪 Testing

```bash
# Health check
curl https://your-app.vercel.app/api/health

# Transcribe video
curl -X POST https://your-app.vercel.app/api/transcribe \
     -H "Content-Type: application/json" \
     -d '{"video_id":"dQw4w9WgXcQ"}'
```

## 🔧 Environment Variables

Set these in your Vercel dashboard:

- `WHISPER_MODEL=base` (tiny/base/small)
- `MAX_AUDIO_DURATION=300` (5 minutes max)

## 💰 Vercel Limits

- **Hobby Plan**: 10 second timeout, 1GB memory
- **Pro Plan**: 60 second timeout, 3GB memory (recommended)

## 🚀 Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/magento-wise/whisper-vercel-server)

## 📊 Performance

- **Startup**: ~10-30 seconds (cold start)
- **Transcription**: 2-5x real-time speed
- **Accuracy**: 95%+ for clear English audio
- **Supported formats**: MP4, MP3, WAV, M4A

## 🔗 Integration

Update your Enhanced Transcript Service:

```typescript
const whisperServerUrl = 'https://your-app.vercel.app'
```

## 📞 Support

For issues:
1. Check Vercel function logs
2. Verify environment variables
3. Test with curl commands
4. Check video duration limits

---

**Deployed with ❤️ on Vercel**
