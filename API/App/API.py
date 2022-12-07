#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import logging
from collections import defaultdict
from src import create_app, InterfaceMetadata, YoutubeHandler, Cache

LOG_LEVEL = os.environ.get('LOGGING_LEVEL', 'DEBUG')
logging.info(f'Log level is {LOG_LEVEL}')

logging.basicConfig(level=LOG_LEVEL)
logging.getLogger('elastic_transport.transport').setLevel(logging.ERROR)
logging.getLogger('urllib3').setLevel(logging.ERROR)

logging.getLogger('Configs').setLevel(LOG_LEVEL)
logging.getLogger('DataClasses').setLevel(LOG_LEVEL)
logging.getLogger('Filter').setLevel(LOG_LEVEL)
logging.getLogger('MetadataHandler').setLevel(LOG_LEVEL)
logging.getLogger('YoutubeDownloadHandler').setLevel(LOG_LEVEL)
logging.getLogger('cache').setLevel(LOG_LEVEL)
logging.getLogger('elastic_connector').setLevel(LOG_LEVEL)


app = create_app()

videos = defaultdict(YoutubeHandler)


@app.post('/update/{video_id}')
async def update_video(video_id: str):
    videos[video_id].url = video_id
    return videos[video_id].metadata

@app.post('/downloadMP3/{video_id}')
async def download_mp3(video_id: str):
    if video_id not in videos:
        videos[video_id].url = video_id
    videos[video_id].generate_audio()
    return 'Started'

@app.get('/visualize/{video_id}/metadata')
async def get_video_metadata(video_id: str):
    if video_id not in videos:
        return Cache().get_cached_data(video_id)
    return videos[video_id].metadata.json()

@app.get('/visualize/{video_id}/download')
async def download_status(video_id: str):
    return videos[video_id].download_status

@app.put('/update/{video_id}/metadata')
async def update_metadata(video_id: str, metadata: InterfaceMetadata):
    return videos[video_id].update_video_metadata(metadata)

@app.delete('/cache')
async def clear_cache():
    Cache().clear()
    videos.clear()