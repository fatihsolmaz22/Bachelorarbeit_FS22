from restaurant_data_extractor import RestaurantDataExtractor
from restaurant_data import RestaurantData
import matplotlib.pyplot as plt


class RestaurantDataAnalyzer:

    def __init__(self):
        self.__restaurantDataExtractor = RestaurantDataExtractor()

    def plot_turnover_per_month_all_restaurants(self):
        for restaurant_data in RestaurantData:
            self.plot_turnover_per_month(restaurant_data)

    def plot_turnover_per_month(self, restaurant_data):
        df_turnover_per_month = self.__restaurantDataExtractor \
            .get_turnover_per_month_dataframe(restaurant_data)

        plt.figure()
        df_turnover_per_month.plot()
        plt.title("Turnover per month: " + self.__get_restaurant_name(
                                                restaurant_data))
        plt.xlabel('day')
        plt.ylabel('turnover CHF')
        plt.legend(loc="upper left")
        plt.grid()
        plt.show()

    def __get_restaurant_name(self, restaurant_data):
        restaurant_data_array = str(restaurant_data).lower().split(".")[1].split("_")
        restaurant_data_array = [element.capitalize() for element in restaurant_data_array]
        return ' '.join(restaurant_data_array)


restaurantDataAnalyzer = RestaurantDataAnalyzer()
restaurantDataAnalyzer.plot_turnover_per_month_all_restaurants()
