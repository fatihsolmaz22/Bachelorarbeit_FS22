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
from datetime import datetime
from enum import Enum
from statsmodels.tsa.seasonal import seasonal_decompose


class AnalyzerOption(Enum):
    OVERALL_RATING_VS_AVERAGE_TURNOVER = 1
    AVERAGE_RATING_VS_AVERAGE_TURNOVER = 2
    OVERALL_RATING_GOOGLE_VS_OVERALL_RATING_TRIPADVISOR = 3
    AVERAGE_RATING_GOOGLE_VS_AVERAGE_RATING_TRIPADVISOR = 4


class DecomposeOption(Enum):
    RESIDUAL = 1
    RESIDUAL_PLUS_TREND = 2


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

    def plot_for_all_restaurants(self, analyzer_option,
                                 restaurant_review_data_type,
                                 time_period='m',
                                 rating_date_offset_in_months=0,
                                 filter_corona_data=False,
                                 decompose_option=None):

        for restaurant in Restaurant:
            self.plot(analyzer_option, restaurant, restaurant_review_data_type, time_period,
                      rating_date_offset_in_months, filter_corona_data, decompose_option)

    def plot(self, analyzer_option,
             restaurant,
             restaurant_review_data_type,
             time_period='m',
             rating_date_offset_in_months=0,
             filter_corona_data=False,
             decompose_option=None):

        if analyzer_option == AnalyzerOption.OVERALL_RATING_VS_AVERAGE_TURNOVER:
            self.__plot_overall_rating_development_and_average_turnover_per_time_period(restaurant,
                                                                                        restaurant_review_data_type,
                                                                                        time_period,
                                                                                        rating_date_offset_in_months,
                                                                                        filter_corona_data,
                                                                                        decompose_option)

        elif analyzer_option == AnalyzerOption.AVERAGE_RATING_VS_AVERAGE_TURNOVER:
            self.__plot_average_rating_and_average_turnover_per_time_period(restaurant,
                                                                            restaurant_review_data_type,
                                                                            time_period,
                                                                            rating_date_offset_in_months,
                                                                            filter_corona_data,
                                                                            decompose_option)

        elif analyzer_option == AnalyzerOption.OVERALL_RATING_GOOGLE_VS_OVERALL_RATING_TRIPADVISOR:
            self.__plot_overall_rating_google_and_overall_rating_tripadvisor(restaurant, time_period,
                                                                             filter_corona_data)

        elif analyzer_option == AnalyzerOption.AVERAGE_RATING_GOOGLE_VS_AVERAGE_RATING_TRIPADVISOR:
            self.__plot_average_rating_google_and_average_rating_tripadvisor(restaurant, time_period,
                                                                             filter_corona_data)
        else:
            print("Invalid AnalyzerOption")

    def __plot_overall_rating_development_and_average_turnover_per_time_period(self, restaurant,
                                                                               restaurant_review_data_type,
                                                                               time_period='m',
                                                                               rating_date_offset_in_months=0,
                                                                               filter_corona_data=False,
                                                                               decompose_option=None):

        df_average_turnover_per_time_period_decomposed = \
            self.__prepare_df_average_turnover_per_time_period_decomposed(restaurant, time_period)

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
            'x1': 'date',
            'y1': 'average_turnover_per_time_period',
            'df1': df_average_turnover_per_time_period_decomposed,
            'y1_label': 'average turnover in CHF',
            'color1': 'red'
        }

        if decompose_option == DecomposeOption.RESIDUAL:
            title = "Overall rating development vs average turnover\n over " \
                    + self.__get_time_period_value(time_period) + "s (residual): " + restaurant.value
            parameters_for_the_first_plot['y1'] = 'residual'

            if df_average_turnover_per_time_period_decomposed['residual'].isnull().all():
                print("Couldn't perform decompose and generate plot for", restaurant.value)
                return

        elif decompose_option == DecomposeOption.RESIDUAL_PLUS_TREND:
            title = "Overall rating development vs average turnover\n over " \
                    + self.__get_time_period_value(time_period) + "s (residual + trend): " + restaurant.value
            parameters_for_the_first_plot['y1'] = 'residual_plus_trend'

            if df_average_turnover_per_time_period_decomposed['residual_plus_trend'].isnull().all():
                print("Couldn't perform decompose and generate plot for", restaurant.value)
                return

        # define variables for second plot (df2)
        parameters_for_the_second_plot = {
            'x2': 'date',
            'y2': 'overall_rating_development',
            'df2': df_overall_rating_development_over_time_period,
            'y2_label': 'overall rating',
            'color2': 'blue'
        }

        self.__plot_turnover_and_rating_in_one_figure(restaurant=restaurant,
                                                      title=title,
                                                      labels_for_legend=labels_for_legend,
                                                      parameters_for_the_first_plot=parameters_for_the_first_plot,
                                                      parameters_for_the_second_plot=parameters_for_the_second_plot,
                                                      filter_corona_data=filter_corona_data)

    def __plot_average_rating_and_average_turnover_per_time_period(self, restaurant,
                                                                   restaurant_review_data_type,
                                                                   time_period='m',
                                                                   rating_date_offset_in_months=0,
                                                                   filter_corona_data=False,
                                                                   decompose_option=None):

        df_average_turnover_per_time_period_decomposed = \
            self.__prepare_df_average_turnover_per_time_period_decomposed(restaurant, time_period)

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
            'x1': 'date',
            'y1': 'average_turnover_per_time_period',
            'df1': df_average_turnover_per_time_period_decomposed,
            'y1_label': 'average turnover in CHF',
            'color1': 'red'
        }

        if decompose_option == DecomposeOption.RESIDUAL:
            title = "Average rating vs average turnover\n over " \
                    + self.__get_time_period_value(time_period) + "s (residual): " + restaurant.value
            parameters_for_the_first_plot['y1'] = 'residual'

            if df_average_turnover_per_time_period_decomposed['residual'].isnull().all():
                print("Couldn't perform decompose and generate plot for", restaurant.value)
                return

        elif decompose_option == DecomposeOption.RESIDUAL_PLUS_TREND:
            title = "Average rating vs average turnover\n over " \
                    + self.__get_time_period_value(time_period) + "s (residual + trend): " + restaurant.value
            parameters_for_the_first_plot['y1'] = 'residual_plus_trend'

            if df_average_turnover_per_time_period_decomposed['residual_plus_trend'].isnull().all():
                print("Couldn't perform decompose and generate plot for", restaurant.value)
                return

        # define variables for second plot (df2)
        parameters_for_the_second_plot = {
            'x2': 'date',
            'y2': 'average_rating_per_time_period',
            'df2': df_average_rating_per_time_period,
            'y2_label': 'average rating',
            'color2': 'blue'
        }

        self.__plot_turnover_and_rating_in_one_figure(restaurant=restaurant,
                                                      title=title,
                                                      labels_for_legend=labels_for_legend,
                                                      parameters_for_the_first_plot=parameters_for_the_first_plot,
                                                      parameters_for_the_second_plot=parameters_for_the_second_plot,
                                                      filter_corona_data=filter_corona_data)

    def __plot_turnover_and_rating_in_one_figure(self,
                                                 restaurant,
                                                 title,
                                                 labels_for_legend,
                                                 parameters_for_the_first_plot,
                                                 parameters_for_the_second_plot,
                                                 filter_corona_data):
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

        if filter_corona_data:
            x_max = datetime.strptime('2020', '%Y')

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
        # fig.legend(labels_for_legend, bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.xlim([x_min, x_max])
        picture_name = self.get_picture_name(restaurant, filter_corona_data)
        plt.savefig('{}-lineplot.png'.format(picture_name), dpi=600)
        plt.show()

    def __plot_overall_rating_google_and_overall_rating_tripadvisor(self, restaurant, time_period='m',
                                                                    filter_corona_data=False):
        # get tripadvisor_restaurant_review_data_extractor for a restaurant
        tripadvisor_restaurant_review_data_extractor = \
            self.__get_restaurant_review_data_extractor(restaurant, RestaurantReviewDataType.TRIPADVISOR_REVIEW)

        # get df_average_rating_per_time_period
        df_overall_rating_per_time_period_tripadvisor = tripadvisor_restaurant_review_data_extractor \
            .get_overall_rating_development_over_time_period_dataframe(time_period)

        # get google_restaurant_review_data_extractor for a restaurant
        google_restaurant_review_data_extractor = \
            self.__get_restaurant_review_data_extractor(restaurant, RestaurantReviewDataType.GOOGLE_REVIEW)

        # get df_average_rating_per_time_period
        df_overall_rating_per_time_period_google = google_restaurant_review_data_extractor \
            .get_overall_rating_development_over_time_period_dataframe(time_period)

        title = "Overall rating tripadvisor vs overall rating google per " + self.__get_time_period_value(time_period) \
                + ":\n" + restaurant.value
        x1 = 'date'
        y1 = 'overall_rating_development'
        df1 = df_overall_rating_per_time_period_tripadvisor
        x2 = x1
        y2 = y1
        df2 = df_overall_rating_per_time_period_google

        self.__plot_google_and_tripadvisor_rating(title, df1, x1, y1, df2, x2, y2, filter_corona_data)

    def __plot_average_rating_google_and_average_rating_tripadvisor(self, restaurant, time_period='m',
                                                                    filter_corona_data=False):
        # get tripadvisor_restaurant_review_data_extractor for a restaurant
        tripadvisor_restaurant_review_data_extractor = \
            self.__get_restaurant_review_data_extractor(restaurant, RestaurantReviewDataType.TRIPADVISOR_REVIEW)

        # get df_average_rating_per_time_period
        df_average_rating_per_time_period_tripadvisor = tripadvisor_restaurant_review_data_extractor \
            .get_average_rating_per_time_period_dataframe(time_period)

        # get google_restaurant_review_data_extractor for a restaurant
        google_restaurant_review_data_extractor = \
            self.__get_restaurant_review_data_extractor(restaurant, RestaurantReviewDataType.GOOGLE_REVIEW)

        # get df_average_rating_per_time_period
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

        self.__plot_google_and_tripadvisor_rating(title, df1, x1, y1, df2, x2, y2, filter_corona_data)

    def __plot_google_and_tripadvisor_rating(self, title, df1, x1, y1, df2, x2, y2, filter_corona_data):

        x_max, x_min = self.__get_x_min_and_x_max_for_plot(df1, df2, x1, x2)

        if filter_corona_data:
            x_max = datetime.strptime('2020', '%Y')

        ax = df1.plot(x=x1, y=y1, marker='o', label='Tripadvisor')
        df2.plot(ax=ax, x=x2, y=y2, marker='o', label='Google')
        plt.title(title)
        plt.xlim([x_min, x_max])
        plt.ylim([1, 5])
        plt.xlabel(x1)
        plt.ylabel('rating')
        plt.legend()
        plt.show()

    @staticmethod
    def get_picture_name(restaurant, filter_corona_data):
        if filter_corona_data:
            picture_name = restaurant.value + "-before-corona"
        else:
            picture_name = restaurant.value + "-after-corona"
        return picture_name

    @staticmethod
    def __get_x_min_and_x_max_for_plot(df1, df2, x1, x2):
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

    def compute_correlation_for_all_restaurants(self, analyzer_option,
                                                restaurant_review_data_type,
                                                time_period='m',
                                                rating_date_offset_in_months=0,
                                                filter_corona_data=False,
                                                decompose_option=None):
        restaurant_name_list = []
        pearson_list = []
        spearman_list = []

        for restaurant in Restaurant:
            pearson_corr_value, spearman_corr_value = self.compute_correlation(analyzer_option, restaurant,
                                                                               restaurant_review_data_type, time_period,
                                                                               rating_date_offset_in_months,
                                                                               filter_corona_data,
                                                                               decompose_option)

            restaurant_name = self.get_picture_name(restaurant, filter_corona_data)
            restaurant_name_list.append(restaurant_name)
            pearson_list.append(pearson_corr_value)
            spearman_list.append(spearman_corr_value)

        return pd.DataFrame({"restaurant_name": restaurant_name_list,
                             "pearson": pearson_list,
                             "spearman": spearman_list})

    def compute_correlation(self, analyzer_option,
                            restaurant,
                            restaurant_review_data_type,
                            time_period='m',
                            rating_date_offset_in_months=0,
                            filter_corona_data=False,
                            decompose_option=None):

        if analyzer_option == AnalyzerOption.OVERALL_RATING_VS_AVERAGE_TURNOVER:
            pearson_corr_value, spearman_corr_value = \
                self.__compute_correlation_between_overall_rating_and_average_turnover(
                    restaurant, restaurant_review_data_type, time_period, rating_date_offset_in_months,
                    filter_corona_data, decompose_option)

        elif analyzer_option == AnalyzerOption.AVERAGE_RATING_VS_AVERAGE_TURNOVER:
            pearson_corr_value, spearman_corr_value = \
                self.__compute_correlation_between_average_rating_and_average_turnover(
                    restaurant,
                    restaurant_review_data_type,
                    time_period,
                    rating_date_offset_in_months,
                    filter_corona_data, decompose_option)

        elif analyzer_option == AnalyzerOption.OVERALL_RATING_GOOGLE_VS_OVERALL_RATING_TRIPADVISOR:
            pearson_corr_value, spearman_corr_value = \
                self.__compute_correlation_between_overall_rating_google_and_overall_rating_tripadvisor(
                    restaurant,
                    time_period,
                    filter_corona_data)

        elif analyzer_option == AnalyzerOption.AVERAGE_RATING_GOOGLE_VS_AVERAGE_RATING_TRIPADVISOR:
            pearson_corr_value, spearman_corr_value = \
                self.__compute_correlation_between_average_rating_google_and_average_rating_tripadvisor(
                    restaurant,
                    time_period,
                    filter_corona_data)
        else:
            pearson_corr_value = None
            spearman_corr_value = None
            print("Invalid AnalyzerOption")

        return pearson_corr_value, spearman_corr_value

    def __compute_correlation_between_overall_rating_and_average_turnover(self, restaurant,
                                                                          restaurant_review_data_type,
                                                                          time_period='m',
                                                                          rating_date_offset_in_months=0,
                                                                          filter_corona_data=False,
                                                                          decompose_option=None):
        df_average_turnover_per_time_period, y, y_label = \
            self.__get_average_turnover_dataframe_with_plot_parameters(restaurant,
                                                                       time_period,
                                                                       decompose_option)

        if df_average_turnover_per_time_period[y].isnull().all():
            print("Couldn't perform decompose and compute correlation for", restaurant.value)
            return None, None

        restaurant_review_data_extractor = self.__get_restaurant_review_data_extractor(restaurant,
                                                                                       restaurant_review_data_type)

        # get df_average_rating_per_time_period and change format of 'date' to join later
        df_overall_rating_development_over_time_period = restaurant_review_data_extractor \
            .get_overall_rating_development_over_time_period_dataframe(time_period, rating_date_offset_in_months)
        df_overall_rating_development_over_time_period['date'] = pd.to_datetime(
            df_overall_rating_development_over_time_period['date'].dt.date)

        df_join_average_turnover_overall_rating, pearson_corr_value, spearman_corr_value = \
            self.__compute_pearson_and_spearman_corr_value(df1=df_average_turnover_per_time_period,
                                                           df2=df_overall_rating_development_over_time_period,
                                                           filter_corona_data=filter_corona_data,
                                                           restaurant=restaurant)
        x = 'overall_rating_development'
        x_label = 'overall rating development'
        title = 'overall rating development vs average turnover per ' \
                + self.__get_time_period_value(time_period) + ":\n" \
                + restaurant.value

        self.__scatterplot_dataframe(restaurant, filter_corona_data,
                                     df_join_average_turnover_overall_rating, x, y, x_label, y_label, title)

        return pearson_corr_value, spearman_corr_value

    def __compute_correlation_between_average_rating_and_average_turnover(self, restaurant,
                                                                          restaurant_review_data_type,
                                                                          time_period='m',
                                                                          rating_date_offset_in_months=0,
                                                                          filter_corona_data=False,
                                                                          decompose_option=None):
        df_average_turnover_per_time_period, y, y_label = \
            self.__get_average_turnover_dataframe_with_plot_parameters(restaurant,
                                                                       time_period,
                                                                       decompose_option)

        if df_average_turnover_per_time_period[y].isnull().all():
            print("Couldn't perform decompose and compute correlation for", restaurant.value)
            return None, None

        restaurant_review_data_extractor = self.__get_restaurant_review_data_extractor(restaurant,
                                                                                       restaurant_review_data_type)

        # get df_average_rating_per_time_period and change format of 'date' to join later
        df_average_rating_per_time_period = restaurant_review_data_extractor \
            .get_average_rating_per_time_period_dataframe(time_period, rating_date_offset_in_months)
        df_average_rating_per_time_period['date'] = pd.to_datetime(df_average_rating_per_time_period['date'].dt.date)

        df_join_average_turnover_average_rating, pearson_corr_value, spearman_corr_value = \
            self.__compute_pearson_and_spearman_corr_value(df1=df_average_turnover_per_time_period,
                                                           df2=df_average_rating_per_time_period,
                                                           filter_corona_data=filter_corona_data,
                                                           restaurant=restaurant)

        x = 'average_rating_per_time_period'
        x_label = 'average rating'
        title = 'average rating vs average turnover per ' \
                + self.__get_time_period_value(time_period) + ":\n" \
                + restaurant.value

        self.__scatterplot_dataframe(restaurant, filter_corona_data,
                                     df_join_average_turnover_average_rating, x, y, x_label, y_label, title)

        return pearson_corr_value, spearman_corr_value

    def __get_average_turnover_dataframe_with_plot_parameters(self, restaurant, time_period, decompose_option):
        df_average_turnover_per_time_period_decomposed = \
            self.__prepare_df_average_turnover_per_time_period_decomposed(restaurant, time_period)

        if decompose_option == DecomposeOption.RESIDUAL:
            y = 'residual'
            y_label = 'average turnover (residual) in CHF'
            df_average_turnover_per_time_period = \
                df_average_turnover_per_time_period_decomposed[['date', y]]

        elif decompose_option == DecomposeOption.RESIDUAL_PLUS_TREND:
            y = 'residual_plus_trend'
            y_label = 'average turnover (residual + trend) in CHF'
            df_average_turnover_per_time_period = \
                df_average_turnover_per_time_period_decomposed[['date', y]]

        else:
            y = 'average_turnover_per_time_period'
            y_label = 'average turnover in CHF'
            df_average_turnover_per_time_period = \
                df_average_turnover_per_time_period_decomposed[['date', y]]

        return df_average_turnover_per_time_period, y, y_label

    def __prepare_df_average_turnover_per_time_period_decomposed(self, restaurant, time_period):
        # get df_average_turnover_per_time_period
        df_average_turnover_per_time_period = \
            self.__prognolite_restaurant_data_extractor \
                .get_average_turnover_per_time_period_dataframe(restaurant, time_period)

        # rename column 'd' to 'date' of df_average_turnover_per_time_period and change format of 'date' to join later
        df_average_turnover_per_time_period = df_average_turnover_per_time_period.rename(columns={'d': 'date'})
        df_average_turnover_per_time_period['date'] = \
            pd.to_datetime(df_average_turnover_per_time_period['date'].dt.date)

        return self.__decompose_average_turnover_per_time_period_dataframe(df_average_turnover_per_time_period)

    @staticmethod
    def __decompose_average_turnover_per_time_period_dataframe(df_average_turnover_per_time_period):
        df_average_turnover_per_time_period.dropna(subset=['average_turnover_per_time_period'], inplace=True)

        try:
            decomposed_components = seasonal_decompose(df_average_turnover_per_time_period
                                                       .set_index('date')['average_turnover_per_time_period'],
                                                       model='additive')
            decomposed_components.plot()
            plt.show()

            df_resid = decomposed_components.resid.to_frame().reset_index()
            df_seasonal = decomposed_components.seasonal.to_frame().reset_index()
            df_trend = decomposed_components.trend.to_frame().reset_index()
        except:
            empty_values = [np.nan for x in range(len(df_average_turnover_per_time_period))]

            df_resid = pd.DataFrame({
                'resid': empty_values
            })
            df_seasonal = pd.DataFrame({
                'seasonal': empty_values
            })
            df_trend = pd.DataFrame({
                'trend': empty_values
            })

        df_average_turnover_per_time_period_decomposed = pd.DataFrame({
            'date': df_average_turnover_per_time_period['date'],
            'average_turnover_per_time_period': df_average_turnover_per_time_period['average_turnover_per_time_period'],
            'residual': df_resid['resid'],
            'seasonal': df_seasonal['seasonal'],
            'trend': df_trend['trend'],
            'residual_plus_trend': df_resid['resid'] + df_trend['trend']
        })

        return df_average_turnover_per_time_period_decomposed

    def __compute_correlation_between_overall_rating_google_and_overall_rating_tripadvisor(self,
                                                                                           restaurant,
                                                                                           time_period='m',
                                                                                           filter_corona_data=False):

        # get tripadvisor_restaurant_review_data_extractor for a restaurant
        tripadvisor_restaurant_review_data_extractor = \
            self.__get_restaurant_review_data_extractor(restaurant, RestaurantReviewDataType.TRIPADVISOR_REVIEW)

        # get df_average_rating_per_time_period and change format of 'date' to join later
        df_overall_rating_per_time_period_tripadvisor = tripadvisor_restaurant_review_data_extractor \
            .get_overall_rating_development_over_time_period_dataframe(time_period)
        df_overall_rating_per_time_period_tripadvisor['date'] = \
            pd.to_datetime(df_overall_rating_per_time_period_tripadvisor['date'].dt.date)

        # get google_restaurant_review_data_extractor for a restaurant
        google_restaurant_review_data_extractor = \
            self.__get_restaurant_review_data_extractor(restaurant, RestaurantReviewDataType.GOOGLE_REVIEW)

        # get df_average_rating_per_time_period and change format of 'date' to join later
        df_overall_rating_per_time_period_google = google_restaurant_review_data_extractor \
            .get_overall_rating_development_over_time_period_dataframe(time_period)
        df_overall_rating_per_time_period_google['date'] = \
            pd.to_datetime(df_overall_rating_per_time_period_google['date'].dt.date)

        df_join_overall_rating_google_and_tripadvisor, pearson_corr_value, spearman_corr_value = \
            self.__compute_pearson_and_spearman_corr_value(df1=df_overall_rating_per_time_period_tripadvisor,
                                                           df2=df_overall_rating_per_time_period_google,
                                                           filter_corona_data=filter_corona_data,
                                                           restaurant=restaurant)

        df_join_overall_rating_google_and_tripadvisor = \
            df_join_overall_rating_google_and_tripadvisor.rename(
                columns={"overall_rating_development_x": "overall_rating_development_tripadvisor",
                         "overall_rating_development_y": "overall_rating_development_google"})
        x = 'overall_rating_development_tripadvisor'
        y = 'overall_rating_development_google'
        x_label = 'overall rating development tripadvisor'
        y_label = 'overall rating development google'
        title = 'overall rating tripadvisor vs overall rating google per ' \
                + self.__get_time_period_value(time_period) + ":\n" \
                + restaurant.value

        self.__scatterplot_dataframe(restaurant, filter_corona_data,
                                     df_join_overall_rating_google_and_tripadvisor, x, y, x_label, y_label, title)

        return pearson_corr_value, spearman_corr_value

    def __compute_correlation_between_average_rating_google_and_average_rating_tripadvisor(self, restaurant,
                                                                                           time_period='m',
                                                                                           filter_corona_data=False):

        # get tripadvisor_restaurant_review_data_extractor for a restaurant
        tripadvisor_restaurant_review_data_extractor = \
            self.__get_restaurant_review_data_extractor(restaurant, RestaurantReviewDataType.TRIPADVISOR_REVIEW)

        # get df_average_rating_per_time_period and change format of 'date' to join later
        df_average_rating_per_time_period_tripadvisor = tripadvisor_restaurant_review_data_extractor \
            .get_average_rating_per_time_period_dataframe(time_period)
        df_average_rating_per_time_period_tripadvisor['date'] = \
            pd.to_datetime(df_average_rating_per_time_period_tripadvisor['date'].dt.date)

        # get google_restaurant_review_data_extractor for a restaurant
        google_restaurant_review_data_extractor = \
            self.__get_restaurant_review_data_extractor(restaurant, RestaurantReviewDataType.GOOGLE_REVIEW)

        # get df_average_rating_per_time_period and change format of 'date' to join later
        df_average_rating_per_time_period_google = google_restaurant_review_data_extractor \
            .get_average_rating_per_time_period_dataframe(time_period)
        df_average_rating_per_time_period_google['date'] = \
            pd.to_datetime(df_average_rating_per_time_period_google['date'].dt.date)

        df_join_average_rating_google_and_tripadvisor, pearson_corr_value, spearman_corr_value = \
            self.__compute_pearson_and_spearman_corr_value(df1=df_average_rating_per_time_period_tripadvisor,
                                                           df2=df_average_rating_per_time_period_google,
                                                           filter_corona_data=filter_corona_data,
                                                           restaurant=restaurant)

        df_join_average_rating_google_and_tripadvisor = \
            df_join_average_rating_google_and_tripadvisor.rename(
                columns={"average_rating_per_time_period_x": "average_rating_per_time_period_tripadvisor",
                         "average_rating_per_time_period_y": "average_rating_per_time_period_google"})
        x = 'average_rating_per_time_period_tripadvisor'
        y = 'average_rating_per_time_period_google'
        x_label = 'average rating per time period tripadvisor'
        y_label = 'average rating per time period google'
        title = 'average rating tripadvisor vs average rating google per ' \
                + self.__get_time_period_value(time_period) + ":\n" \
                + restaurant.value

        self.__scatterplot_dataframe(restaurant, filter_corona_data,
                                     df_join_average_rating_google_and_tripadvisor, x, y, x_label, y_label, title)

        return pearson_corr_value, spearman_corr_value

    def __compute_pearson_and_spearman_corr_value(self, df1, df2, filter_corona_data, restaurant):

        df_join = self.__join_two_dataframes_on_date(df1=df1, df2=df2)

        if filter_corona_data:
            df_join = self.__filter_entries_from_dataframe_before_corona(df_join)
        print("\nRestaurant:", restaurant.value)

        pearson_corr_matrix, spearman_corr_matrix = self.__compute_pearson_and_spearman_corr_matrix(df_join)
        pearson_corr_value = pearson_corr_matrix.iloc[0, 1]
        spearman_corr_value = spearman_corr_matrix.iloc[0, 1]

        return df_join, pearson_corr_value, spearman_corr_value

    @staticmethod
    def __join_two_dataframes_on_date(df1, df2):
        # df1 join df2
        df_merged = pd.merge(left=df1, right=df2, on='date')

        # dropping rows containing NaN
        df_merged = df_merged.dropna().reset_index(drop=True)

        return df_merged

    # TODO: implement filter like Marco said
    @staticmethod
    def __filter_entries_from_dataframe_before_corona(df):
        corona_start_year = 2020
        return df[df['date'].dt.year < corona_start_year]

    @staticmethod
    def __compute_pearson_and_spearman_corr_matrix(df):
        # pearson correlation
        pearson_correlation_matrix = df.corr(method="pearson")
        print("\nPearson correlation:")
        print(pearson_correlation_matrix)

        # spearman correlation
        spearman_correlation_matrix = df.corr(method="spearman")
        print("\nSpearman correlation:")
        print(spearman_correlation_matrix)

        return pearson_correlation_matrix, spearman_correlation_matrix

    def __get_restaurant_review_data_extractor(self, restaurant, restaurant_review_data_type):
        restaurant_review_data_extractor = None

        if restaurant_review_data_type == RestaurantReviewDataType.TRIPADVISOR_REVIEW:
            restaurant_review_data_extractor = self.__tripadvisor_restaurant_review_data_extractors_dict[restaurant]
        elif restaurant_review_data_type == RestaurantReviewDataType.GOOGLE_REVIEW:
            restaurant_review_data_extractor = self.__google_restaurant_review_data_extractors_dict[restaurant]

        return restaurant_review_data_extractor

    def __scatterplot_dataframe(self, restaurant, filter_corona_data, df, x, y, x_label, y_label, title):
        plt.figure()
        sns.set_style("darkgrid")
        sns.scatterplot(data=df, x=x, y=y).set(title=title)
        picture_name = self.get_picture_name(restaurant, filter_corona_data)
        plt.savefig('{}-corr.png'.format(picture_name), dpi=600)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()

    @staticmethod
    def __get_time_period_value(time_period):
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

    def print_number_of_review_for_all_restaurants(self):

        restaurants = []
        number_of_reviews_tripadvisor = []
        number_of_reviews_google = []

        for restaurant in Restaurant:
            tripadvisor_restaurant_review_data_extractor = \
                self.__get_restaurant_review_data_extractor(restaurant,RestaurantReviewDataType.TRIPADVISOR_REVIEW)
            google_review_data_extractor = \
                self.__get_restaurant_review_data_extractor(restaurant,RestaurantReviewDataType.GOOGLE_REVIEW)

            restaurants.append(restaurant.value)
            number_of_reviews_tripadvisor.append(tripadvisor_restaurant_review_data_extractor.get_number_of_reviews())
            number_of_reviews_google.append(google_review_data_extractor.get_number_of_reviews())

        pd.set_option('display.max_columns', None)
        df_number_of_review_for_each_restaurant = pd.DataFrame({
            'restaurant': restaurants,
            'number_of_reviews_tripadvisor': number_of_reviews_tripadvisor,
            'number_of_reviews_google': number_of_reviews_google,
        })

        print(df_number_of_review_for_each_restaurant)



# code template to create a dataAnalyzer
"""
dataAnalyzer = DataAnalyzer()
"""

# code template to analyse tripadvisor/google review data with prognolite restaurant data
"""
dataAnalyzer.plot_for_all_restaurants(analyzer_option=AnalyzerOption.AVERAGE_RATING_VS_AVERAGE_TURNOVER,
                                          restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
                                          time_period='m',
                                          rating_date_offset_in_months=0,
                                          filter_corona_data=False)
                                          
dataAnalyzer.plot(analyzer_option=AnalyzerOption.OVERALL_RATING_GOOGLE_VS_OVERALL_RATING_TRIPADVISOR,
                  restaurant=Restaurant.BUTCHER_USTER,
                  restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
                  time_period='m',
                  rating_date_offset_in_months=0,
                  filter_corona_data=False)
                                          
dataAnalyzer.compute_correlation_for_all_restaurants(
    analyzer_option=AnalyzerOption.OVERALL_RATING_VS_AVERAGE_TURNOVER,
    restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
    time_period='m',
    rating_date_offset_in_months=0,
    filter_corona_data=False)
    
dataAnalyzer.compute_correlation(analyzer_option=AnalyzerOption.OVERALL_RATING_GOOGLE_VS_OVERALL_RATING_TRIPADVISOR,
                                 restaurant=Restaurant.BUTCHER_USTER,
                                 restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
                                 time_period='m',
                                 rating_date_offset_in_months=0,
                                 filter_corona_data=False)
"""


def main():
    dataAnalyzer = DataAnalyzer()
    # dataAnalyzer.plot(analyzer_option=AnalyzerOption.AVERAGE_RATING_VS_AVERAGE_TURNOVER,
    #                   restaurant=Restaurant.NOOCH_BARFI,
    #                   restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
    #                   time_period='m',
    #                   rating_date_offset_in_months=0,
    #                   filter_corona_data=False,
    #                   decompose_option=DecomposeOption.RESIDUAL_PLUS_TREND)
    #
    # dataAnalyzer.compute_correlation(analyzer_option=AnalyzerOption.AVERAGE_RATING_VS_AVERAGE_TURNOVER,
    #                                  restaurant=Restaurant.NOOCH_BARFI,
    #                                  restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
    #                                  time_period='m',
    #                                  rating_date_offset_in_months=0,
    #                                  filter_corona_data=False,
    #                                  decompose_option=DecomposeOption.RESIDUAL_PLUS_TREND)

    # TODO: 1. get plots of all rest overall rating vs turnover
    # dataAnalyzer.plot_for_all_restaurants(analyzer_option=AnalyzerOption.AVERAGE_RATING_VS_AVERAGE_TURNOVER,
    #                                       restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
    #                                       time_period='m',
    #                                       rating_date_offset_in_months=0,
    #                                       filter_corona_data=False,
    #                                       decompose_option=DecomposeOption.RESIDUAL_PLUS_TREND)

    # TODO: look at correlations overall rating vs turnover
    # dataAnalyzer.compute_correlation_for_all_restaurants(
    #     analyzer_option=AnalyzerOption.AVERAGE_RATING_VS_AVERAGE_TURNOVER,
    #     restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
    #     time_period='m',
    #     rating_date_offset_in_months=0,
    #     filter_corona_data=False,
    #     decompose_option=DecomposeOption.RESIDUAL_PLUS_TREND)

    # TODO: 2. get plots of all rest average rating vs turnover
    # dataAnalyzer.plot_for_all_restaurants(analyzer_option=AnalyzerOption.AVERAGE_RATING_VS_AVERAGE_TURNOVER,
    #                                       restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
    #                                       time_period='m',
    #                                       rating_date_offset_in_months=0,
    #                                       filter_corona_data=False)

    # TODO: look at correlations average rating vs turnover
    # dataAnalyzer.compute_correlation_for_all_restaurants(
    #     analyzer_option=AnalyzerOption.AVERAGE_RATING_VS_AVERAGE_TURNOVER,
    #     restaurant_review_data_type=RestaurantReviewDataType.GOOGLE_REVIEW,
    #     time_period='m',
    #     rating_date_offset_in_months=0,
    #     filter_corona_data=False)


if __name__ == '__main__':
    main()
