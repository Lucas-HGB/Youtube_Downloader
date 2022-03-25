#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import logging
from fastapi import FastAPI
from threading import Thread


from src.YoutubeDownloadHandler import YoutubeHandler

logging.basicConfig(level=os.environ.get('LOGGING_LEVEL', 'INFO'))


ytb = YoutubeHandler()

app = FastAPI()


@app.post('/update/{url}')
def update_video(url: str):
    ytb.url = url
    return ytb.metadata.to_json()


@app.post('/downloadMP3')
def download_mp3():
    ytb.generate_audio()
    return 'Started'


@app.get('/visualize/metadata')
def get_video_metadata():
    return ytb.metadata.json()


@app.get('/status/download')
def download_status():
    return ytb.download_status

# uvicorn main:app --reload