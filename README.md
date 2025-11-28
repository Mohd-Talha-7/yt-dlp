# YouTube Downloader API

## Quick Deploy Options

### 1. Railway (Easiest - Free Tier)
1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub"
4. Select your repo
5. Done! Get your URL

### 2. Render.com (Free Tier)
1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. New → Web Service → Connect repo
4. Done! Get your URL

### 3. Docker (Any VPS/EC2)
```bash
docker-compose up -d
```

### 4. AWS EC2
```bash
# SSH into EC2
sudo apt update
sudo apt install docker.io docker-compose -y
git clone <your-repo>
cd yt-dlp
docker-compose up -d
```

## Local Testing
```bash
docker build -t yt-api .
docker run -p 8000:8000 yt-api
```

## API Endpoints
- POST `/download` - Download video
- GET `/video/{filename}` - Get video file
- GET `/docs` - API documentation
