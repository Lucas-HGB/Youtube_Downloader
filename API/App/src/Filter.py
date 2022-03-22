import re
from .Configs import Configs


class Filter:

	def filter_artist(artist):
		artist = artist.strip()
		for pattern, replacement in Configs().artist_regex.items():
			artist = re.sub(pattern, replacement, artist).strip()

		return artist.strip()

	def filter_title(title):
		title = title.strip()
		for pattern, replacement in Configs().title_regex.items():
			title = re.sub(pattern, replacement, title).strip()

		if Configs().transform_upper and title.isupper():
			title = title.lower().capitalize()

		return title.strip()
