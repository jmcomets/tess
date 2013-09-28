from flask import (Flask, jsonify, render_template, request)
import elastic

app = Flask(__name__)

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

@app.route('/search', methods=['GET'])
def search():
    """
    Search view, querying the elastic search backend
    based on the 'query' GET parameter.
    """
    query = request.args.get('query')
    response = jsonify(results=elastic.search(query))
    return response

if __name__ == '__main__':
    app.run(debug=True)

# vim: ft=python et sw=4 sts=4
