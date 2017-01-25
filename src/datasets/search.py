import logging

from django.conf import settings

from elasticsearch import Elasticsearch, TransportError
from elasticsearch.helpers import bulk

logger = logging.getLogger(__name__)

es = Elasticsearch(settings.ES_HOSTS,
          sniff_on_start=False,
          sniff_on_connection_fail=False,
          sniffer_timeout=60)
es.indices.create(index=settings.ES_INDEX, ignore=400)


def index_dataset(dataset):
    try:
        res = es.index(
            index=settings.ES_INDEX,
            doc_type='dataset',
            id=dataset.id,
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
            doc_type='dataset',
            id=dataset.id,
            refresh=True  # Make sure it is removed straight away
        )
    except TransportError as te:
        if te.status_code == 404:
            return

        logger.exception("Failed to remove dataset '' from index".format(dataset.id))

def bulk_import(data):
    bulk(es, data)

def reset_index():
    es.indices.delete(index=settings.ES_INDEX, ignore=400)
    es.indices.create(index=settings.ES_INDEX, ignore=400)


# TODO: Provide a query function like ....
#res = es.search(index="test-index", body={"query": {"match_all": {}}})
#print("Got %d Hits:" % res['hits']['total'])
#for hit in res['hits']['hits']:
#    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
