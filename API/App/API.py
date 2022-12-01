#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import logging
from collections import defaultdict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread

from src.DataClasses import InterfaceMetadata
from src.YoutubeDownloadHandler import YoutubeHandler

logging.basicConfig(level=os.environ.get('LOGGING_LEVEL', 'INFO'))
logging.getLogger('Configs').setLevel(logging.ERROR)
logging.getLogger('DataClasses').setLevel(logging.ERROR)
logging.getLogger('Filter').setLevel(logging.ERROR)
logging.getLogger('MetadataHandler').setLevel(logging.INFO)
logging.getLogger('YoutubeDownloadHandler').setLevel(logging.INFO)

ytb = YoutubeHandler()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

videos = defaultdict(YoutubeHandler)


@app.post('/update/{url}')
async def update_video(url: str):
    videos[url].url = url
    return videos[url].metadata.to_json()


@app.post('/downloadMP3/{url}')
async def download_mp3(url: str):
    videos[url].generate_audio()
    return 'Started'


@app.get('/visualize/{url}/metadata')
async def get_video_metadata(url: str):
    return videos[url].metadata.json()

@app.get('/visualize/{url}/download')
async def download_status(url: str):
    return videos[url].download_status

@app.put('/update/{url}/metadata')
async def update_metadata(url: str, metadata: InterfaceMetadata):
    return videos[url].update_video_metadata(metadata)