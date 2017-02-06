import json

from flask import Flask, render_template, Response
from schema import SchemaError

import queries
from config import postgres_settings
from consts import USERS, APPLICATION_JSON
from schemas import interest_schema
from storage import Storage


app = Flask("FoodTinder")


def __init__(self, storage_settings):
    self.storage = Storage(storage_settings)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html'), 200


@app.route('/restaurants', methods=['GET'])
def restaurants():
    return Response(json.dumps(storage.get(queries.GET_ALL_RESTAURANTS)), status=200, mimetype=APPLICATION_JSON)


@app.route('/interest', methods=['PUT'])
def put(request):
    try:
        data = request.get_json(silent=True)
        interest_schema.validate(data)
        keys, values = data.keys(), data.values()
        storage.insert(queries.INSERT_INTERESTED.format(keys=keys, values=values))
    except SchemaError, e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype=APPLICATION_JSON)


@app.route('/match/<user_id>', methods=['GET'])
def match(user_id):
    matches = storage.get(queries.GET_ALL_RELEVANT_MATCHES)
    relevant_rests = filter(lambda x: user_id in x[USERS], matches)
    irrelevant_rests = [x for x in matches if x not in relevant_rests]
    total_rests = relevant_rests + irrelevant_rests
    return Response(json.dumps(total_rests), status=200, mimetype=APPLICATION_JSON)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    storage = Storage(postgres_settings)
    app.run(debug=True, host="0.0.0.0", port=5000)
