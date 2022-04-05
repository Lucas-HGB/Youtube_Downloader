#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread


from src.YoutubeDownloadHandler import YoutubeHandler

logging.basicConfig(level=os.environ.get('LOGGING_LEVEL', 'INFO'))


ytb = YoutubeHandler()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/update/{url}')
async def update_video(url: str):
    ytb.url = url
    return ytb.metadata.to_json()


@app.post('/downloadMP3')
async def download_mp3():
    ytb.generate_audio()
    return 'Started'


@app.get('/visualize/metadata')
async def get_video_metadata():
    return ytb.metadata.json()


@app.get('/status/download')
async def download_status():
    return ytb.download_status

# uvicorn API:app --reload