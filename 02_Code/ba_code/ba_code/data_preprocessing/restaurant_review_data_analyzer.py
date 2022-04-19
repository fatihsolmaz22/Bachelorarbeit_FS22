import matplotlib.pyplot as plt
from ba_code.data_preprocessing.prognolite_restaurant_data_preprocessing.prognolite_restaurant_data_extractor import \
    PrognoliteRestaurantDataExtractor
from ba_code.data_preprocessing.tripadvisor_restaurant_data_preprocessing.tripadvisor_restaurant_data_extractor import \
    TripadvisorRestaurantDataExtractor
from ba_code.data_preprocessing.prognolite_restaurant_data_preprocessing.prognolite_restaurant_constants import \
    Restaurant
from ba_code.data_preprocessing.tripadvisor_restaurant_data_preprocessing.tripadvisor_restaurant_data_uri import \
    TripadvisorRestaurantDataUri


class PrognoliteTripadvisorRestaurantDataAnalyzer:

    def __init__(self):
        self.__prognoliteRestaurantDataExtractor = PrognoliteRestaurantDataExtractor()
        self.__tripadvisor_restaurant_data_extractors = dict()
        self.__initialize_tripadvisor_restaurant_data_extractors()
        self.__restaurants = dict(zip(Restaurant, TripadvisorRestaurantDataUri))

    def __initialize_tripadvisor_restaurant_data_extractors(self):
        for tripadvisor_restaurant_data_uri in TripadvisorRestaurantDataUri:
            tripadvisor_restaurant_data_extractor = TripadvisorRestaurantDataExtractor()
            tripadvisor_restaurant_data_extractor.load_restaurant_data(open(tripadvisor_restaurant_data_uri.value))
            self.__tripadvisor_restaurant_data_extractors[tripadvisor_restaurant_data_uri] = \
                tripadvisor_restaurant_data_extractor

    def plot_development_of_overall_rating_and_turnover_since_beginning_for_all_restaurants(self, time_period='m'):
        for restaurant in self.__restaurants:
            self.plot_development_of_overall_rating_and_turnover_since_beginning(restaurant, time_period)

    def plot_development_of_overall_rating_and_turnover_since_beginning(self, restaurant, time_period='m'):
        df_turnover_development_since_beginning = self.__prognoliteRestaurantDataExtractor \
            .get_turnover_development_since_beginning_dataframe(restaurant, time_period)

        tripadvisor_restaurant_data_uri = self.__restaurants[restaurant]
        df_overall_rating_development_since_beginning = \
            self.__tripadvisor_restaurant_data_extractors[tripadvisor_restaurant_data_uri] \
                .get_overall_rating_development_since_beginning_dataframe(time_period)

        title = "Turnover and overall rating development over days"
        x1 = 'd'
        y1 = 'turnover'
        x2 = 'date'
        y2 = 'overall_rating_development'

        # find x_min and x_max limits
        if time_period != 'Q':
            x_min_date_turnover = df_turnover_development_since_beginning[x1].to_numpy().min().tz_localize(None)
            x_max_date_turnover = df_turnover_development_since_beginning[x1].to_numpy().max().tz_localize(None)
        else:
            x_min_date_turnover = df_turnover_development_since_beginning[x1].to_numpy().min()
            x_max_date_turnover = df_turnover_development_since_beginning[x1].to_numpy().max()

        x_min_date_overall_rating = df_overall_rating_development_since_beginning[x2].to_numpy().min()
        x_min = x_min_date_turnover if x_min_date_turnover < x_min_date_overall_rating else x_min_date_overall_rating

        x_max_date_overall_rating = df_overall_rating_development_since_beginning[x2].to_numpy().max()
        x_max = x_max_date_turnover if x_max_date_turnover > x_max_date_overall_rating else x_max_date_overall_rating

        # plot turnover development for a restaurant
        color = 'red'
        fig, ax1 = plt.subplots()
        ax1.set_xlabel('date')
        ax1.set_ylabel('turnover in CHF', color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        df_turnover_development_since_beginning.plot(x=x1, y=y1, ax=ax1, color=color, marker='o')

        # plot overall rating development for a restaurant in the same plot
        color = 'blue'
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        ax2.set_ylabel('overall rating', color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        df_overall_rating_development_since_beginning.plot(x=x2, y=y2, ax=ax2, color=color, marker='o')

        # fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.title(title + ": " + restaurant.value)
        plt.xlim([x_min, x_max])
        plt.legend(loc="upper left")
        plt.grid()
        plt.show()


prognoliteTripadvisorRestaurantDataAnalyzer = PrognoliteTripadvisorRestaurantDataAnalyzer()
