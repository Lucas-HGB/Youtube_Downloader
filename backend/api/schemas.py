from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class VideoMetadata(BaseModel):
    title: str
    author: str
    album: Optional[str] = None

class VideoRequest(BaseModel):
    video_url: str
    metadata: VideoMetadata

class VideoResponse(BaseModel):
    id: str
    status: str = Field(..., description="pending, processing, completed, or failed")
    download_url: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PlaylistRequest(BaseModel):
    playlist_url: str
    metadata: Optional[List[VideoMetadata]] = None

class ConversionJob(BaseModel):
    id: UUID
    video_url: str
    metadata: VideoMetadata
    status: str
    download_url: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class FetchPlaylistParams(BaseModel):
    part: str
    max_results: int
    playlist_id: str