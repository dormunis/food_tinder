from postgres_connector import PostgresConnector


class RestaurantsIndexer(object):
    def __init__(self, config):
        self.__config = config
        self.__postgres_config = config["postgres_config"]
        self.__restaurant_table_name = config["restaurant_table_name"]
        self.__restaurant_table_columns = self.__config["restaurant_table_columns"]

    def index(self, restaurants):
        rows = [restaurant.get_attributes() for restaurant in restaurants]

        with PostgresConnector.get_connector(self.__postgres_config) as connector:
            connector.replace_table_content(self.__restaurant_table_name, self.__restaurant_table_columns, rows)
