import json
import requests

SEARCH_URL = 'http://92.39.246.129:9200/object/_search'

def format_results(results):
    """
    Specialized data formatter built from the example json
    response data sent by the elastic search backend.
    """
    if isinstance(results, str):
        results = json.loads(results)
    if 'hits' not in results:
        return []
    return [hit['_source'] for hit in results['hits']['hits']]

def format_matchall(query):
    """ Specialized query formatter """
    bool_query = dict()
    bool_query['must'] = []
    bool_query['must_not'] = []
    bool_query['should'] = [dict(query_string=dict(default_field="_all", query=query)),
                            dict(query_string=dict(default_field="name", query=query, boost=7)),
                            dict(query_string=dict(default_field="url", query=query, boost=3))]
    
    for token in query.split(' '):
        bool_query['should'].append(dict(prefix=dict(_all=dict(prefix=token,  boost=0.6))))

    elas_query = dict(query=dict(bool=bool_query), size=60, sort=[], facets={})
    elas_query['from'] = 0

    print json.dumps(elas_query)
    return json.dumps(elas_query)

    # return '{"query":{\
    #          "bool":{"must":[{"query_string":{"default_field":"_all","query":"%s"}}],\
    #                  "must_not":[],\
    #                  "should":[]}},\
    #                  "from":0,\
    #                  "size":50,\
    #                  "sort":[],\
    #                  "facets":{}}' % query

def search(query):
    r = requests.post(SEARCH_URL, data=format_matchall(query))
    results = r.json()
    return format_results(results)

# vim: ft=python et sw=4 sts=4
