#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import logging
from flask import Flask, jsonify, request
from threading import Thread

from src.YoutubeDownloadHandler import YoutubeHandler

logging.basicConfig(level=os.environ.get('LOGGING_LEVEL', 'INFO'))


ytb = YoutubeHandler()

app = Flask(__name__)


@app.route('/update', methods=['POST'])
def update_video():
    ytb.url = request.values['url']
    thread = Thread(target=ytb.download_video)
    thread.daemon = True
    thread.start()
    return jsonify(ytb.metadata.to_json())

@app.route('/downloadMP3', methods=['POST'])
def download_mp3():
    ytb.generate_audio()
    return 'Started'



@app.route('/visualize/metadata', methods=['GET'])
def get_video_metadata():
    ytb.url = request.values['url']
    return jsonify(ytb.metadata.to_json())

@app.route('/visualize/video', methods=['GET'])
def get_video_file_path():
    return jsonify(ytb.metadata.to_json())



@app.route('/status/download', methods=['GET'])
def download_status():
    return jsonify(ytb.download_status)


if __name__ == "__main__":
    ytb.url = "https://www.youtube.com/watch?v=qMhWatqmB-o"
    try:
        app.run(host="0.0.0.0", debug=True, port=8000)
    finally:
        pass
        # ytb.clear_cache()