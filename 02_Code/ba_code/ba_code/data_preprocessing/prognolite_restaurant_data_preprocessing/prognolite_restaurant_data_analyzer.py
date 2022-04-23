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
        df_turnover_per_time_period = self.__restaurantDataExtractor \
            .get_turnover_per_time_period_dataframe(restaurant, time_period)

        if df_turnover_per_time_period.empty:
            return

        title = "Turnover per " + self.__get_value_of_time_period(time_period)
        x = 'd'
        y = 'turnover_per_time_period'
        x_label = self.__get_value_of_time_period(time_period)
        y_label = "turnover in CHF"
        self.__plot_dataframe(df_turnover_per_time_period, x, y,
                              title, x_label, y_label, restaurant)

    # TODO: remove this method later, this is not what Martin asked for
    def plot_turnover_development_since_beginning_for_all_restaurants(self, time_period='m'):
        for restaurant in Restaurant:
            self.plot_turnover_development_since_beginning(restaurant, time_period)

    # TODO: remove this method later, this is not what Martin asked for
    def plot_turnover_development_since_beginning(self, restaurant, time_period='m'):
        df_turnover_development_since_beginning = self.__restaurantDataExtractor \
            .get_turnover_development_since_beginning_dataframe(restaurant, time_period)

        if df_turnover_development_since_beginning.empty:
            return

        title = "Turnover development since beginning"
        x = 'd'
        y = 'turnover'
        x_label = self.__get_value_of_time_period(time_period)
        y_label = "turnover in CHF"
        self.__plot_dataframe(df_turnover_development_since_beginning, x, y,
                              title, x_label, y_label, restaurant)

    def __get_value_of_time_period(self, time_period):
        time_period_value = ''
        if time_period == 'd':
            time_period_value = 'day'
        elif time_period == 'm':
            time_period_value = 'month'
        elif time_period == 'Q':
            time_period_value = 'quarter year'
        elif time_period == 'Y':
            time_period_value = 'year'
        return time_period_value

    def __plot_dataframe(self, df, x, y, title, x_label, y_label, restaurant):
        plt.figure()
        df.plot(x=x, y=y, marker='o')
        plt.title(title + ":\n" + restaurant.value)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc="upper left")
        plt.grid()
        plt.show()


prognoliteRestaurantDataAnalyzer = PrognoliteRestaurantDataAnalyzer()
# prognoliteRestaurantDataAnalyzer.plot_turnover_per_time_period(Restaurant.BUTCHER_USTER, 'Q')
