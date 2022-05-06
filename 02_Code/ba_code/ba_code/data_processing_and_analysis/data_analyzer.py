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
import numpy as np
from dateutil.relativedelta import relativedelta


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

    def plot_overall_rating_development_and_average_turnover_per_time_period_for_all_restaurants(
            self,
            restaurant_review_data_type,
            time_period='m',
            rating_date_offset_in_months=0):

        for restaurant in Restaurant:
            self.plot_overall_rating_development_and_average_turnover_per_time_period(restaurant,
                                                                                      restaurant_review_data_type,
                                                                                      time_period,
                                                                                      rating_date_offset_in_months)

    def plot_overall_rating_development_and_average_turnover_per_time_period(self, restaurant,
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

        # define variables for plot
        title = "Overall rating development vs average turnover\n over " \
                + self.__get_time_period_value(time_period) + "s: " + restaurant.value
        labels_for_legend = ['average_turnover_per_' + self.__get_time_period_value(time_period),
                             'overall_rating_development']
        # define variables for the first plot (df1)
        parameters_for_the_first_plot = {
            'x1': 'd',
            'y1': 'average_turnover_per_time_period',
            'df1': df_average_turnover_per_time_period,
            'y1_label': 'turnover in CHF',
            'color1': 'red'
        }

        # define variables for second plot (df2)
        parameters_for_the_second_plot = {
            'x2': 'date',
            'y2': 'overall_rating_development',
            'df2': df_overall_rating_development_over_time_period,
            'y2_label': 'overall rating',
            'color2': 'blue'
        }

        self.__plot_turnover_and_rating_in_one_figure(title=title,
                                                      labels_for_legend=labels_for_legend,
                                                      parameters_for_the_first_plot=parameters_for_the_first_plot,
                                                      parameters_for_the_second_plot=parameters_for_the_second_plot)

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

        # define variables for plot
        title = "Average rating vs average turnover per " + self.__get_time_period_value(time_period) \
                + ":\n" + restaurant.value
        labels_for_legend = ['average_turnover_per_' + self.__get_time_period_value(time_period),
                             'average_rating_per_' + self.__get_time_period_value(time_period)]
        # define variables for the first plot (df1)
        parameters_for_the_first_plot = {
            'x1': 'd',
            'y1': 'average_turnover_per_time_period',
            'df1': df_average_turnover_per_time_period,
            'y1_label': 'turnover in CHF',
            'color1': 'red'
        }

        # define variables for second plot (df2)
        parameters_for_the_second_plot = {
            'x2': 'date',
            'y2': 'average_rating_per_time_period',
            'df2': df_average_rating_per_time_period,
            'y2_label': 'overall rating',
            'color2': 'blue'
        }

        self.__plot_turnover_and_rating_in_one_figure(title=title,
                                                      labels_for_legend=labels_for_legend,
                                                      parameters_for_the_first_plot=parameters_for_the_first_plot,
                                                      parameters_for_the_second_plot=parameters_for_the_second_plot)

    def plot_average_rating_google_and_average_rating_tripadvisor_for_all_restaurants(self, time_period='m'):
        for restaurant in Restaurant:
            self.plot_average_rating_google_and_average_rating_tripadvisor(restaurant, time_period)

    def plot_average_rating_google_and_average_rating_tripadvisor(self, restaurant, time_period='m'):
        # get tripadvisor_restaurant_review_data_extractor for a restaurant
        tripadvisor_restaurant_review_data_extractor = \
            self.__get_restaurant_review_data_extractor(restaurant, RestaurantReviewDataType.TRIPADVISOR_REVIEW)

        # get df_average_rating_per_time_period and change format of 'date' to join later
        df_average_rating_per_time_period_tripadvisor = tripadvisor_restaurant_review_data_extractor \
            .get_average_rating_per_time_period_dataframe(time_period)

        # get google_restaurant_review_data_extractor for a restaurant
        google_restaurant_review_data_extractor = \
            self.__get_restaurant_review_data_extractor(restaurant, RestaurantReviewDataType.GOOGLE_REVIEW)

        # get df_average_rating_per_time_period and change format of 'date' to join later
        df_average_rating_per_time_period_google = google_restaurant_review_data_extractor \
            .get_average_rating_per_time_period_dataframe(time_period)

        title = "Average rating tripadvisor vs average rating google per " + self.__get_time_period_value(time_period) \
                + ":\n" + restaurant.value
        x1 = 'date'
        y1 = 'average_rating_per_time_period'
        df1 = df_average_rating_per_time_period_tripadvisor
        x2 = x1
        y2 = y1
        df2 = df_average_rating_per_time_period_google

        x_max, x_min = self.__get_x_min_and_x_max_for_plot(df1, df2, x1, x2)

        plt.figure()
        ax = df1.plot(x=x1, y=y1, marker='o')
        df2.plot(ax=ax, x=x2, y=y2, marker='o')
        plt.title(title)
        plt.xlim([x_min, x_max])
        plt.ylim([1, 5])
        plt.xlabel(x1)
        plt.ylabel(y1)
        plt.legend()
        plt.show()

    def __plot_turnover_and_rating_in_one_figure(self, title,
                                                 labels_for_legend,
                                                 parameters_for_the_first_plot,
                                                 parameters_for_the_second_plot):
        # parameters for the first plot
        x1 = parameters_for_the_first_plot['x1']
        y1 = parameters_for_the_first_plot['y1']
        df1 = parameters_for_the_first_plot['df1']
        y1_label = parameters_for_the_first_plot['y1_label']
        color1 = parameters_for_the_first_plot['color1']

        # parameters for the second plot
        x2 = parameters_for_the_second_plot['x2']
        y2 = parameters_for_the_second_plot['y2']
        df2 = parameters_for_the_second_plot['df2']
        y2_label = parameters_for_the_second_plot['y2_label']
        color2 = parameters_for_the_second_plot['color2']

        x_max, x_min = self.__get_x_min_and_x_max_for_plot(df1, df2, x1, x2)

        # plot df1
        fig, ax1 = plt.subplots()
        ax1.set_xlabel(x2)
        ax1.set_ylabel(y1_label, color=color1)
        # ax1.set_ylim(bottom=0, top=df_average_turnover_per_time_period[y1].to_numpy().max())
        ax1.tick_params(axis='y', labelcolor=color1)
        ax1.plot(df1[x1],
                 df1[y1],
                 color=color1,
                 marker='o')

        # plot df2 in the same plot
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        ax2.set_ylabel(y2_label, color=color2)
        ax2.set_ylim(1, 5)
        ax2.tick_params(axis='y', labelcolor=color2)
        ax2.plot(df2[x2],
                 df2[y2],
                 color=color2,
                 marker='o')

        plt.title(title)
        plt.setp(ax1.get_xticklabels(), rotation=30, horizontalalignment='right')
        #fig.legend(labels_for_legend, bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.xlim([x_min, x_max])
        # plt.savefig('haha.png',dpi=600)
        plt.show()

    def __get_x_min_and_x_max_for_plot(self, df1, df2, x1, x2):
        # find x_min and x_max for the plot
        df1[x1] = pd.to_datetime(df1[x1].dt.date)
        df2[x2] = pd.to_datetime(df2[x2].dt.date)
        date_min_df1 = df1[x1].min()
        date_max_df1 = df1[x1].max()
        date_min_df2 = df2[x2].min()
        date_max_df2 = df2[x2].max()

        date_threshold_in_months = 6
        difference_between_min_dates = np.abs(date_min_df1 - date_min_df2) / np.timedelta64(1, 'M')
        difference_between_max_dates = np.abs(date_max_df1 - date_max_df2) / np.timedelta64(1, 'M')

        x_min = date_min_df1 if date_min_df1 < date_min_df2 else date_min_df1
        x_max = date_max_df1 if date_max_df1 > date_max_df2 else date_max_df2
        if difference_between_min_dates > date_threshold_in_months:
            x_min = date_min_df2 if date_min_df1 < date_min_df2 else date_min_df1
            x_min = x_min - relativedelta(months=date_threshold_in_months)
        if difference_between_max_dates > date_threshold_in_months:
            x_max = date_max_df2 if date_max_df1 > date_max_df2 else date_max_df1
            x_max = x_max + relativedelta(months=date_threshold_in_months)

        return x_max, x_min

    def compute_correlation_between_average_turnover_and_overall_rating_development_for_all_restaurants(
            self, restaurant_review_data_type, time_period='m', rating_date_offset_in_months=0):

        for restaurant in Restaurant:
            self.compute_correlation_between_average_turnover_and_overall_rating_development(
                restaurant, restaurant_review_data_type, time_period, rating_date_offset_in_months)

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

        # join df_average_turnover_per_time_period with df_overall_rating_development_over_time_period
        df_average_turnover_and_overall_rating_development_per_time_period = \
            self.__join_two_dataframes_on_date(df1=df_average_turnover_per_time_period,
                                               df2=df_overall_rating_development_over_time_period)

        # filter df_average_turnover_per_time_period before corona
        df_average_turnover_and_overall_rating_development_per_time_period = \
            self.__filter_entries_from_dataframe_before_corona(
                df_average_turnover_and_overall_rating_development_per_time_period)

        print("Restaurant:", restaurant.value)
        print("df_average_turnover_and_overall_rating_development_per_time_period:\n")
        print(df_average_turnover_and_overall_rating_development_per_time_period)

        self.__compute_pearson_and_spearman_correlation(
            df_average_turnover_and_overall_rating_development_per_time_period)

        # scatterplot average rating vs average turnover
        df = df_average_turnover_and_overall_rating_development_per_time_period
        x = 'overall_rating_development'
        y = 'average_turnover_per_time_period'
        title = 'overall rating development vs average turnover per ' \
                + self.__get_time_period_value(time_period) + ":\n" \
                + restaurant.value

        self.__scatterplot_dataframe(df, x, y, title)

    def compute_correlation_between_average_turnover_and_average_rating_for_all_restaurants(self,
                                                                                            restaurant_review_data_type,
                                                                                            time_period='m',
                                                                                            rating_date_offset_in_months=0):
        for restaurant in Restaurant:
            self.compute_correlation_between_average_turnover_and_average_rating(restaurant,
                                                                                 restaurant_review_data_type,
                                                                                 time_period,
                                                                                 rating_date_offset_in_months)

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

        # join df_average_turnover_per_time_period with df_average_rating_per_time_period
        df_average_turnover_and_average_rating_per_time_period = \
            self.__join_two_dataframes_on_date(df1=df_average_turnover_per_time_period,
                                               df2=df_average_rating_per_time_period)

        # filter df_average_turnover_per_time_period before corona
        df_average_turnover_and_average_rating_per_time_period = \
            self.__filter_entries_from_dataframe_before_corona(df_average_turnover_and_average_rating_per_time_period)

        print("Restaurant:", restaurant.value)
        print("df_average_turnover_and_average_rating_per_time_period:\n")
        print(df_average_turnover_and_average_rating_per_time_period)

        self.__compute_pearson_and_spearman_correlation(df_average_turnover_and_average_rating_per_time_period)

        # scatterplot average rating vs average turnover
        df = df_average_turnover_and_average_rating_per_time_period
        x = 'average_rating_per_time_period'
        y = 'average_turnover_per_time_period'
        title = 'average rating vs average turnover per ' \
                + self.__get_time_period_value(time_period) + ":\n" \
                + restaurant.value

        self.__scatterplot_dataframe(df, x, y, title)

    def compute_correlation_between_average_rating_google_and_average_rating_tripadvisor_for_all_restaurants(
            self, time_period='m'):

        for restaurant in Restaurant:
            self.compute_correlation_between_average_rating_google_and_average_rating_tripadvisor(restaurant,
                                                                                                  time_period)

    def compute_correlation_between_average_rating_google_and_average_rating_tripadvisor(self, restaurant,
                                                                                         time_period='m'):

        # get tripadvisor_restaurant_review_data_extractor for a restaurant
        tripadvisor_restaurant_review_data_extractor = \
            self.__get_restaurant_review_data_extractor(restaurant, RestaurantReviewDataType.TRIPADVISOR_REVIEW)

        # get df_average_rating_per_time_period and change format of 'date' to join later
        df_average_rating_per_time_period_tripadvisor = tripadvisor_restaurant_review_data_extractor \
            .get_average_rating_per_time_period_dataframe(time_period)
        df_average_rating_per_time_period_tripadvisor['date'] = \
            pd.to_datetime(df_average_rating_per_time_period_tripadvisor['date'].dt.date)

        print(df_average_rating_per_time_period_tripadvisor)

        # get google_restaurant_review_data_extractor for a restaurant
        google_restaurant_review_data_extractor = \
            self.__get_restaurant_review_data_extractor(restaurant, RestaurantReviewDataType.GOOGLE_REVIEW)

        # get df_average_rating_per_time_period and change format of 'date' to join later
        df_average_rating_per_time_period_google = google_restaurant_review_data_extractor \
            .get_average_rating_per_time_period_dataframe(time_period)
        df_average_rating_per_time_period_google['date'] = \
            pd.to_datetime(df_average_rating_per_time_period_google['date'].dt.date)

        print(df_average_rating_per_time_period_google)

        # join df_average_turnover_per_time_period with df_average_rating_per_time_period
        df_average_rating_tripadvisor_and_google_per_time_period = \
            self.__join_two_dataframes_on_date(df1=df_average_rating_per_time_period_tripadvisor,
                                               df2=df_average_rating_per_time_period_google)

        # filter df_average_turnover_per_time_period before corona
        df_average_rating_tripadvisor_and_google_per_time_period = \
            self.__filter_entries_from_dataframe_before_corona(df_average_rating_tripadvisor_and_google_per_time_period)

        print("Restaurant:", restaurant.value)
        print("df_average_rating_tripadvisor_and_google_per_time_period:\n")
        print(df_average_rating_tripadvisor_and_google_per_time_period)

        self.__compute_pearson_and_spearman_correlation(df_average_rating_tripadvisor_and_google_per_time_period)

        # scatterplot average rating vs average turnover
        df = df_average_rating_tripadvisor_and_google_per_time_period \
            .rename(columns={"average_rating_per_time_period_x": "average_rating_per_time_period_tripadvisor",
                             "average_rating_per_time_period_y": "average_rating_per_time_period_google"})
        x = 'average_rating_per_time_period_tripadvisor'
        y = 'average_rating_per_time_period_google'
        title = 'average rating tripadvisor vs average rating google per ' \
                + self.__get_time_period_value(time_period) + ":\n" \
                + restaurant.value

        self.__scatterplot_dataframe(df, x, y, title)

    def __join_two_dataframes_on_date(self, df1, df2):
        # df1 join df2
        df_merged = \
            pd.merge(left=df1, right=df2, on='date')

        # print(df_merged)

        # dropping rows containing NaN
        df_merged = \
            df_merged.dropna().reset_index(drop=True)

        # print(df_merged)
        return df_merged

    # TODO: implement filter like Marco said
    def __filter_entries_from_dataframe_before_corona(self, df):
        corona_start_year = 2020
        return df[df['date'].dt.year < corona_start_year]

    def __compute_pearson_and_spearman_correlation(self, df):
        # pearson correlation
        print("\nPearson correlation:")
        print(df.corr(method="pearson"))

        # spearman correlation
        print("\nSpearman correlation:")
        print(df.corr(method="spearman"))

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


# code template to create a dataAnalyzer
"""
dataAnalyzer = DataAnalyzer()
"""

# code templates to analyse tripadvisor review data with prognolite restaurant data
"""
dataAnalyzer.plot_overall_rating_development_and_average_turnover_per_time_period_for_all_restaurants(
    restaurant_review_data_type=RestaurantReviewDataType.TRIPADVISOR_REVIEW,
    time_period='m',
    rating_date_offset_in_months=0)

dataAnalyzer.plot_overall_rating_development_and_average_turnover_per_time_period(
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
dataAnalyzer.plot_overall_rating_development_and_average_turnover_per_time_period_for_all_restaurants(
    restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
    time_period='m',
    rating_date_offset_in_months=0)

dataAnalyzer.plot_overall_rating_development_and_average_turnover_per_time_period(
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
