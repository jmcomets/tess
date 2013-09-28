from flask import (Flask, jsonify, render_template, request)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def add_numbers():
    query = request.args.get('q')
    return jsonify()

# vim: ft=python et sw=4 sts=4
