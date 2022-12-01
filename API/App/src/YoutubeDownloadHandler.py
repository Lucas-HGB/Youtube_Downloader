#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import logging
import os
import moviepy.editor as mp
from yt_dlp import YoutubeDL

from .Configs import Configs
from .DataClasses import YoutubeMetadata, YoutubeDLOptions
from .MetadataHandler import MetadataHandler
from .Utils import write_to_json, remove_invalid_char, get_logger, Thread
from .Filter import Filter


logger = get_logger(__file__)


class YoutubeHandler:

    def __init__(self):
        self.cached_videos = []
        self._url = ''
        self.mp4_path = None
        self.download_status = 'Not Downloading'
        self.configs = Configs()
        self.recreate_ytb_dl()

    def recreate_ytb_dl(self):
        logger.info(f'recreate_ytb_dl')
        self.ytb = YoutubeDL(self.configs.youtubeDL_options.to_ytb_dl_options(update_hook=self.update_status))

    def generate_audio(self):
        logger.info(f'generate_audio')
        if not self.mp4_path:
            raise AttributeError('No video has been downloaded!')
        
        video_clip = mp.VideoFileClip(self.mp4_path)
        output_path = os.path.join(self.configs.mp3_output_path, remove_invalid_char(self.metadata.title) + '.mp3')

        video_clip.audio.write_audiofile(output_path)

        with MetadataHandler(output_path) as mp3:
            mp3['title'] = Filter.filter_title(self.metadata.title)
            mp3['artist'] = Filter.filter_artist(self.metadata.channel)
            mp3['website'] = self.url
            mp3['language'] = self.metadata.other.get('language')
            mp3.add_cover(self.metadata.thumbnail_b64)

    def download_video(self):
        logger.info(f'download_video')
        file_format = remove_invalid_char('{} - {}'.format(self.metadata['title'], self.metadata['channel'])) + '.mp4'
        logger.debug(f'file_format: {file_format}')
        if self.url not in self.cached_videos:
            logging.info(f'Downloading mp4 from {self.url}')
            self.cached_videos.append(self.url)
            self.configs.youtubeDL_options.prepare_mp4_download()
            self.recreate_ytb_dl()
            self.ytb.download([self.url])
            os.rename(self.download_status['filename'].replace('.f251', ''), os.path.join(self.configs.cache_dir, file_format))

        full_path = os.path.join(self.configs.cache_dir, file_format)
        self.mp4_path = full_path
        logger.debug(f'mp4_path: {full_path}')

        return full_path

    def update_video_metadata(self):
        logger.info(f'update_video_metadata')
        metadata = self.ytb.extract_info(url = self.url, download=False)
        self.metadata = YoutubeMetadata(raw_metadata=metadata)
        self.log_metadata()
        return self.metadata

    def log_metadata(self):
        logger.info(f'log_metadata')
        write_to_json(os.path.join(self.configs.cache_dir, remove_invalid_char(str(self.metadata)) + '.log'), dict(self.metadata)) # Logging purposes

    def update_status(self, status):
        self.download_status = status

    def clear_cache(self):
        logger.info(f'clear_cache')
        for file in [i for i in os.listdir(os.path.join(self.configs.cache_dir)) if not i.endswith('.log')]:
            os.remove(os.path.join(self.configs.cache_dir, file))

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, video_id: str):
        url = f'https://www.youtube.com/watch?v={video_id}'
        logger.info(f'Setting current url to {url}')
        self._url = url
        metadata = self.update_video_metadata()
        Thread(target=self.download_video).start()