import json
try:
    import requests
except ImportError:
    print 'requests module is required (pip install requests)'
    raise

def format_results(results):
    """
    Specialized data formatter built from the example json
    response data sent by the elastic search backend.
    """
    if isinstance(results, str):
        results = json.loads(results)
    return [hit['_source'] for hit in results['hits']['hits']]

def format_matchall(query):
    return '{"query":{"bool":{"must":[{"query_string":{"default_field":"_all","query":"%s"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"facets":{}}' % query

def matchall(query):
    search_url = 'http://192.168.66.27:9200/tess/_search'
    r = requests.post(search_url, data=format_matchall(query))
    results = r.json()
    return format_results(results)

# vim: ft=python et sw=4 sts=4
