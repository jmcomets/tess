from flask import (Flask, jsonify, render_template, request)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form('query')
    # TODO parse request *better*
    return jsonify({
        'query': query,
        'results': [],
        })

if __name__ == '__main__':
    app.run()

# vim: ft=python et sw=4 sts=4
