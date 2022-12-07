import os, json, re
from .Utils import read_from_json, write_to_json, is_unix, get_app_path, get_logger
from .DataClasses import YoutubeDLOptions, Singleton

logger = get_logger(__file__)


class Configs(metaclass=Singleton):

	def __init__(self):
		self.config_dir = os.path.join('/', 'etc', 'youtube_downloader') if is_unix() else get_app_path()
		if os.path.isfile(conf := os.path.join(self.config_dir, "ytb_dl.conf")):
			self.load_config()
		else:
			self.set_default_config()

		self.set_cache_dir()
		self.set_mp3_output_path()
		self.set_mp4_output_path()
		self.youtubeDL_options = YoutubeDLOptions()
		self.youtubeDL_options.prepare_mp3_download()

	def set_cache_dir(self, path: str = None):
		self.cache_dir = path or os.path.join('/', 'app', 'cache')
		logger.info(f'Cache dir is {self.cache_dir}')
		if not os.path.exists(self.cache_dir):
			logger.info(f'Cache dir not created, creating.')
			os.makedirs(self.cache_dir)

	def set_mp3_output_path(self, path: str = None):
		self.mp3_output_path = path or os.path.join('/', 'app', 'media', 'mp3')
		if not os.path.exists(self.mp3_output_path):
			logger.info(f'Output path not created, creating')
			os.makedirs(self.mp3_output_path)

	def set_mp4_output_path(self, path: str = None):
		self.mp4_output_path = path or os.path.join('/', 'app', 'media', 'mp4')
		if not os.path.exists(self.mp4_output_path):
			logger.info(f'Output path not created, creating')
			os.makedirs(self.mp4_output_path)

	def set_default_config(self):
		logger.info(f'Setting default config')
		self.artist_regex = {}
		self.title_regex = {}
		self.transform_upper = True

	def load_config(self):
		logger.info(f'Loading config')
		conf = read_from_json(os.path.join(self.config_dir, "ytb_dl.conf"))
		self.artist_regex = {re.compile(reg, flags=re.IGNORECASE): replacement for reg, replacement in conf['artist_regex'].items()}
		self.title_regex = {re.compile(reg, flags=re.IGNORECASE): replacement for reg, replacement in conf['title_regex'].items()}
		self.transform_upper = conf['transform_upper']