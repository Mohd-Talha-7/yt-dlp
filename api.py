from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import os
import uuid
import time

app = FastAPI(title="YouTube Downloader API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str

@app.post("/download")
async def download_video(request: VideoRequest):
    try:
        video_id = str(uuid.uuid4())
        output_path = f"downloads/{video_id}.%(ext)s"
        
        os.makedirs("downloads", exist_ok=True)
        
        ydl_opts = {
            'outtmpl': output_path,
            'quiet': False,
            'no_warnings': False,
            'format': 'best[ext=mp4]/best',
            'socket_timeout': 30,
            'retries': 3,
            'fragment_retries': 3,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(request.url, download=True)
            ext = info.get('ext', 'mp4')
            final_path = f"downloads/{video_id}.{ext}"
        
        return {
            "status": "success",
            "video_path": final_path,
            "download_url": f"/video/{video_id}.{ext}"
        }
    
    except Exception as e:
        error_msg = str(e)
        if "Sign in to confirm" in error_msg:
            raise HTTPException(
                status_code=429,
                detail="YouTube bot detection triggered. Try: 1) Different video 2) YouTube Shorts 3) Wait 5 minutes"
            )
        raise HTTPException(status_code=400, detail=error_msg)

@app.get("/video/{filename}")
async def get_video(filename: str):
    file_path = f"downloads/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(file_path)
