import base64
from mutagen import easyid3
from mutagen.mp3 import MP3
from mutagen import id3
from mutagen.id3 import APIC
from .Utils import get_logger

logger = get_logger(__file__)



class MetadataHandler:

	def __init__(self, file_name):
		self.file_name = file_name
		self.keys = lambda: self.audio_file.keys()

	def add_cover(self, thumbnail: str):
		logger.info(f'add_cover')
		audio_file = MP3(self.file_name)
		audio_file.tags.add(id3.APIC(mime='image/jpeg', type=3, desc=u'Cover', data=bytes(base64.b64decode(thumbnail))))
		audio_file.save()

		self.audio_file = easyid3.EasyID3(self.file_name)

	def __setitem__(self, key, value):
		logger.debug(f'setitem on {key!r} with value {value!r}')
		self.audio_file[key] = value

	def __getitem__(self, key):
		return self.audio_file[key]

	def __enter__(self):
		logger.debug(f'Opening file {self.file_name}')
		self.audio_file = easyid3.EasyID3(self.file_name)
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		# make sure the file gets saved if no error occurred
		if not exc_type:
			self.audio_file.save()