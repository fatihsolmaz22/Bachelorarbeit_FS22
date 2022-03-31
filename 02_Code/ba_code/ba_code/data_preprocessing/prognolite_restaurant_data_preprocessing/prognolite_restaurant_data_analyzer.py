from prognolite_restaurant_data_extractor import PrognoliteRestaurantDataExtractor
from ba_code.data_preprocessing.prognolite_restaurant_data_preprocessing.restaurant_constants import Restaurant
import matplotlib.pyplot as plt


# TODO: not clean, code duplication (interface or superclass)
class PrognoliteRestaurantDataAnalyzer:

    def __init__(self):
        self.__restaurantDataExtractor = PrognoliteRestaurantDataExtractor()

    def plot_turnover_per_month_all_restaurants(self):
        for restaurant in Restaurant:
            self.plot_turnover_per_month(restaurant)

    def plot_turnover_per_month(self, restaurant):
        df_turnover_per_month = self.__restaurantDataExtractor \
            .get_turnover_per_month_dataframe(restaurant)

        if df_turnover_per_month.empty:
            return

        title = "Turnover per month"
        x_label = "month"
        y_label = "turnover in CHF"
        self.__plot_dataframe(df_turnover_per_month,
                              title, x_label, y_label, restaurant)

    def __plot_dataframe(self, df, title, x_label, y_label, restaurant):
        plt.figure()
        df.plot(marker='o')
        plt.title(title + ": " + restaurant.value)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc="upper left")
        plt.grid()
        plt.show()


restaurantDataAnalyzer = PrognoliteRestaurantDataAnalyzer()
restaurantDataAnalyzer.plot_turnover_per_month_all_restaurants()
