import matplotlib.pyplot as plt
from ba_code.data_processing_and_analysis.prognolite.prognolite_restaurant_data_extractor import \
    PrognoliteRestaurantDataExtractor
from ba_code.data_processing_and_analysis.google_and_tripadvisor.restaurant_review_data_extractor import \
    RestaurantReviewDataExtractor
from ba_code.data_processing_and_analysis.prognolite.prognolite_restaurant_constants import \
    Restaurant
from ba_code.data_processing_and_analysis.google_and_tripadvisor.restaurant_review_data_uri import \
    TripadvisorRestaurantReviewDataUri, GoogleRestaurantReviewDataUri, RestaurantReviewDataType
import seaborn as sns
import pandas as pd


class DataAnalyzer:

    def __init__(self):
        self.__prognolite_restaurant_data_extractor = PrognoliteRestaurantDataExtractor()
        self.__tripadvisor_restaurant_review_data_extractors_dict = dict()
        self.__google_restaurant_review_data_extractors_dict = dict()
        self.__initialize_restaurant_review_data_extractors()

    def __initialize_restaurant_review_data_extractors(self):
        restaurant_review_data_uris = [TripadvisorRestaurantReviewDataUri, GoogleRestaurantReviewDataUri]

        for uri in restaurant_review_data_uris:
            restaurants_dict = dict(zip(Restaurant, uri))

            for restaurant, restaurant_review_data_uri in restaurants_dict.items():
                restaurant_review_data_extractor = RestaurantReviewDataExtractor()

                # initialize self.__tripadvisor_restaurant_review_data_extractors_dict
                if uri == TripadvisorRestaurantReviewDataUri:
                    restaurant_review_data_extractor \
                        .load_restaurant_review_data(open(restaurant_review_data_uri.value),
                                                     RestaurantReviewDataType.TRIPADVISOR_REVIEW)

                    self.__tripadvisor_restaurant_review_data_extractors_dict[restaurant] = \
                        restaurant_review_data_extractor

                # initialize self.__google_restaurant_review_data_extractors_dict
                elif uri == GoogleRestaurantReviewDataUri:
                    restaurant_review_data_extractor \
                        .load_restaurant_review_data(open(restaurant_review_data_uri.value),
                                                     RestaurantReviewDataType.GOOGLE_REVIEW)

                    self.__google_restaurant_review_data_extractors_dict[restaurant] = \
                        restaurant_review_data_extractor

    def plot_development_of_overall_rating_and_average_turnover_per_time_period_for_all_restaurants(self,
                                                                                                    restaurant_review_data_type,
                                                                                                    time_period='m',
                                                                                                    rating_date_offset_in_months=0):
        for restaurant in Restaurant:
            self.plot_development_of_overall_rating_and_average_turnover_per_time_period(restaurant,
                                                                                         restaurant_review_data_type,
                                                                                         time_period,
                                                                                         rating_date_offset_in_months)

    def plot_development_of_overall_rating_and_average_turnover_per_time_period(self, restaurant,
                                                                                restaurant_review_data_type,
                                                                                time_period='m',
                                                                                rating_date_offset_in_months=0):

        df_average_turnover_per_time_period = self.__prognolite_restaurant_data_extractor \
            .get_average_turnover_per_time_period_dataframe(restaurant, time_period)

        restaurant_review_data_extractor = self.__get_restaurant_review_data_extractor(restaurant,
                                                                                       restaurant_review_data_type)
        df_overall_rating_development_over_time_period = \
            restaurant_review_data_extractor \
                .get_overall_rating_development_over_time_period_dataframe(time_period, rating_date_offset_in_months)

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
        # ax1.set_ylim(bottom=0, top=df_average_turnover_per_time_period[y1].to_numpy().max())
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
        ax2.plot(df_overall_rating_development_over_time_period[x2],
                 df_overall_rating_development_over_time_period[y2],
                 color=color,
                 marker='o')

        # fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.title(title)
        plt.setp(ax1.get_xticklabels(), rotation=30, horizontalalignment='right')
        labels = ['average_turnover_per_' + self.__get_time_period_value(time_period), 'overall_rating_development']
        fig.legend(labels, bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
        # plt.savefig('haha.png',dpi=600)
        plt.show()

    def plot_average_rating_vs_average_turnover_per_time_period_for_all_restaurants(self,
                                                                                    restaurant_review_data_type,
                                                                                    time_period='m',
                                                                                    rating_date_offset_in_months=0):
        for restaurant in Restaurant:
            self.plot_average_rating_vs_average_turnover_per_time_period(restaurant,
                                                                         restaurant_review_data_type,
                                                                         time_period,
                                                                         rating_date_offset_in_months)

    def plot_average_rating_vs_average_turnover_per_time_period(self, restaurant,
                                                                restaurant_review_data_type,
                                                                time_period='m',
                                                                rating_date_offset_in_months=0):

        df_average_turnover_per_time_period = self.__prognolite_restaurant_data_extractor \
            .get_average_turnover_per_time_period_dataframe(restaurant, time_period)

        restaurant_review_data_extractor = self.__get_restaurant_review_data_extractor(restaurant,
                                                                                       restaurant_review_data_type)
        df_average_rating_per_time_period = \
            restaurant_review_data_extractor \
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

    def compute_correlation_between_average_turnover_and_overall_rating_development(self, restaurant,
                                                                                    restaurant_review_data_type,
                                                                                    time_period='m',
                                                                                    rating_date_offset_in_months=0):
        # get df_average_turnover_per_time_period
        df_average_turnover_per_time_period = self.__prognolite_restaurant_data_extractor \
            .get_average_turnover_per_time_period_dataframe(restaurant, time_period)

        # rename column 'd' to 'date' of df_average_turnover_per_time_period and change format of 'date' to join later
        df_average_turnover_per_time_period = df_average_turnover_per_time_period.rename(columns={'d': 'date'})
        df_average_turnover_per_time_period['date'] = pd.to_datetime(
            df_average_turnover_per_time_period['date'].dt.date)

        # print(df_average_turnover_per_time_period)

        # get tripadvisor_restaurant_data_extractor with tripadvisor_restaurant_data_uri
        restaurant_review_data_extractor = self.__get_restaurant_review_data_extractor(restaurant,
                                                                                       restaurant_review_data_type)

        # get df_average_rating_per_time_period and change format of 'date' to join later
        df_overall_rating_development_over_time_period = restaurant_review_data_extractor \
            .get_overall_rating_development_over_time_period_dataframe(time_period, rating_date_offset_in_months)
        df_overall_rating_development_over_time_period['date'] = pd.to_datetime(
            df_overall_rating_development_over_time_period['date'].dt.date)

        # print(df_average_turnover_and_average_rating_per_time_period)

        # df_average_turnover_per_time_period join df_average_rating_per_time_period
        df_average_turnover_and_overall_rating_development_per_time_period = \
            pd.merge(left=df_average_turnover_per_time_period, right=df_overall_rating_development_over_time_period,
                     on='date')

        # print(df_average_turnover_and_overall_rating_development_per_time_period)

        # dropping rows containing NaN
        df_average_turnover_and_overall_rating_development_per_time_period = \
            df_average_turnover_and_overall_rating_development_per_time_period.dropna().reset_index(drop=True)

        # print(df_average_turnover_and_overall_rating_development_per_time_period)

        # filter df_average_turnover_and_average_rating_per_time_period before corona
        corona_start_year = 2020

        df_average_turnover_and_overall_rating_development_per_time_period = \
            df_average_turnover_and_overall_rating_development_per_time_period[
                df_average_turnover_and_overall_rating_development_per_time_period['date'].dt.year < corona_start_year
                ]

        print("df_average_turnover_and_overall_rating_development_per_time_period:\n")
        print(df_average_turnover_and_overall_rating_development_per_time_period)

        # pearson correlation
        print("\nPearson correlation:")
        print(df_average_turnover_and_overall_rating_development_per_time_period.corr(method="pearson"))

        # spearman correlation
        print("\nSpearman correlation:")
        print(df_average_turnover_and_overall_rating_development_per_time_period.corr(method="spearman"))

        # scatterplot average rating vs average turnover
        df = df_average_turnover_and_overall_rating_development_per_time_period
        x = 'overall_rating_development'
        y = 'average_turnover_per_time_period'
        title = 'overall rating development vs average turnover per ' \
                + self.__get_time_period_value(time_period) + ":\n" \
                + restaurant.value

        self.__scatterplot_dataframe(df, x, y, title)

    def compute_correlation_between_average_turnover_and_average_rating(self, restaurant,
                                                                        restaurant_review_data_type,
                                                                        time_period='m',
                                                                        rating_date_offset_in_months=0):
        # get df_average_turnover_per_time_period
        df_average_turnover_per_time_period = \
            self.__prognolite_restaurant_data_extractor \
                .get_average_turnover_per_time_period_dataframe(restaurant, time_period)

        # rename column 'd' to 'date' of df_average_turnover_per_time_period and change format of 'date' to join later
        df_average_turnover_per_time_period = df_average_turnover_per_time_period.rename(columns={'d': 'date'})
        df_average_turnover_per_time_period['date'] = pd.to_datetime(
            df_average_turnover_per_time_period['date'].dt.date)

        # print(df_average_turnover_per_time_period)

        # get restaurant_review_data_extractor
        restaurant_review_data_extractor = self.__get_restaurant_review_data_extractor(restaurant,
                                                                                       restaurant_review_data_type)

        # get df_average_rating_per_time_period and change format of 'date' to join later
        df_average_rating_per_time_period = restaurant_review_data_extractor \
            .get_average_rating_per_time_period_dataframe(time_period, rating_date_offset_in_months)
        df_average_rating_per_time_period['date'] = pd.to_datetime(df_average_rating_per_time_period['date'].dt.date)

        # print(df_average_rating_per_time_period)

        # df_average_turnover_per_time_period join df_average_rating_per_time_period
        df_average_turnover_and_average_rating_per_time_period = \
            pd.merge(left=df_average_turnover_per_time_period, right=df_average_rating_per_time_period, on='date')

        # print(df_average_turnover_and_average_rating_per_time_period)

        # dropping rows containing NaN
        df_average_turnover_and_average_rating_per_time_period = \
            df_average_turnover_and_average_rating_per_time_period.dropna().reset_index(drop=True)

        # print(df_average_turnover_and_average_rating_per_time_period)

        # filter df_average_turnover_and_average_rating_per_time_period before corona
        corona_start_year = 2020

        df_average_turnover_and_average_rating_per_time_period = \
            df_average_turnover_and_average_rating_per_time_period[
                df_average_turnover_and_average_rating_per_time_period['date'].dt.year < corona_start_year
                ]

        print("df_average_turnover_and_average_rating_per_time_period:\n")
        print(df_average_turnover_and_average_rating_per_time_period)

        # pearson correlation
        print("\nPearson correlation:")
        print(df_average_turnover_and_average_rating_per_time_period.corr(method="pearson"))

        # spearman correlation
        print("\nSpearman correlation:")
        print(df_average_turnover_and_average_rating_per_time_period.corr(method="spearman"))

        # scatterplot average rating vs average turnover
        df = df_average_turnover_and_average_rating_per_time_period
        x = 'average_rating_per_time_period'
        y = 'average_turnover_per_time_period'
        title = 'average rating vs average turnover per ' \
                + self.__get_time_period_value(time_period) + ":\n" \
                + restaurant.value

        self.__scatterplot_dataframe(df, x, y, title)

    def __get_restaurant_review_data_extractor(self, restaurant, restaurant_review_data_type):
        restaurant_review_data_extractor = None

        if restaurant_review_data_type == RestaurantReviewDataType.TRIPADVISOR_REVIEW:
            restaurant_review_data_extractor = self.__tripadvisor_restaurant_review_data_extractors_dict[restaurant]
        elif restaurant_review_data_type == RestaurantReviewDataType.GOOGLE_REVIEW:
            restaurant_review_data_extractor = self.__google_restaurant_review_data_extractors_dict[restaurant]

        return restaurant_review_data_extractor

    def __scatterplot_dataframe(self, df, x, y, title):
        plt.figure()
        sns.set_style("darkgrid")
        sns.scatterplot(data=df, x=x, y=y).set(title=title)
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


dataAnalyzer = DataAnalyzer()

# code templates to analyse tripadvisor review data with prognolite restaurant data
"""
dataAnalyzer.plot_development_of_overall_rating_and_average_turnover_per_time_period_for_all_restaurants(
    restaurant_review_data_type=RestaurantReviewDataType.TRIPADVISOR_REVIEW,
    time_period='m',
    rating_date_offset_in_months=0)

dataAnalyzer.plot_development_of_overall_rating_and_average_turnover_per_time_period(
    restaurant=Restaurant.BUTCHER_USTER,
    restaurant_review_data_type=RestaurantReviewDataType.TRIPADVISOR_REVIEW,
    time_period='m',
    rating_date_offset_in_months=0)

dataAnalyzer.plot_average_rating_vs_average_turnover_per_time_period_for_all_restaurants(
    restaurant_review_data_type=RestaurantReviewDataType.TRIPADVISOR_REVIEW,
    time_period='m',
    rating_date_offset_in_months=0)

dataAnalyzer.plot_average_rating_vs_average_turnover_per_time_period(
    restaurant=Restaurant.BUTCHER_USTER,
    restaurant_review_data_type=RestaurantReviewDataType.TRIPADVISOR_REVIEW,
    time_period='m',
    rating_date_offset_in_months=0)

dataAnalyzer.compute_correlation_between_average_turnover_and_average_rating(
    restaurant=Restaurant.BUTCHER_USTER,
    restaurant_review_data_type=RestaurantReviewDataType.TRIPADVISOR_REVIEW,
    time_period='m',
    rating_date_offset_in_months=0)

dataAnalyzer.compute_correlation_between_average_turnover_and_overall_rating_development(
    restaurant=Restaurant.BUTCHER_USTER,
    restaurant_review_data_type=RestaurantReviewDataType.TRIPADVISOR_REVIEW,
    time_period='m',
    rating_date_offset_in_months=0)
"""

# code templates to analyse google review data with prognolite restaurant data
"""
dataAnalyzer.plot_development_of_overall_rating_and_average_turnover_per_time_period_for_all_restaurants(
    restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
    time_period='m',
    rating_date_offset_in_months=0)

dataAnalyzer.plot_development_of_overall_rating_and_average_turnover_per_time_period(
    restaurant=Restaurant.BUTCHER_USTER,
    restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
    time_period='m',
    rating_date_offset_in_months=0)

dataAnalyzer.plot_average_rating_vs_average_turnover_per_time_period_for_all_restaurants(
    restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
    time_period='m',
    rating_date_offset_in_months=0)

dataAnalyzer.plot_average_rating_vs_average_turnover_per_time_period(
    restaurant=Restaurant.BUTCHER_USTER,
    restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
    time_period='m',
    rating_date_offset_in_months=0)

dataAnalyzer.compute_correlation_between_average_turnover_and_average_rating(
    restaurant=Restaurant.BUTCHER_USTER,
    restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
    time_period='m',
    rating_date_offset_in_months=0)

dataAnalyzer.compute_correlation_between_average_turnover_and_overall_rating_development(
    restaurant=Restaurant.BUTCHER_USTER,
    restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
    time_period='m',
    rating_date_offset_in_months=0)
"""
