from mutagen import easyid3
from mutagen.mp3 import MP3
from mutagen import id3
from mutagen.id3 import APIC
import base64



class MetadataHandler:

	def __init__(self, file_name):
		self.file_name = file_name

	def add_cover(self, thumbnail: str):
		audio_file = MP3(self.file_name)
		audio_file.tags.add(id3.APIC(mime='image/jpeg', type=3, desc=u'Cover', data=bytes(base64.b64decode(thumbnail))))

	def __setitem__(self, key, value):
		self.audio_file[key] = value

	def __getitem__(self, key):
		return self.audio_file[key]

	def __enter__(self):
		self.audio_file = easyid3.EasyID3(self.file_name)
		return self

	def keys(self) -> list:
		return self.audio_file.keys()

	def __exit__(self, exc_type, exc_val, exc_tb):
		# make sure the file gets saved if no error occurred
		if not exc_type:
			self.audio_file.save()