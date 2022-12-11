#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import logging
import os
import shutil
import moviepy.editor as mp
from yt_dlp import YoutubeDL

from .Configs import Configs
from .DataClasses import YoutubeMetadata, YoutubeDLOptions, InterfaceMetadata
from .MetadataHandler import MetadataHandler
from .Utils import write_to_json, remove_invalid_char, get_logger, Thread, get_video_code, format_watch_url
from .Filter import Filter
from .database.cache import Cache


logger = get_logger(__file__)


class YoutubeHandler:

    def __init__(self):
        self.cached_videos = []
        self._url = ''
        self.mp4_path = None
        self.download_status = 'Not Downloading'
        self.configs = Configs()
        self.recreate_ytb_dl()
        self.cache = Cache()

    def recreate_ytb_dl(self):
        logger.info(f'recreate_ytb_dl')
        self.ytb = YoutubeDL(self.configs.youtubeDL_options.to_ytb_dl_options(update_hook=self.update_status))

    def move_file(self, origin: str, dest: str):
        logger.info(f'Move file from {origin!r} to {dest!r}')
        os.system(f"cp --no-preserve=mode {origin!r} {dest!r}")
        os.remove(origin)

    def generate_audio(self):
        logger.info(f'generate_audio')
        if not self.mp4_path and not self.cache.is_cached(self.metadata.get_video_code()):
            raise AttributeError('No video has been downloaded!')
        
        video_clip = mp.VideoFileClip(self.mp4_path)
        file = remove_invalid_char(self.metadata.title) + '.mp3'
        output_path = os.path.join(self.configs.cache_dir, file)

        video_clip.audio.write_audiofile(output_path)

        with MetadataHandler(output_path) as mp3:
            mp3.add_cover(self.metadata.thumbnail_b64)

        with MetadataHandler(output_path) as mp3:
            mp3['title'] = Filter.filter_title(self.metadata.title)
            mp3['artist'] = Filter.filter_artist(self.metadata.channel)
            if hasattr(self.metadata, 'album') and self.metadata.album is not None:
                mp3['album'] = self.metadata.album
            mp3['website'] = self.url
            if self.metadata.other.get('language'):
                mp3['language'] = self.metadata.other.get('language', '')

        self.move_file(output_path, os.path.join(self.configs.mp3_output_path, file))

    def extract_metadata(self):
        logger.info(f'extract_metadata')
        metadata = self.ytb.extract_info(url = self.url, download=False)
        return YoutubeMetadata.from_raw_data(metadata)

    def download_video(self):
        logger.info('download_video')
        file_format = remove_invalid_char('{} - {}'.format(self.metadata['title'], self.metadata['channel'])) + '.mp4'
        self.configs.youtubeDL_options.prepare_mp4_download()
        self.recreate_ytb_dl()
        self.ytb.download([self.url])
        output_path = os.path.join(self.configs.cache_dir, file_format)
        file = self.download_status['filename'].replace('.f251', '')
        self.move_file(file, output_path)
        self.mp4_path = output_path
        self.cache.add_to_cache(self.mp4_path, self.metadata)

    def update_status(self, status):
        self.download_status = status

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, video_id: str):
        url = format_watch_url(video_id)
        logger.info(f'Setting current url to {url}')
        self._url = url
        if self.cache.is_cached(video_id):
            self.metadata, video_data = self.cache.get_cached_data(video_id)
            self.mp4_path = video_data['path']
            return
        self.metadata = self.extract_metadata()
        th = Thread(target=self.download_video).start()
        # th.result() # Debugging purposes

    def update_video_metadata(self, metadata: InterfaceMetadata):
        self.metadata.update(**metadata.dict())
        self.cache.add_to_cache(self.mp4_path, self.metadata)
        return self.metadata