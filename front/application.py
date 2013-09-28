from flask import (Flask, jsonify, render_template, request)
import elastic
from werkzeug.routing import BaseConverter

app = Flask(__name__)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

@app.route('/')
def index():
    """
    Root view (no data, simple template)
    """
    return render_template('index.html')

def parse_query(query):
    """
    Return the cleaned version of the query, based on the
    passed space-separated query.
    """
    return query # TODO

@app.route('/<regex("[\w\s\-_]+"):query>/')
def query_on_index(query):
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search():
    """
    Search view, querying the elastic search backend
    based on the 'query' GET parameter.
    """
    query = request.args.get('query')
    response = jsonify(results=elastic.search(query))
    return response

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

# vim: ft=python et sw=4 sts=4
