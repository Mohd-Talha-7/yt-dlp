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

# Multiple Invidious instances for fallback
INVIDIOUS_INSTANCES = [
    "https://inv.nadeko.net",
    "https://invidious.flokinet.to",
    "https://iv.ggtyler.dev",
    "https://inv.in.projectsegfau.lt"
]

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
        
        # Try multiple Invidious instances
        meta = None
        for instance in INVIDIOUS_INSTANCES:
            try:
                response = requests.get(f"{instance}/api/v1/videos/{video_id}", timeout=10)
                if response.status_code == 200:
                    meta = response.json()
                    break
            except:
                continue
        
        if not meta:
            raise HTTPException(status_code=503, detail="All Invidious instances are unavailable")
        
        # Get all formats
        formats = meta.get("adaptiveFormats", []) + meta.get("formatStreams", [])
        
        if not formats:
            raise HTTPException(status_code=404, detail="No formats available for this video")
        
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
    except requests.exceptions.JSONDecodeError:
        raise HTTPException(status_code=503, detail="Invidious API returned invalid response")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")
