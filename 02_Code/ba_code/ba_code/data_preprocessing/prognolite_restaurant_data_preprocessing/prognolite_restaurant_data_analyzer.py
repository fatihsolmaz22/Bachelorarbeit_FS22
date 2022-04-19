from prognolite_restaurant_data_extractor import PrognoliteRestaurantDataExtractor
from ba_code.data_preprocessing.prognolite_restaurant_data_preprocessing.prognolite_restaurant_constants import \
    Restaurant
import matplotlib.pyplot as plt


class PrognoliteRestaurantDataAnalyzer:

    def __init__(self):
        self.__restaurantDataExtractor = PrognoliteRestaurantDataExtractor()

    def plot_turnover_per_time_period_for_all_restaurants(self, time_period='m'):
        for restaurant in Restaurant:
            self.plot_turnover_per_time_period(restaurant, time_period)

    def plot_turnover_per_time_period(self, restaurant, time_period='m'):
        df_turnover_per_month = self.__restaurantDataExtractor \
            .get_turnover_per_time_period_dataframe(restaurant, time_period)

        if df_turnover_per_month.empty:
            return

        title = "Turnover per month"
        x = 'd'
        y = 'turnover_per_time_period'
        x_label = self.__get_x_label(time_period)
        y_label = "turnover in CHF"
        self.__plot_dataframe(df_turnover_per_month, x, y,
                              title, x_label, y_label, restaurant)

    def plot_turnover_development_since_beginning_for_all_restaurants(self, time_period='m'):
        for restaurant in Restaurant:
            self.plot_turnover_development_since_beginning(restaurant, time_period)

    def plot_turnover_development_since_beginning(self, restaurant, time_period='m'):
        df_turnover_development_since_beginning = self.__restaurantDataExtractor \
            .get_turnover_development_since_beginning_dataframe(restaurant, time_period)

        if df_turnover_development_since_beginning.empty:
            return

        title = "Turnover development since beginning"
        x = 'd'
        y = 'turnover'
        x_label = self.__get_x_label(time_period)
        y_label = "turnover in CHF"
        self.__plot_dataframe(df_turnover_development_since_beginning, x, y,
                              title, x_label, y_label, restaurant)

    def __get_x_label(self, time_period):
        x_label = ''
        if time_period == 'd':
            x_label = 'day'
        elif time_period == 'm':
            x_label = 'month'
        elif time_period == 'Q':
            x_label = 'quarter year'
        elif time_period == 'Y':
            x_label = 'year'
        return x_label

    def __plot_dataframe(self, df, x, y, title, x_label, y_label, restaurant):
        plt.figure()
        df.plot(x=x, y=y, marker='o')
        plt.title(title + ": " + restaurant.value)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc="upper left")
        plt.grid()
        plt.show()


prognoliteRestaurantDataAnalyzer = PrognoliteRestaurantDataAnalyzer()
# prognoliteRestaurantDataAnalyzer.plot_turnover_per_time_period(Restaurant.BUTCHER_USTER, 'Q')
