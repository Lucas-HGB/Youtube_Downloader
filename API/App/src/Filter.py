import re
from .Configs import Configs
from .Utils import get_logger

logger = get_logger(__file__)


class Filter:

	def filter_artist(artist):
		artist = artist.strip()
		for pattern, replacement in Configs().artist_regex.items():
			logger.info(f'Replacing artist {replacement} with pattern {pattern} and value {artist}')
			artist = re.sub(pattern, replacement, artist).strip()

		return artist.strip()

	def filter_title(title):
		title = title.strip()
		for pattern, replacement in Configs().title_regex.items():
			logger.info(f'Replacing title {replacement} with pattern {pattern} and value {title}')
			title = re.sub(pattern, replacement, title).strip()

		if Configs().transform_upper and title.isupper():
			title = title.lower().capitalize()

		return title.strip()
