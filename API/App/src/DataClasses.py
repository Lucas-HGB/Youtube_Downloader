import pydantic
import os
import datetime
import requests
import base64
import pprint
from .Utils import get_logger, get_video_code, format_watch_url

logger = get_logger(__file__)



class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]



class YoutubeDLOptions(pydantic.BaseModel):
	format: str = ''
	postprocessors: list[dict] = list()
	current_setup: str = None
	output_format: str = r'%(title)s - %(uploader)s.%(ext)s'
	allow_playlist: bool = False
	rate_limit: int = os.environ.get('RATE_LIMIT', 99999999999999999999)

	def prepare_mp3_download(self):
		logger.info('prepare_mp3_download')
		self.format = 'bestaudio/best'
		self.postprocessors = [{
			'key': 'FFmpegMetadata',
			'add_chapters': True,
			'add_metadata': True,
		}]
		self.current_setup = 'mp3'

	def prepare_mp4_download(self):
		logger.info('prepare_mp4_download')
		self.format = ''
		self.postprocessors = []
		self.current_setup = 'mp4'

	def to_ytb_dl_options(self, update_hook: callable) -> dict:
		logger.info(f'to_ytb_dl_options')
		d = {'postprocessors': self.postprocessors, 'ratelimit': self.rate_limit,
			 'outtmpl': self.output_format, 'progress_hooks': [update_hook], 'no_playlist': not self.allow_playlist}
		if self.format:
			d['format'] = self.format

		logger.debug(pprint.pformat(d))
		return d

	def is_mp3_ready(self) -> bool:
		return self.current_setup == 'mp3'

	def is_mp4_ready(self) -> bool:
		return self.current_setup == 'mp4'


class InterfaceMetadata(pydantic.BaseModel):

	title: str
	channel: str
	album: str

class YoutubeMetadata(pydantic.BaseModel):
	
	url: str
	channel: str
	title: str
	thumbnail_b64: str
	other: dict
	album: str = None
	doc_id: str = None

	def get_video_code(self) -> str:
		return get_video_code(self.url)

	@classmethod
	def from_cache(cls, metadata: str):
		metadata['other'] = {}
		metadata['thumbnail_b64'] = metadata.pop('thumbnail')
		metadata['url'] = format_watch_url(metadata.pop('video_code'))
		return cls(**metadata)

	@classmethod
	def from_raw_data(cls, metadata: dict):
		logger.info('parse_metadata')
		thumbnail_b64 = base64.b64encode(requests.get(metadata['thumbnail']).content)
		metadata.pop('formats')
		metadata.pop('thumbnails')
		if 'automatic_captions' in metadata:
			metadata.pop('automatic_captions')
		data = {
			'url': metadata.pop('original_url'),
			'channel': metadata.pop('channel'),
			'title': metadata.pop('fulltitle'),
			'thumbnail_b64': thumbnail_b64,
			'other': {key: value for key, value in sorted(metadata.items())}
		}
		logger.debug(data)
		return cls(**data)
		
	def to_json(self):
		return dict(self)

	def update(self, **kwargs):
		for key, value in kwargs.items():
			setattr(self, key, value)
		return self

	def to_elastic(self) -> dict:
		return {
			"video_code": self.get_video_code(),
			'channel': self.channel,
			'title': self.title,
			'thumbnail': self.thumbnail_b64,
			'album': self.album
		}

	def __getitem__(self, key):
		return dict(self)[key]

	def __str__(self) -> str:
		now = datetime.datetime.now(datetime.timezone.utc)
		current_time = f'{now.day}-{now.month}-{now.year} {now.hour}.{now.minute}.{now.second}'
		return f'{self.title} - {self.channel} - {current_time}'