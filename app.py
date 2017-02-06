from flask import Flask, render_template
from schema import SchemaError

import queries
from schemas import interest_schema
from storage import Storage


class Application(object):
    app = Flask("FoodTinder")

    def __init__(self, storage_settings):
        self.storage = Storage(storage_settings)

    @app.route('/', methods=['GET'])
    def index(self):
        return render_template('index.html'), 200

    @app.route('/restaurants', methods=['GET'])
    def restaurants(self):
        return self.storage.get(queries.GET_ALL_RESTAURANTS), 200

    @app.route('/interest', methods=['PUT'])
    def put(self, request):
        try:
            data = request.data.decode()
            interest_schema.validate(data)
            keys, values = data.keys(), data.values()
            self.storage.insert(queries.INSERT_INTERESTED.format(keys=keys, values=values))
        except SchemaError, e:
            return str(e), 400

    @app.route('/match', methods=['GET'])
    def match(self):
        return self.storage.get(queries.GET_ALL_RELEVANT_MATCHES), 200


if __name__ == '__main__':
    app = Application
    app.app.run()
