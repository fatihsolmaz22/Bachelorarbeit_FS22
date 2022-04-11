from ba_code.data_preprocessing.tripadvisor_restaurant_data_preprocessing \
    .tripadvisor_restaurant_data_extractor import TripadvisorRestaurantDataExtractor
from ba_code.utils.file_util import FileUtil
from ba_code.path import TRIPADVISOR_RESTAURANT_DATA_PATH
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


class TripadvisorRestaurantDataAnalyzer:

    def __init__(self):
        self.__tripadvisor_restaurant_data = dict()
        self.__initialize()

    def __initialize(self):
        restaurant_files = FileUtil.get_files_in_dir(TRIPADVISOR_RESTAURANT_DATA_PATH)

        for restaurant_file in restaurant_files:
            tripadvisor_restaurant_data_extractor = TripadvisorRestaurantDataExtractor()
            tripadvisor_restaurant_data_extractor.load_restaurant_data(open(restaurant_file))
            restaurant_name = tripadvisor_restaurant_data_extractor.get_restaurant_name()
            self.__tripadvisor_restaurant_data[restaurant_name] = tripadvisor_restaurant_data_extractor

    def plot_overall_rating_vs_overall_rating_computed(self):
        overall_ratings = []
        overall_ratings_computed = []

        for tripadvisor_restaurant_data_extractor in self.__tripadvisor_restaurant_data.values():
            overall_ratings.append(tripadvisor_restaurant_data_extractor.get_overall_rating())
            overall_ratings_computed.append(tripadvisor_restaurant_data_extractor.get_overall_rating_computed())

        # TODO: remove this commented out code if __plot_dataframe will not be used
        """
        df = pd.DataFrame({
            'restaurant_id': np.arange(len(self.__tripadvisor_restaurant_data)),
            'overall_ratings': overall_ratings,
            'overall_ratings_computed': overall_ratings_computed
        })
        
        x = 'restaurant_id'
        y = ['overall_ratings', 'overall_ratings_computed']
        title = 'Overall rating vs overall rating computed'
        x_label = 'restaurant id'
        y_label = 'overall rating'
        
        #self.__plot_dataframe(df, x, y, title, x_label, y_label)
        """

        df = pd.DataFrame({
            'overall_ratings': overall_ratings,
            'overall_ratings_computed': overall_ratings_computed
        })

        x = 'overall_ratings_computed'
        y = 'overall_ratings'

        self.__scatterplot_dataframe(df, x, y)

    def get_restaurant_data_extractors_where_overall_rating_not_equal_computed_one(self):
        tripadvisor_restaurant_data_extractors = []

        for tripadvisor_restaurant_data_extractor in self.__tripadvisor_restaurant_data.values():
            if (tripadvisor_restaurant_data_extractor.get_overall_rating() != tripadvisor_restaurant_data_extractor
                    .get_overall_rating_computed_and_rounded()):
                tripadvisor_restaurant_data_extractors.append(tripadvisor_restaurant_data_extractor)

        return tripadvisor_restaurant_data_extractors

    def get_tripadvisor_restaurant_data(self):
        return self.__tripadvisor_restaurant_data

    def __scatterplot_dataframe(self, df, x, y):
        plt.figure()
        sns.set_style("darkgrid")
        sns.scatterplot(data=df, x=x, y=y)
        plt.show()

    # TODO: This method may not be used in the future, remove it later
    def __plot_dataframe(self, df, x, y, title, x_label, y_label):
        plt.figure()
        df.plot(x=x, y=y, marker='o')
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc="upper left")
        plt.grid()
        plt.show()


restaurantDataAnalyzer = TripadvisorRestaurantDataAnalyzer()
restaurantDataAnalyzer.plot_overall_rating_vs_overall_rating_computed()


# TODO: check if there are duplicates
tripadvisor_restaurant_data = restaurantDataAnalyzer.get_tripadvisor_restaurant_data()
for tripadvisor_restaurant_data_extractor in tripadvisor_restaurant_data.values():
    df_review_data = tripadvisor_restaurant_data_extractor.get_review_data_dataframe()
    df_author_base_infos = tripadvisor_restaurant_data_extractor.get_author_base_infos_dataframe()
    df_author_stats = tripadvisor_restaurant_data_extractor.get_author_stats_dataframe()
    df_author_distribution = tripadvisor_restaurant_data_extractor.get_author_distribution_dataframe()
    any_duplicates = any(df_review_data.duplicated().to_list())

    contents = df_review_data.content.to_list()

    contains_more = []
    for content in contents:
        contains_more.append("...More" in content)

    any_contains_more = any(contains_more)

    print("#########################################")
    print("Restaurant name:", tripadvisor_restaurant_data_extractor.get_restaurant_name())
    print("Any duplicate in reviews:", any_duplicates)
    print("Review contains ...More:", any_contains_more)
    print("Number of entries in df_review_data", len(df_review_data.index))
    print("Number of entries in df_author_base_infos", len(df_author_base_infos))
    print("Number of entries in df_author_stats", len(df_author_stats))
    print("Number of entries in df_author_distribution", len(df_author_distribution))
