from restaurant_data_extractor import RestaurantDataExtractor
from ba_code.restaurant_data_preprocessing.restaurant_uri import RestaurantUri
import matplotlib.pyplot as plt


class RestaurantDataAnalyzer:

    def __init__(self):
        self.__restaurantDataExtractor = RestaurantDataExtractor()

    def plot_turnover_per_month_all_restaurants(self):
        for restaurant_uri in RestaurantUri:
            self.plot_turnover_per_month(restaurant_uri)

    def plot_turnover_per_month(self, restaurant_uri):
        df_turnover_per_month = self.__restaurantDataExtractor \
            .get_turnover_per_month_dataframe(restaurant_uri)

        plt.figure()
        df_turnover_per_month.plot()
        plt.title("Turnover per month: " + self.__get_restaurant_name(
                                                restaurant_uri))
        plt.xlabel('month')
        plt.ylabel('turnover CHF')
        plt.legend(loc="upper left")
        plt.grid()
        plt.show()

    def __get_restaurant_name(self, restaurant_uri):
        restaurant_uri_array = str(restaurant_uri).lower().split(".")[1].split("_")
        restaurant_uri_array = [element.capitalize() for element in restaurant_uri_array]
        return ' '.join(restaurant_uri_array)


restaurantDataAnalyzer = RestaurantDataAnalyzer()
restaurantDataAnalyzer.plot_turnover_per_month_all_restaurants()
