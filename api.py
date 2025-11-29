from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from urllib.parse import urlparse, parse_qs

app = FastAPI(title="YouTube Downloader API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

INVIDIOUS_INSTANCE = "https://inv.nadeko.net"

class VideoRequest(BaseModel):
    url: str

@app.post("/download")
def download_video(request: VideoRequest):
    try:
        url = request.url
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        video_id = query.get("v")
        
        # Handle shorts or share links
        if not video_id:
            if "shorts/" in url:
                video_id = url.split("shorts/")[-1].split("?")[0]
            elif "/" in url:
                video_id = url.split("/")[-1].split("?")[0]
            else:
                raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        
        if isinstance(video_id, list):
            video_id = video_id[0]
        
        # Build direct download URL (itag 22 = 720p MP4)
        download_url = f"{INVIDIOUS_INSTANCE}/latest_version?id={video_id}&itag=22"
        
        return {
            "status": "success",
            "video_id": video_id,
            "download_url": download_url,
            "note": "Use this URL to directly download the video"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
