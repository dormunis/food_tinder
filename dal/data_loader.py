import csv
from restaurants import Restaurant
from utils import json_loader


class RestaurantLoader(object):
    def __init__(self, config):
        self.__restaurant_files = config["restaurant_input_file"]

    def load_restaurants_from_csv(self):
        restaurants = []

        with open(self.__restaurant_file, 'rU') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                name = row["Name"]
                image = row["Image"]
                description = row["Description"]
                rate = float(row["Rate"]) if row["Rate"] else 0
                food_type = row["Type"].split(", ")
                distance = 1
                is_kosher = True if row["Kosher"] == "yes" else False

                restaurant = Restaurant(name, image, description, rate, food_type, distance, is_kosher)
                restaurants.append(restaurant)

        return restaurants

    def load_restaurants_from_json(self):
        restaurants = []

        for restaurant_file in self.__restaurant_files:
            restaurants_content_list = json_loader(restaurant_file)
            for restaurant_content in restaurants_content_list:
                name = restaurant_content["RestaurantName"]
                image = restaurant_content["RestaurantLogoUrl"]
                description = ""
                rate = restaurant_content["ReviewsRank"]
                food_type = restaurant_content["RestaurantCuisineList"].split(", ")
                distance = restaurant_content["distanceFromUserInMeters"]
                is_kosher = True if restaurant_content["IsKosher"] == "yes" else False

                restaurant_content = Restaurant(name, image, description, rate, food_type, distance, is_kosher)
                restaurants.append(restaurant_content)

        return restaurants


