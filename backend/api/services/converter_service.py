import asyncio
import os
import logging
from uuid import uuid4
from datetime import datetime
import eyed3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import requests
from typing import Dict, Optional
from ..schemas import VideoMetadata, ConversionJob, VideoResponse, VideoRequest
from .youtube_service import YouTubeService

class ConverterService:

    jobs: Dict[str, ConversionJob] = {}
    output_dir: str = 'downloads'

    @staticmethod
    async def _download_thumbnail(thumbnail_url: str, output_path: str) -> bool:
        try:
            response = requests.get(thumbnail_url)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return True
            return False
        except Exception as e:
            print(f"Error downloading thumbnail: {e}")
            return False

    @staticmethod
    async def create_job(request: VideoRequest) -> str:
        """Create a new conversion job"""
        job_id = str(uuid4())
        ConverterService.jobs[job_id] = ConversionJob(
            id=job_id,
            video_url=request.video_url,
            metadata=request.metadata,
            status="pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        return job_id

    @staticmethod
    async def get_job(job_id: str) -> Optional[VideoResponse]:
        """Get job status"""
        job = ConverterService.jobs.get(job_id)
        if not job:
            return None
        
        return VideoResponse(
            id=str(job.id),
            status=job.status,
            download_url=job.download_url,
            error=job.error
        )

    @staticmethod
    async def _update_metadata(file_path: str, metadata: VideoMetadata, thumbnail_url: Optional[str] = None):
        """Update MP3 metadata including thumbnail"""
        # Update basic metadata with eyed3
        print(f'Updating metadata for file {file_path!r}')
        audiofile = eyed3.load(file_path)
        if audiofile is None:
            raise Exception("Failed to load audio file")

        audiofile.tag.title = metadata.title
        audiofile.tag.artist = metadata.author
        if metadata.album:
            audiofile.tag.album = metadata.album
        
        await asyncio.to_thread(audiofile.tag.save)

        # Add thumbnail using mutagen if available
        if thumbnail_url:
            # Download thumbnail
            thumb_path = f"{file_path}.thumb.jpg"
            if await ConverterService._download_thumbnail(thumbnail_url, thumb_path):
                try:
                    audio = ID3(file_path)
                except:
                    audio = ID3()

                with open(thumb_path, 'rb') as album_art:
                    audio.add(
                        APIC(
                            encoding=3,
                            mime='image/jpeg',
                            type=3,  # Cover image
                            desc='Cover',
                            data=album_art.read()
                        )
                    )
                audio.save(file_path)
                
                # Clean up thumbnail file
                os.remove(thumb_path)


    @staticmethod
    async def process_video(job_id: str, url: str, metadata: VideoMetadata):
        """Process video conversion"""
        job = ConverterService.jobs[job_id]
        job.status = "processing"
        job.updated_at = datetime.utcnow()

        # Get video info including thumbnail
        youtube_service = YouTubeService()
        video_info = await youtube_service.get_video_info(url)
        if not video_info:
            raise Exception("Failed to get video info")

        thumbnail_url = video_info.get('thumbnail')

        # Download video
        output_path = os.path.join(ConverterService.output_dir, f"{metadata.title}.%(ext)s")
        success = await youtube_service.download_video(url, output_path)
        
        if not success:
            raise Exception("Failed to download video")

        # Update metadata
        mp3_path = os.path.join(ConverterService.output_dir, f"{metadata.title}.mp3")
        await ConverterService._update_metadata(mp3_path, metadata, thumbnail_url)

        # Update job status
        job.status = "completed"
        job.download_url = f"/downloads/{metadata.title}.mp3"
            
        
        job.updated_at = datetime.utcnow()