from ba_code.data_preprocessing.tripadvisor_restaurant_data_preprocessing \
    .tripadvisor_restaurant_data_extractor import TripadvisorRestaurantDataExtractor
from ba_code.utils.file_util import FileUtil
from ba_code.path import TRIPADVISOR_RESTAURANT_DATA_PATH
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.font_manager import FontProperties
from ba_code.data_preprocessing.prognolite_restaurant_data_preprocessing.prognolite_restaurant_constants import \
    Restaurant

fontP = FontProperties()
fontP.set_size('x-small')


class TripadvisorRestaurantDataAnalyzer:

    def __init__(self):
        self.__tripadvisor_restaurant_data_extractors = dict()
        self.__initialize()

    def __initialize(self):
        restaurant_files = FileUtil.get_files_in_dir(TRIPADVISOR_RESTAURANT_DATA_PATH)

        for restaurant_file in restaurant_files:
            tripadvisor_restaurant_data_extractor = TripadvisorRestaurantDataExtractor()
            tripadvisor_restaurant_data_extractor.load_restaurant_data(open(restaurant_file))
            restaurant_name = tripadvisor_restaurant_data_extractor.get_restaurant_name()
            self.__tripadvisor_restaurant_data_extractors[restaurant_name] = tripadvisor_restaurant_data_extractor

    def scatterplot_overall_rating_vs_overall_rating_computed(self):
        overall_ratings = []
        overall_ratings_computed = []
        overall_ratings_computed_and_rounded = []

        for tripadvisor_restaurant_data_extractor in self.__tripadvisor_restaurant_data_extractors.values():
            overall_ratings.append(tripadvisor_restaurant_data_extractor.get_overall_rating())
            overall_ratings_computed.append(tripadvisor_restaurant_data_extractor.get_overall_rating_computed())
            overall_ratings_computed_and_rounded.append(tripadvisor_restaurant_data_extractor
                                                        .get_overall_rating_computed_and_rounded())

        df = pd.DataFrame({
            'overall_rating': overall_ratings,
            'overall_rating_computed': overall_ratings_computed,
            'overall_rating_computed_and_rounded': overall_ratings_computed_and_rounded
        })

        x1 = 'overall_rating_computed'
        x2 = 'overall_rating_computed_and_rounded'
        y = 'overall_rating'

        self.__scatterplot_dataframe(df, x1, y)
        self.__scatterplot_dataframe(df, x2, y)

    def __scatterplot_dataframe(self, df, x, y):
        vertical_line_positions = np.arange(1.25, 5, 0.5)
        min_overall_rating_computed = df[x].to_numpy().min()
        vertical_line_positions = vertical_line_positions[vertical_line_positions > min_overall_rating_computed]

        plt.figure()
        sns.set_style("darkgrid")
        sns.scatterplot(data=df, x=x, y=y)
        for vertical_line_position in vertical_line_positions:
            plt.axvline(x=vertical_line_position, color='r', linestyle='dashed', label='overall_rating')
        plt.show()

    def plot_incremental_overall_rating_for_all_restaurants(self):
        for restaurant_name in self.__tripadvisor_restaurant_data_extractors.keys():
            self.plot_incremental_overall_rating_for_restaurant(restaurant_name)

    def plot_incremental_overall_rating_for_restaurant(self, restaurant_name):
        tripadvisor_restaurant_data_extractor = self.__tripadvisor_restaurant_data_extractors[restaurant_name]

        df_incremental_overall_rating = \
            tripadvisor_restaurant_data_extractor.get_incremental_overall_rating_over_years_dataframe()

        x = 'bygone_year'
        y = ['incremental_overall_rating']
        title = 'Incremental overall rating for ' + restaurant_name
        x_label = 'bygone years'
        y_label = 'overall rating'

        y_min = df_incremental_overall_rating[y].to_numpy().min()
        y_max = df_incremental_overall_rating[y].to_numpy().max()

        overall_rating = tripadvisor_restaurant_data_extractor.get_overall_rating()
        y_min = overall_rating if overall_rating < y_min else y_min

        plt.figure()
        df_incremental_overall_rating.plot(x=x, y=y)
        plt.axhline(y=overall_rating - 0.25, color='r', linestyle='dashed', label='lower_bound')
        plt.axhline(y=overall_rating, color='g', linestyle='dashed', label='overall_rating')
        plt.axhline(y=overall_rating + 0.25, color='r', linestyle='dashed', label='upper_bound')
        plt.ylim([y_min - 0.05, y_max + 0.05])
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc='upper right', prop=fontP)
        plt.grid()
        plt.show()

    def plot_average_rating_per_time_period_for_all_restaurants(self, time_period='m'):
        for restaurant_name in self.__tripadvisor_restaurant_data_extractors.keys():
            self.plot_average_rating_per_time_period(restaurant_name, time_period)

    def plot_average_rating_per_time_period(self, restaurant_name, time_period='m'):
        tripadvisor_restaurant_data_extractor = self.__tripadvisor_restaurant_data_extractors[restaurant_name]

        df_average_rating_per_time_period = \
            tripadvisor_restaurant_data_extractor.get_average_rating_per_time_period_dataframe(time_period)

        title = "Average rating per time period: " + restaurant_name
        x = 'date'
        y = 'average_rating_per_time_period'
        x_label = self.__get_x_label(time_period)
        y_label = 'rating'

        plt.figure()
        df_average_rating_per_time_period.plot(x=x, y=y)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc='upper right', prop=fontP)
        plt.grid()
        plt.show()

    def boxplot_overall_rating_computed_by_overall_rating(self):
        overall_ratings = []
        overall_ratings_computed = []

        for tripadvisor_restaurant_data_extractor in self.__tripadvisor_restaurant_data_extractors.values():
            overall_ratings.append(tripadvisor_restaurant_data_extractor.get_overall_rating())
            overall_ratings_computed.append(tripadvisor_restaurant_data_extractor.get_overall_rating_computed())

        df = pd.DataFrame({
            'overall_rating': overall_ratings,
            'overall_rating_computed': overall_ratings_computed,
        })

        plt.figure()
        sns.boxplot(data=df,
                    x='overall_rating',
                    y="overall_rating_computed",
                    width=0.5)

        sns.stripplot(data=df,
                      x='overall_rating',
                      y="overall_rating_computed",
                      jitter=True,
                      marker='o',
                      alpha=0.5,
                      color='black')

        plt.title("Boxplot of overall_rating_computed by overall_rating")
        plt.legend(loc='lower right', prop=fontP)
        plt.show()

    def boxplot_of_rating_by_author_level_for_all_restaurants(self):
        for restaurant_name in self.__tripadvisor_restaurant_data_extractors.keys():
            self.boxplot_of_rating_by_author_level_for_restaurant(restaurant_name)

    def boxplot_of_rating_by_author_level_for_restaurant(self, restaurant_name):
        tripadvisor_restaurant_data_extractor = self.__tripadvisor_restaurant_data_extractors[restaurant_name]
        df_author_level_with_rating = tripadvisor_restaurant_data_extractor.get_author_level_with_rating_dataframe()

        overall_rating = tripadvisor_restaurant_data_extractor.get_overall_rating()
        overall_rating_computed = tripadvisor_restaurant_data_extractor.get_overall_rating_computed()

        if df_author_level_with_rating['author_level'].isnull().values.any():
            df_author_level_with_rating = df_author_level_with_rating[
                ~df_author_level_with_rating['author_level'].isnull()]

        plt.figure()
        sns.boxplot(data=df_author_level_with_rating,
                    x="author_level",
                    y="rating",
                    width=0.5)

        sns.stripplot(data=df_author_level_with_rating,
                      x="author_level",
                      y="rating",
                      jitter=True,
                      marker='o',
                      alpha=0.5,
                      color='black')

        plt.axhline(y=overall_rating, color='g', linestyle='dashed', label='overall_rating')
        plt.axhline(y=overall_rating_computed, color='r', linestyle='dashed', label='overall_rating_computed')

        plt.title("Boxplot of rating by author level for " + restaurant_name)
        plt.legend(loc='lower right', prop=fontP)
        plt.show()

    def get_restaurant_data_extractors_where_overall_rating_not_equal_computed_and_rounded_one(self):
        tripadvisor_restaurant_data_extractors = []

        for tripadvisor_restaurant_data_extractor in self.__tripadvisor_restaurant_data_extractors.values():
            if (tripadvisor_restaurant_data_extractor.get_overall_rating() != tripadvisor_restaurant_data_extractor
                    .get_overall_rating_computed_and_rounded()):
                tripadvisor_restaurant_data_extractors.append(tripadvisor_restaurant_data_extractor)

        return tripadvisor_restaurant_data_extractors

    def inspection_of_freshness_based_average_rating(self):
        # TODO: Fatih
        pass

    def get_tripadvisor_restaurant_data_extractors(self):
        return self.__tripadvisor_restaurant_data_extractors

    def get_restaurant_names(self):
        return self.__tripadvisor_restaurant_data_extractors.keys()

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


tripadvisorRestaurantDataAnalyzer = TripadvisorRestaurantDataAnalyzer()
# tripadvisorRestaurantDataAnalyzer.plot_average_rating_per_time_period('BUTCHER_USTER', 'Q')
