from elasticsearch import Elasticsearch
import pprint


def run():
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