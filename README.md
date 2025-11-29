# YouTube Downloader API

Simple API to get direct YouTube video download links using Invidious.

## Features
✅ No bot detection
✅ No cookies needed
✅ No CAPTCHA
✅ Works with YouTube videos and Shorts
✅ Fast and lightweight

## Quick Deploy

### Render.com (Recommended)
1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. New → Web Service → Connect repo
4. Start Command: `uvicorn api:app --host 0.0.0.0 --port $PORT`
5. Done! Get your URL

### Railway.app
1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub"
4. Select your repo
5. Done!

### Docker
```bash
docker-compose up -d
```

## API Usage

### Request
```bash
curl -X POST "https://your-app.onrender.com/download" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=VIDEO_ID"}'
```

### Response
```json
{
  "status": "success",
  "video_id": "VIDEO_ID",
  "download_url": "https://inv.nadeko.net/latest_version?id=VIDEO_ID&itag=22",
  "note": "Use this URL to directly download the video"
}
```

### Supported URLs
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtube.com/shorts/VIDEO_ID`
- `https://youtu.be/VIDEO_ID`

## API Endpoints
- POST `/download` - Get video download link
- GET `/docs` - Interactive API documentation

## Local Testing
```bash
uvicorn api:app --reload
```
Visit: http://localhost:8000/docs
