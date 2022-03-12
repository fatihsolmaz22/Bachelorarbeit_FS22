import pandas as pd
from restaurant_data import RestaurantData


class RestaurantDataExtractor:

    def __init__(self):
        self.__restaurant_dfs = dict()
        self.__initialize_dataframes()

    def __initialize_dataframes(self):
        for restaurant_data in RestaurantData:
            df = pd.read_csv(restaurant_data.value)
            self.__restaurant_dfs[restaurant_data] = df

    def get_dataframe(self, restaurant_data):
        return self.__restaurant_dfs[restaurant_data]

"""
Call Example
restaurantDataExtractor = RestaurantDataExtractor()

df = restaurantDataExtractor.get_dataframe(RestaurantData.BUTCHER_BADENERSTRASSE)

print(df)
"""

