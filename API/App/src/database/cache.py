import base64
import os

from .elastic_connector import ElasticConnector
from ..DataClasses import Singleton, YoutubeMetadata


from ..Utils import get_logger, write_to_json

logger = get_logger(__file__)


class Cache(metaclass=Singleton):

	def __init__(self):
		self.es = ElasticConnector()
		self.index_prefix = 'youtubedownloads'
		self.metadata_index = f'{self.index_prefix}-metadata'
		self.video_index = f'{self.index_prefix}-video'
		self.setup_elastic()

	def get_cached_data(self, video_code: str) -> (YoutubeMetadata, dict):
		logger.info('get_cached_data')
		query = self.es.build_query(video_code=video_code)
		metadata = self.es.query_docs(self.metadata_index, query)
		if not metadata:
			return {}, {}
		logger.info(f'finished_query')
		metadata = metadata[0]
		video = self.es.query_docs(self.video_index, query)[0]
		return YoutubeMetadata.from_cache(metadata), video

	def is_cached(self, video_code: str) -> str:
		return bool(self.get_cached_data(video_code)[0])

	def add_to_cache(self, video_path: str, metadata: YoutubeMetadata) -> dict:
		video_code = metadata.get_video_code()
		logger.info(f'Adding video with code {video_code} to cache')
		cached_data, video_data = self.get_cached_data(video_code)
		if not cached_data:
			logger.info(f'Adding to cache')
			self.es.grava_elastic(self.metadata_index, metadata.to_elastic())
			self.es.grava_elastic(self.video_index, {'video_code': video_code, 'path': video_path})
		else:
			logger.info(f'Updating cache')
			self.es.atualiza_elastic(self.metadata_index, cached_data['doc_id'], metadata.to_elastic())
			self.es.atualiza_elastic(self.video_index, video_data['doc_id'], {'video_code': video_code, 'path': video_path})

	def setup_elastic(self):
		indexes = self.es.get_indices()
		if self.metadata_index in indexes:
			return
		logger.info(f'Creating elastic indexes')
		metadata_index = {
		  "settings": {
			"number_of_replicas": 0,
			"number_of_shards": 1
		  },
		  "mappings": {
			"properties": {
				"video_code": {
				  "type": "keyword"
				},
				"channel": {
				  "type": "text",
				  "fields": {
					"keyword": {
					  "type": "keyword"
					}
				  }
				},
				"title": {
				  "type": "text",
				  "fields": {
					"keyword": {
					  "type": "keyword"
					}
				  }
				},
				"thumbnail": {
				  "type": "binary"
				},
				"album": {
				  "type": "text",
				  "fields": {
					"keyword": {
					  "type": "keyword"
					}
				  }
				}
			  }
		  }
		}
		video_index = {
		  "settings": {
			"number_of_replicas": 0,
			"number_of_shards": 1
		  },
		  "mappings": {
			"properties": {
					"base64": {
					  "type": "binary"
					},
					"path": {
					  "type": "keyword"
					}
				}
		  	}
		}
		self.es.indices.create(index = self.metadata_index, body = metadata_index)
		self.es.indices.create(index = self.video_index, body = video_index)


	def get_all_cached(self):
		return self.es.query_docs(f'{self.index_prefix}-*', {}, return_index=True)

	def clear(self):
		all_docs = self.get_all_cached()
		bulk_operations = []
		errors = []
		video_docs = (i for i in all_docs if i['index'] == self.video_index)
		doc_pairs = [(vd, [i for i in all_docs if i['video_code'] == vd['video_code'] and i['index'] == self.metadata_index][0]) for vd in video_docs]
		for video_doc, metadata_doc in doc_pairs:
			try:
				os.remove(video_doc['path'])
				successfuly_deleted = True
			except FileNotFoundError:
				logger.debug(f'Failed to delete {video_doc["path"]}')
				successfuly_deleted = False
			successfuly_deleted = True
			if successfuly_deleted:
				bulk_operations.extend([
					{'_op_type': 'delete', '_index': self.metadata_index, '_id': metadata_doc['doc_id']},
					{'_op_type': 'delete', '_index': self.video_index, '_id': video_doc['doc_id']}
				])
			else:
				errors.append(video_doc['video_code'])

		write_to_json('out.json', bulk_operations)
		self.es.do_bulk(bulk_operations)