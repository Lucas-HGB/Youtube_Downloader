import elasticsearch
import os
import pprint
from datetime import datetime, timezone
from ..DataClasses import Singleton
from ..Utils import get_logger


logger = get_logger(__file__)


class ElasticConnector(elasticsearch.Elasticsearch, metaclass=Singleton):

    def __init__(self):
        user = os.environ.get('ELASTIC_USER')
        password = os.environ.get('ELASTIC_PASSWORD')
        if user and password:
            super().__init__(
                os.environ.get("ELASTIC_SERVER"),
                http_auth=(user, password),
                verify_certs=False
            )
        else:
            super().__init__(
                os.environ.get("ELASTIC_SERVER"),
                verify_certs=False
            )

    def build_query(self, include_fields: list = [], sort_by: dict = {}, **kwargs) -> dict:
        query = {
            'query': {
                'bool': {
                    'filter': []
                }
            }
        }
        if include_fields:
            query['_source'] = {'includes': include_fields}

        if sort_by:
            query['sort'] = []
            for key, order in sort_by.items():
                query['sort'].append(
                    {key: {'order': order}}
                )
        for key, value in kwargs.items():
            if value is None:
                continue
            query['query']['bool']['filter'].append({'match_phrase': {key : value}})

        return query

    def query_docs(self, index: str, query: dict, return_index: bool = False) -> list:
        elastic_data = self.search(index=index, body=query)
        data = []
        for doc in elastic_data['hits']['hits']:
            dict_doc = doc['_source']
            doc_id = doc['_id']
            dict_doc['doc_id'] = doc_id
            if return_index:
                dict_doc['index'] = doc['_index']
            data.append(dict_doc)

        logger.info(f'QUERY_DOCS - {index!r} - {len(data)} doc{"s" if len(data) > 1 or len(data) == 0 else ""}')
        logger.debug(pprint.pformat(query))
        return data

    def grava_elastic(self, index: str, body: dict, user: str = 'LucasHGB') -> dict:
        ''' Atualiza campos de status e então grava registro no Elastic '''
        body['record_creation_date'] = datetime.now(timezone.utc).isoformat()
        body['record_created_by_user'] = user
        result = self.index(index = index, refresh = True, body = body)
        logger.info(f'GRAVA_ELASTIC - {index!r} - {result["_id"]}')
        logger.debug(pprint.pformat(body))
        return result

    def atualiza_elastic(self, index: str, doc_id: str, body: dict, user: str = 'LucasHGB') -> dict:
        ''' Atualiza campos de status e então atualiza registro no Elastic '''
        body['record_last_update'] = datetime.now(timezone.utc).isoformat()
        body['record_updated_by_user'] = user
        new_event_request_body = {"doc": body}

        logger.info(f'ATUALIZA_ELASTIC - {index!r} - {doc_id!r}')
        logger.debug(pprint.pformat(body))
        return self.update(index = index, id = doc_id, refresh = True, body = new_event_request_body)

    def get_indices(self) -> list:
        return list(self.indices.get(index='*'))

    def do_bulk(self, bulk_body: dict) -> dict:
        return elasticsearch.helpers.bulk(self, bulk_body)