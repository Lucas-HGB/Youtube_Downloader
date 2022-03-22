import pydantic
import os
import datetime
import requests
import base64
import logging



class YoutubeDLOptions(pydantic.BaseModel):

	format: str = ''
	postprocessors: list[dict] = list()
	current_setup: str = None

	def prepare_mp3_download(self):
		self.format = 'bestaudio/best'
		self.postprocessors = [{
	        'key': 'FFmpegMetadata',
	        'add_chapters': True,
	        'add_metadata': True,
	    }]
		self.current_setup = 'mp3'

	def prepare_mp4_download(self):
		self.format = ''
		self.postprocessors = []
		self.current_setup = 'mp4'

	def to_ytb_dl_options(self, update_hook: callable) -> dict:
		d = {'postprocessors': self.postprocessors, 'ratelimit': self.ratelimit, 
		'outtmpl': self.output_format, 'progress_hooks': [update_hook], 'no_playlist': not self.allow_playlist}
		if self.format:
			d['format'] = self.format
		return d

	@property
	def is_mp3_ready(self):
		return self.current_setup == 'mp3'

	@property
	def is_mp4_ready(self):
		return self.current_setup == 'mp4'

	@property
	def ratelimit(self):
		return os.environ.get('RATE_LIMIT', 99999999999999999999)

	@property
	def output_format(self):
		return r'%(title)s - %(uploader)s.%(ext)s'
	
	@property
	def allow_playlist(self):
		return False


class YoutubeMetadata(pydantic.BaseModel):

	url: str
	channel: str
	title: str
	thumbnail_b64: str
	other: dict

	@pydantic.root_validator(pre=True)
	@classmethod
	def parse_metadata(cls, values):
		metadata = values['raw_metadata']
		thumbnail_b64 = base64.b64encode(requests.get(metadata['thumbnail']).content)
		metadata.pop('formats')
		metadata.pop('thumbnails')
		if 'automatic_captions' in metadata:
			metadata.pop('automatic_captions')

		return {
			'url': metadata.pop('original_url'),
			'channel': metadata.pop('channel'),
			'title': metadata.pop('fulltitle'),
			'thumbnail_b64': thumbnail_b64,
			'other': {key:value for key, value in sorted(metadata.items())}
		}

	def to_json(self):
		return dict(self)

	def __getitem__(self, key):
		return dict(self)[key]

	def __str__(self) -> str:
		now = datetime.datetime.now(datetime.timezone.utc)
		current_time = f'{now.day}-{now.month}-{now.year} {now.hour}.{now.minute}.{now.second}'
		return f'{self.title} - {self.channel} - {current_time}'