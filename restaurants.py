

class Restaurant(object):
    def __init__(self, name, image, description, rate, food_types,  distance, kosher):
        self.__name = name
        self.__image = image
        self.__description = description
        self.__rate = rate
        self.__food_types = food_types
        self.__distance = distance
        self.__kosher = kosher

    def get_attributes(self):
        return (self.__name, self.__image, self.__description, self.__rate, self.__food_types, self.__distance,
                self.__kosher)
