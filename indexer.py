import os

from dal.data_indexer import RestaurantsIndexer
from dal.data_loader import RestaurantLoader
from utils import json_loader

CONFIG_FILE_PATH = os.path.join("settings", "config.json")


def main():
    config = json_loader(CONFIG_FILE_PATH)

    # Load filtered domains from input file
    loader = RestaurantLoader(config["data_loader_config"])
    restaurants = loader.load_restaurants_from_json()

    indexer = RestaurantsIndexer(config["data_indexer_config"])
    indexer.index(restaurants)
    print 3
    # Get and index blacklist
    # indexer.index(filtered_domains_removed_contains)


if __name__ == "__main__":
    main()
