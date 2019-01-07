import flask
from flask import Flask, request, jsonify
import sqlalchemy
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET'])
def home():
    return "Hello from Homepage"

@app.route('/candidates/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('records.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_records = cur.execute('SELECT * FROM candidate_records;').fetchall()
    return jsonify(all_records)

@app.route('/candidates/request', methods=['GET'])
def api_filter():
    conn = sqlite3.connect('records.db')
    constituency = request.args.get('constituency')

    query = "SELECT * FROM candidate_records WHERE"
    to_filter = []

    if constituency:
        query += ' constituency=? AND'
        to_filter.append(constituency)

    query = query[:-4] + ';'

    conn = sqlite3.connect('records.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()
