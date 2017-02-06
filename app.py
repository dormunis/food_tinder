import json

from flask import Flask, render_template, Response
from schema import SchemaError

import queries
from config import postgres_settings
from consts import USERS, APPLICATION_JSON
from schemas import interest_schema
from slack_handler import notify_slack
from storage import Storage
from flask import request

DEFAULT_IS_KOSHER = False
DEFAULT_MAX_DISTANCE = 5000
DEFAULT_FOOD_TYPE = ""

app = Flask("FoodTinder")


def get_args():
    distance = DEFAULT_MAX_DISTANCE
    is_kosher = DEFAULT_IS_KOSHER
    food_type = DEFAULT_FOOD_TYPE

    try:
        is_kosher = True if request.args.get('kosher') == 'true' else False
    except Exception:
        pass

    try:
        distance = int(request.args.get('distance'))
    except Exception:
        pass

    try:
        food_type = '%' + request.args.get('food_type') + '%'
    except Exception:
        pass

    return distance, is_kosher, food_type


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html'), 200


@app.route('/api/restaurants', methods=['GET'])
def restaurants():
    distance, is_kosher, food_type = get_args()
    restaurants = storage.get(queries.GET_FILTERED_RESTAURANTS, (distance, is_kosher, food_type))

    return Response(json.dumps(restaurants),
                    status=200, mimetype=APPLICATION_JSON)


@app.route('/api/interest', methods=['PUT'])
def put():
    try:
        data = request.get_json(silent=True)
        interest_schema.validate(data)
        keys, values = ','.join(data.keys()).encode('utf-8'), ','.join(map(lambda x: x.encode('utf-8'),
                                                                           map(lambda x: "'%s'" % x, data.values())))
        storage.insert(queries.INSERT_INTERESTED.format(keys=keys, values=values))
        return Response(json.dumps(dict(cool="bro")), status=200, mimetype=APPLICATION_JSON)
    except SchemaError, e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype=APPLICATION_JSON)


@app.route('/api/match/<user_id>', methods=['GET'])
def match(user_id):
    matches = storage.get(queries.GET_ALL_RELEVANT_MATCHES)
    relevant_rests = filter(lambda x: user_id in x[USERS], matches)
    irrelevant_rests = [x for x in matches if x not in relevant_rests]
    total_rests = relevant_rests + irrelevant_rests
    return Response(json.dumps(total_rests), status=200, mimetype=APPLICATION_JSON)


@app.route('/gogogo', methods=['GET'])
def gogogo():
    notify_slack(storage)
    return Response(json.dumps(json.dumps(dict(status="went went went"))), status=200, mimetype=APPLICATION_JSON)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    storage = Storage(postgres_settings)
    app.run(debug=True, host="0.0.0.0", port=5000)
