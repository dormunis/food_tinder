import os

from dal.data_indexer import Indexer
from dal.data_loader import RestaurantLoader
from utils import json_loader

CONFIG_FILE_PATH = os.path.join("settings", "config.json")


def main():
    config = json_loader(CONFIG_FILE_PATH)

    # Load filtered domains from input file
    loader = RestaurantLoader(config["data_loader_config"])
    restaurants = loader.load_restaurants_from_json()

    indexer = Indexer(config["data_indexer_config"])
    # indexer.index_restaurants(restaurants)
    indexer.index_users()

if __name__ == "__main__":
    main()
