import os, json, re
from .Utils import read_from_json, write_to_json
from .DataClasses import YoutubeDLOptions



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
		self.set_cache_dir()
		self.config_dir = os.path.join('/', 'etc', 'youtube_downloader')
		self.mp3_output_path = self.mp4_output_path = os.path.join('/', 'var', 'lib', 'youtube_downloader')
		if os.path.isfile(os.path.join(self.config_dir, "ytb_dl.conf")):
			self.load_config()
		else:
			self.set_default_config()
		self.youtubeDL_options = YoutubeDLOptions()
		self.youtubeDL_options.prepare_mp3_download()

	def set_cache_dir(self):
		self.cache_dir = os.path.join('/', 'var', 'log', 'youtube_downloader')

	def set_default_config(self):
		self.artist_regex = {}
		self.title_regex = {}
		self.transform_upper = True


	def load_config(self):
		conf = read_from_json(os.path.join(self.config_dir, "ytb_dl.conf"))
		self.artist_regex = {re.compile(reg, flags=re.IGNORECASE): replacement for reg, replacement in conf['artist_regex'].items()}
		self.title_regex = {re.compile(reg, flags=re.IGNORECASE): replacement for reg, replacement in conf['title_regex'].items()}

		self.transform_upper = conf['transform_upper']