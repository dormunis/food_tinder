from postgres_connector import PostgresConnector


class Indexer(object):
    def __init__(self, config):
        self.__config = config
        self.__postgres_config = config["postgres_config"]
        self.__restaurant_table_name = config["restaurant_table_name"]
        self.__restaurant_table_columns = self.__config["restaurant_table_columns"]
        self.__users_file = config["users_file"]
        self.__users_table_columns = self.__config["users_table_columns"]
        self._users_table_name = self.__config["users_table_name"]

    def index_restaurants(self, restaurants):
        rows = [restaurant.get_attributes() for restaurant in restaurants]
        with PostgresConnector.get_connector(self.__postgres_config) as connector:
            connector.replace_table_content(self.__restaurant_table_name, self.__restaurant_table_columns, rows)

    def index_users(self):
        users = self._get_users()

        with PostgresConnector.get_connector(self.__postgres_config) as connector:
            connector.replace_table_content(self._users_table_name, self.__users_table_columns, users)

    def _get_users(self):
        users = []
        with open(self.__users_file) as f:
            for user in f.read().splitlines():
                users.append((user, '', ''))

        return users
