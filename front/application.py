import os
from flask import (Flask, jsonify, render_template, request)
from elastic import search as es

app = Flask(__name__)

@app.route('/')
def index():
    """
    Root view (no data, simple template)
    """
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    """
    Search view, querying the elastic search backend
    based on the 'query' GET parameter.
    """
    query = request.args.get('query') # TODO parse request
    response = jsonify(results=es.matchall(query))
    return response

if __name__ == '__main__':
    app.run(debug=True)

# vim: ft=python et sw=4 sts=4
