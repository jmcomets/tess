import json

def format_results(results):
    data = json.loads(results)
    return [hit['_source'] for hit in data['hits']['hits']]

# vim: ft=python et sw=4 sts=4
