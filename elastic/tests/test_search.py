from elasticsearch import Elasticsearch
import pprint


def run():
    """
    Searches for a specific position and target in elasticsearch tachy measurements
    run test_file_upload.py first!!!

    :return: dict
    """
    es = Elasticsearch()

    qdsl = {
        "query": {
            "filtered": {
                "filter": {
                    "bool": {
                        "must": [
                            {"term": {"position": "pos11"}},
                            {"term": {"target": "dp01"}}
                        ]
                    }
                }
            }
        }
    }
    sq = es.search(index="dimosy", body=qdsl)
    pprint.pprint(sq)


if __name__ == "__main__":
    run()