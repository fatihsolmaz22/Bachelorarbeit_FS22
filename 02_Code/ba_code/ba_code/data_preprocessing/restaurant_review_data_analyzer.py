import matplotlib.pyplot as plt
from ba_code.data_preprocessing.prognolite_restaurant_data_preprocessing.prognolite_restaurant_data_extractor import PrognoliteRestaurantDataExtractor
from ba_code.data_preprocessing.tripadvisor_restaurant_data_preprocessing.review_data_extractor import ReviewDataExtractor
from ba_code.data_preprocessing.prognolite_restaurant_data_preprocessing.restaurant_constants import RestaurantUri
from ba_code.data_preprocessing.tripadvisor_restaurant_data_preprocessing.review_uri import ReviewUri


class RestaurantReviewDataAnalyzer:

    def __init__(self):
        self.__restaurantDataExtractor = PrognoliteRestaurantDataExtractor()
        self.__reviewDataExtractor = ReviewDataExtractor()

    def plot_restaurant_rating_and_turnover(self, restaurant_uri, review_uri):
        df_restaurant_data = self.__restaurantDataExtractor.get_turnover_per_month_dataframe(restaurant_uri)
        df_review_data = self.__reviewDataExtractor.get_overall_monthly_rating_for_restaurant_dataframe(review_uri)

        # plot ###################################################################
        color = 'red'
        fig, ax1 = plt.subplots()
        ax1.set_xlabel('date')
        ax1.set_ylabel('rating', color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        df_review_data.plot(ax=ax1, color=color, marker='o')

        color = 'blue'
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        ax2.set_ylabel('turnover in CHF', color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        df_restaurant_data.plot(ax=ax2, color=color, marker='o')

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.title("Restaurant: " + self.__reviewDataExtractor.get_restaurant_name(review_uri))
        plt.legend(loc="upper left")
        plt.show()
        # plot ###################################################################"""


restaurantReviewDataAnalyzer = RestaurantReviewDataAnalyzer()
restaurantReviewDataAnalyzer.plot_restaurant_rating_and_turnover(RestaurantUri.NOOCH_BADENERSTRASSE,
                                                                 ReviewUri.NOOCH_BADENERSTRASSE)
