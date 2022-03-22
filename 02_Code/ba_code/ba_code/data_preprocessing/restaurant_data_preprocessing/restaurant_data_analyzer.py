from restaurant_data_extractor import RestaurantDataExtractor
from ba_code.data_preprocessing.restaurant_data_preprocessing.restaurant_uri import RestaurantUri
import matplotlib.pyplot as plt


# TODO: not clean, code duplication (interface or superclass)
class RestaurantDataAnalyzer:

    def __init__(self):
        self.__restaurantDataExtractor = RestaurantDataExtractor()

    def plot_turnover_per_month_all_restaurants(self):
        for restaurant_uri in RestaurantUri:
            self.plot_turnover_per_month(restaurant_uri)

    def plot_turnover_per_month(self, restaurant_uri):
        df_turnover_per_month = self.__restaurantDataExtractor \
            .get_turnover_per_month_dataframe(restaurant_uri)

        title = "Turnover per month"
        x_label = "month"
        y_label = "turnover in CHF"
        self.__plot_dataframe(df_turnover_per_month,
                              title, x_label, y_label, restaurant_uri)

    def __plot_dataframe(self, df, title, x_label, y_label, restaurant_uri):
        plt.figure()
        df.interpolate().plot()
        plt.title(title + ": " + self.__restaurantDataExtractor.get_restaurant_name(restaurant_uri))
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc="upper left")
        plt.grid()
        plt.show()


restaurantDataAnalyzer = RestaurantDataAnalyzer()
restaurantDataAnalyzer.plot_turnover_per_month_all_restaurants()
