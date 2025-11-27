from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import yt_dlp
import os
import uuid

app = FastAPI()

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
            'quiet': True
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
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/video/{filename}")
async def get_video(filename: str):
    file_path = f"downloads/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(file_path)
