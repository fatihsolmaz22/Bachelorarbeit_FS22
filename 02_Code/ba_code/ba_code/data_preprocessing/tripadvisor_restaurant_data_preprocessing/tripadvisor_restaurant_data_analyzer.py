from ba_code.data_preprocessing.tripadvisor_restaurant_data_preprocessing.tripadvisor_restaurant_data_extractor import \
    TripadvisorRestaurantDataExtractor
from ba_code.data_preprocessing.tripadvisor_restaurant_data_preprocessing.review_uri import ReviewUri
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class TripadvisorRestaurantDataAnalyzer:

    def __init__(self):
        self.__tripadvisor_restaurant_data = dict()
        self.__initialize()

    def __initialize(self):
        # TODO: implement fileUtil later.. FileUtil.getFiles...
        restaurant_files = np.array([1, 2, 3, 4, 5])

        i = 0
        for restaurant_file in restaurant_files:
            tripadvisor_restaurant_data_extractor = TripadvisorRestaurantDataExtractor()
            # TODO: replace later open(ReviewUri.BUTCHER_BADENERSTRASSE.value) with open(restaurant_file)
            tripadvisor_restaurant_data_extractor.load_restaurant_data(open(ReviewUri.BUTCHER_BADENERSTRASSE.value))
            restaurant_name = tripadvisor_restaurant_data_extractor.get_restaurant_name()
            # TODO: remove i = i + 1 later
            i = i + 1
            self.__tripadvisor_restaurant_data[restaurant_name + str(i)] = tripadvisor_restaurant_data_extractor

    def plot_overall_rating_vs_overall_rating_computed(self):
        overall_ratings = []
        overall_ratings_computed = []

        for tripadvisor_restaurant_data_extractor in self.__tripadvisor_restaurant_data.values():
            overall_ratings.append(tripadvisor_restaurant_data_extractor.get_overall_rating())
            overall_ratings_computed.append(tripadvisor_restaurant_data_extractor.get_overall_rating_computed())

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

        self.__plot_dataframe(df, x, y, title, x_label, y_label)

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
