import os
import requests
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from api.schemas import VideoRequest, VideoResponse, PlaylistRequest, FetchPlaylistParams
from api.services import YouTubeService, ConverterService
from api.utils.validators import validate_youtube_url


app = FastAPI(
    title="YouTube to MP3 Converter API",
    description="API for converting YouTube videos to MP3 files with custom metadata",
    version="1.0.0"
)

# Configure CORS with more specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Add your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/videos", response_model=VideoResponse)
async def submit_video(request: VideoRequest, background_tasks: BackgroundTasks):
    """Submit a video for conversion to MP3"""
    if not validate_youtube_url(request.video_url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    # Create conversion job
    job_id = await ConverterService.create_job(request)
    
    # Start conversion in background
    background_tasks.add_task(
        ConverterService.process_video,
        job_id,
        request.video_url,
        request.metadata
    )
    
    return VideoResponse(
        id=job_id,
        status="pending"
    )

@app.get("/videos/{job_id}", response_model=VideoResponse)
async def check_status(job_id: str):
    """Check the status of a video conversion"""
    job = await ConverterService.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.post("/playlists", response_model=VideoResponse)
async def submit_playlist(request: PlaylistRequest):
    """Submit a playlist for processing"""
    playlist_info = await YoutubeService.get_playlist_info(request.playlist_url)
    if not playlist_info:
        raise HTTPException(status_code=400, detail="Invalid playlist URL")
    return playlist_info

@app.post('/youtube-api/playlist/metadata')
async def youtube_proxy(query: FetchPlaylistParams):
    youtube_base_url = f"https://www.googleapis.com/youtube/v3/playlistItems?playlistId={query.playlist_id}"

    # Using unpacking to pass query parameters directly
    d = query.dict(exclude_none=True)
    d.pop('playlist_id')
    d['key'] = os.environ.get("YOUTUBE_API_KEY")
    response = requests.get(youtube_base_url, params=d)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )
