import os, json, re
from .Utils import read_from_json, write_to_json, is_unix, get_app_path, get_logger
from .DataClasses import YoutubeDLOptions

logger = get_logger(__file__)


class Configs:

	_instance = None
	def __new__(class_, *args, **kwargs):
		''' 
		Caso classe já tenha sido instanciada, retorna tal instância ao invés de criar outra 
		Isso mantém as configurações uniformes entre todo o programa.
		'''
		if not isinstance(class_._instance, class_):
			class_._instance = object.__new__(class_, *args, **kwargs)
		return class_._instance

	def __setattr__(self, atr, value):
		if atr == "_instance" and self._instance:
			raise AttributeError("Manually setting _instance is not allowed!")
		self.__dict__[atr] = value

	def __init__(self):
		self.config_dir = os.path.join('/', 'etc', 'youtube_downloader') if is_unix() else get_app_path()
		if os.path.isfile(conf := os.path.join(self.config_dir, "ytb_dl.conf")):
			self.load_config()
		else:
			self.set_default_config()
		self.youtubeDL_options = YoutubeDLOptions()
		self.youtubeDL_options.prepare_mp3_download()

	def set_cache_dir(self, path: str = None):
		self.cache_dir = path or os.path.join('/', 'var', 'log', 'youtube_downloader') if is_unix() else os.path.join(get_app_path(), 'cache')
		logger.info(f'Cache dir is {self.cache_dir}')
		if not os.path.exists(self.cache_dir):
			logger.info(f'Cache dir not created, creating.')
			os.mkdir(self.cache_dir)

	def set_mp3_output_path(self, path: str = None):
		self.mp3_output_path = path or os.path.join('/', 'var', 'lib', 'youtube_downloader') if is_unix() else os.path.join(get_app_path(), 'Downloads')
		if not os.path.exists(self.mp3_output_path):
			logger.info(f'Output path not created, creating')
			os.mkdir(self.mp3_output_path)

	def set_mp4_output_path(self, path: str = None):
		self.mp4_output_path = path or os.path.join('/', 'var', 'lib', 'youtube_downloader') if is_unix() else os.path.join(get_app_path(), 'Downloads')
		if not os.path.exists(self.mp4_output_path):
			logger.info(f'Output path not created, creating')
			os.mkdir(self.mp4_output_path)

	def set_default_config(self):
		logger.info(f'Setting default config')
		self.artist_regex = {}
		self.title_regex = {}
		self.transform_upper = True
		self.set_cache_dir()
		self.set_output_path()

	def load_config(self):
		logger.info(f'Loading config')
		conf = read_from_json(os.path.join(self.config_dir, "ytb_dl.conf"))
		self.artist_regex = {re.compile(reg, flags=re.IGNORECASE): replacement for reg, replacement in conf['artist_regex'].items()}
		self.title_regex = {re.compile(reg, flags=re.IGNORECASE): replacement for reg, replacement in conf['title_regex'].items()}
		self.transform_upper = conf['transform_upper']
		self.set_cache_dir(conf.get('cache_dir'))
		self.set_mp3_output_path(conf.get('mp3_output_path'))
		self.set_mp4_output_path(conf.get('mp4_output_path'))