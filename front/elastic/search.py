import json

def format_results(results):
    """
    Specialized data formatter built from the example json
    response data sent by the elastic search backend.
    """
    data = json.loads(results)
    return [hit['_source'] for hit in data['hits']['hits']]

# vim: ft=python et sw=4 sts=4
