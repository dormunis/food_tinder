import json
import math
from collections import namedtuple

Coordinate = namedtuple('Coordinate', 'lat lng')

EARTH_RADIUS = 6378137


def calculate_coordinates(p1, p2):
    """
    :type p1: Coordinate
    :type p2: Coordinate
    :return: number in meters
    """
    d_lat = math.radians(p2.lat - p1.lat)
    d_long = math.radians(p2.lng - p1.lng)
    a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(math.radians(p1.lat)) * math.cos(math.radians(p2.lat)) \
                                                    * math.sin(d_long / 2) * math.sin(d_long / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = EARTH_RADIUS * c
    return d


def json_loader(json_file):
    with open(json_file) as f:
        return json.load(f)
