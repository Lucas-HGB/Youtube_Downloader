from yt_dlp import YoutubeDL
from typing import Optional, Dict, Any
import asyncio
from ..schemas import VideoMetadata

class YouTubeService:

    ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    @staticmethod
    async def get_video_info(url: str) -> Optional[Dict[str, Any]]:
        """Extract video information from YouTube URL"""
        try:
            with YoutubeDL(YouTubeService.ydl_opts) as ydl:
                return await asyncio.to_thread(ydl.extract_info, url, download=False)
        except Exception as e:
            print(f"Error extracting video info: {e}")
            return None

    @staticmethod
    async def download_video(url: str, output_path: str) -> bool:
        """Download video and convert to MP3"""
        try:
            opts = dict(YouTubeService.ydl_opts)
            opts['outtmpl'] = output_path
            
            with YoutubeDL(opts) as ydl:
                await asyncio.to_thread(ydl.download, [url])
            return True
        except Exception as e:
            print(f"Error downloading video: {e}")
            return False

    @staticmethod
    async def get_playlist_info(url: str) -> Optional[Dict[str, Any]]:
        """Get playlist information"""
        try:
            opts = dict(YouTubeService.ydl_opts)
            opts['extract_flat'] = True
            
            with YoutubeDL(opts) as ydl:
                return await asyncio.to_thread(ydl.extract_info, url, download=False)
        except Exception as e:
            print(f"Error extracting playlist info: {e}")
            return None