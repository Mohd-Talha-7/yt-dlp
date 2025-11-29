from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from urllib.parse import urlparse, parse_qs
import requests

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
            elif "youtu.be/" in url:
                video_id = url.split("youtu.be/")[-1].split("?")[0]
            elif "/" in url:
                video_id = url.split("/")[-1].split("?")[0]
            else:
                raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        
        if isinstance(video_id, list):
            video_id = video_id[0]
        
        # Fetch available formats from Invidious
        meta = requests.get(f"{INVIDIOUS_INSTANCE}/api/v1/videos/{video_id}", timeout=10).json()
        
        # Get all formats
        formats = meta.get("adaptiveFormats", []) + meta.get("formatStreams", [])
        
        # Priority: 22 (720p MP4) > 18 (360p MP4) > 140 (audio)
        preferred_itags = ["22", "18", "140"]
        selected_url = None
        itag_used = None
        
        for itag in preferred_itags:
            for fmt in formats:
                if str(fmt.get("itag")) == itag:
                    selected_url = fmt.get("url")
                    itag_used = itag
                    break
            if selected_url:
                break
        
        if not selected_url:
            raise HTTPException(status_code=404, detail="No compatible format found")
        
        quality_map = {"22": "720p MP4", "18": "360p MP4", "140": "Audio Only"}
        
        return {
            "status": "success",
            "video_id": video_id,
            "download_url": selected_url,
            "quality": quality_map.get(itag_used, "Unknown"),
            "note": "Use this URL to directly download the video"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
