import logging

from django.conf import settings

from elasticsearch import Elasticsearch, TransportError
from elasticsearch.helpers import bulk

logger = logging.getLogger(__name__)

es = Elasticsearch(settings.ES_HOSTS,
          sniff_on_start=False,
          sniff_on_connection_fail=False,
          sniffer_timeout=None)
es.indices.create(
    index=settings.ES_INDEX,
    body={"mappings" : {
            "datasets" : {
                "properties" : {
                    "name" : { "type": "string", "index" : "not_analyzed" },
                    "organisation_name" : { "type": "string", "index" : "not_analyzed" }
                }
            }
          },
          "settings" : {
              "index" : {
                "max_result_window" : 75000,
              }
          }
    },
    ignore=400
)


def index_dataset(dataset):
    try:
        res = es.index(
            index=settings.ES_INDEX,
            doc_type='datasets',
            id=str(dataset.id),
            body=dataset.as_dict(),
            refresh=True # Make sure it shows straight away
        )
    except TransportError as te:
        # TODO: Log the failure as serious so we find out about it
        logger.error("Failed to index dataset: {}".format(dataset.id))
        print(te)


def delete_dataset(dataset):
    try:
        es.delete(
            index=settings.ES_INDEX,
            doc_type='datasets',
            id=str(dataset.id),
            refresh=True  # Make sure it is removed straight away
        )
    except TransportError as te:
        if te.status_code == 404:
            return

        logger.exception("Failed to remove dataset '' from index".format(dataset.id))

def bulk_import(data):
    return bulk(es, data, stats_only=True, raise_on_error=True)

def flush_index():
    es.indices.flush(index=settings.ES_INDEX)

def reset_index():
    es.indices.delete(index=settings.ES_INDEX, ignore=400)
    es.indices.create(
        index=settings.ES_INDEX,
        body={
            "mappings": {
                "datasets" : {
                    "properties" : {
                        "name" : { "type": "string", "index" : "not_analyzed" }
                    }
            }},
            "settings" : {
              "index" : {
                "max_result_window" : 75000,
              }
          }
        },
        ignore=400
    )

