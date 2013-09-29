from flask import (Flask, jsonify, render_template, request)
from werkzeug.routing import BaseConverter
from os.path import basename
from urlparse import urlsplit
import elastic
import os
import urllib2

app = Flask(__name__)

base_folder = 'data/sites/'
yes_folder = os.path.join(base_folder, 'YesData/')
no_folder = os.path.join(base_folder, 'NoData/')

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

@app.route('/api/label', methods=['POST'])
def label():
    url = request.form['url']
    label = request.form['label']
    download(url, (yes_folder if label == 'true' else no_folder))
    return ""

@app.route('/api/auto_suggest', methods=['GET'])
def auto_suggest():
    query = request.args.get('query')
    result = elastic.auto_suggest(query)
    return str(result)
    return ''


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

def url2name(url):
    keepcharacters = (' ','_', '-')
    return "".join(c for c in url if c.isalnum() or c in keepcharacters).rstrip() + '.html'

def download(url, path, localFileName = None):
    localName = url2name(url)
    req = urllib2.Request(url)
    r = urllib2.urlopen(req)

    if r.url != url:
        # if we were redirected, the real file name we take from the final URL
        localName = url2name(r.url)
    if localFileName:
        # we can force to save the file as specified name
        localName = localFileName

    fileName = os.path.join(path, localName)
    ensure_dir(fileName)
    with open(fileName, 'wb') as f:
        f.write(r.read())

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)

# vim: ft=python et sw=4 sts=4
