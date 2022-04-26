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

    def plot_development_of_overall_rating_and_average_turnover_per_time_period_for_all_restaurants(self,
                                                                                                    time_period='m',
                                                                                                    rating_date_offset_in_months=0):
        for restaurant in self.__restaurants:
            self.plot_development_of_overall_rating_and_average_turnover_per_time_period(restaurant, time_period,
                                                                                         rating_date_offset_in_months)

    def plot_development_of_overall_rating_and_average_turnover_per_time_period(self, restaurant, time_period='m',
                                                                                rating_date_offset_in_months=0):
        df_average_turnover_per_time_period = self.__prognoliteRestaurantDataExtractor \
            .get_average_turnover_per_time_period_dataframe(restaurant, time_period)

        tripadvisor_restaurant_data_uri = self.__restaurants[restaurant]
        df_overall_rating_development_since_beginning = \
            self.__tripadvisor_restaurant_data_extractors[tripadvisor_restaurant_data_uri] \
                .get_overall_rating_development_since_beginning_dataframe(time_period, rating_date_offset_in_months)

        title = "Development of overall rating vs average turnover\n over " \
                + self.__get_time_period_value(time_period) + "s: " + restaurant.value
        x1 = 'd'
        y1 = 'average_turnover_per_time_period'
        x2 = 'date'
        y2 = 'overall_rating_development'

        # plot average turnover per time period
        color = 'red'
        fig, ax1 = plt.subplots()
        ax1.set_xlabel(x2)
        ax1.set_ylabel('turnover in CHF', color=color)
        #ax1.set_ylim(bottom=0, top=df_average_turnover_per_time_period[y1].to_numpy().max())
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.plot(df_average_turnover_per_time_period[x1],
                 df_average_turnover_per_time_period[y1],
                 color=color,
                 marker='o')

        # plot overall rating development for a restaurant in the same plot
        color = 'blue'
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        ax2.set_ylabel('overall rating', color=color)
        ax2.set_ylim(1, 5)
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.plot(df_overall_rating_development_since_beginning[x2],
                 df_overall_rating_development_since_beginning[y2],
                 color=color,
                 marker='o')

        # fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.title(title)
        plt.setp(ax1.get_xticklabels(), rotation=30, horizontalalignment='right')
        labels = ['average_turnover_per_' + self.__get_time_period_value(time_period), 'overall_rating_development']
        fig.legend(labels, bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
        # plt.savefig('haha.png',dpi=600)
        plt.show()

    def plot_average_rating_vs_average_turnover_per_time_period_for_all_restaurants(self, time_period='m',
                                                                                    rating_date_offset_in_months=0):
        for restaurant in self.__restaurants:
            self.plot_average_rating_vs_average_turnover_per_time_period(restaurant, time_period,
                                                                         rating_date_offset_in_months)

    def plot_average_rating_vs_average_turnover_per_time_period(self, restaurant, time_period='m',
                                                                rating_date_offset_in_months=0):
        df_average_turnover_per_time_period = self.__prognoliteRestaurantDataExtractor \
            .get_average_turnover_per_time_period_dataframe(restaurant, time_period)

        tripadvisor_restaurant_data_uri = self.__restaurants[restaurant]
        df_average_rating_per_time_period = \
            self.__tripadvisor_restaurant_data_extractors[tripadvisor_restaurant_data_uri] \
                .get_average_rating_per_time_period_dataframe(time_period, rating_date_offset_in_months)

        title = "Average rating vs average turnover per " + self.__get_time_period_value(time_period) \
                + ":\n" + restaurant.value
        x1 = 'd'
        y1 = 'average_turnover_per_time_period'
        x2 = 'date'
        y2 = 'average_rating_per_time_period'

        # plot average turnover per time period
        color = 'red'
        fig, ax1 = plt.subplots()
        ax1.set_xlabel(x2)
        ax1.set_ylabel('turnover in CHF', color=color)
        # ax1.set_ylim(bottom=0, top=df_average_turnover_per_time_period[y1].to_numpy().max())
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.plot(df_average_turnover_per_time_period[x1],
                 df_average_turnover_per_time_period[y1],
                 color=color,
                 marker='o')

        # plot average rating for a restaurant in the same plot
        color = 'blue'
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        ax2.set_ylabel('overall rating', color=color)
        ax2.set_ylim(1, 5)
        ax2.tick_params(axis='y', labelcolor=color)
        ax2.plot(df_average_rating_per_time_period[x2],
                 df_average_rating_per_time_period[y2],
                 color=color,
                 marker='o')

        # fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.title(title)
        plt.setp(ax1.get_xticklabels(), rotation=30, horizontalalignment='right')
        labels = ['average_turnover_per_' + self.__get_time_period_value(time_period),
                  'average_rating_per_' + self.__get_time_period_value(time_period)]
        fig.legend(labels, bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
        # plt.savefig('haha.png',dpi=600)
        plt.show()

    def __get_time_period_value(self, time_period):
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


prognoliteTripadvisorRestaurantDataAnalyzer = PrognoliteTripadvisorRestaurantDataAnalyzer()
# prognoliteTripadvisorRestaurantDataAnalyzer.plot_development_of_overall_rating_and_average_turnover_per_time_period_for_all_restaurants('Q')
# prognoliteTripadvisorRestaurantDataAnalyzer.plot_development_of_overall_rating_and_average_turnover_per_time_period(Restaurant.BUTCHER_USTER,'Q')

# prognoliteTripadvisorRestaurantDataAnalyzer.plot_average_rating_vs_average_turnover_per_time_period_for_all_restaurants('Q')
# prognoliteTripadvisorRestaurantDataAnalyzer.plot_average_rating_vs_average_turnover_per_time_period(Restaurant.BUTCHER_USTER,'Q')
