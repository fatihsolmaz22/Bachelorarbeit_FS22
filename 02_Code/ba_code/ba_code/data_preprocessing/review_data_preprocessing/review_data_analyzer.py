from review_data_extractor import ReviewDataExtractor
from ba_code.data_preprocessing.review_data_preprocessing.review_uri import ReviewUri
import matplotlib.pyplot as plt


# TODO: not clean, code duplication (interface or superclass)
class ReviewDataAnalyzer:

    def __init__(self):
        self.__reviewDataExtractor = ReviewDataExtractor()

    def plot_rating_per_month_all_restaurants(self):
        for review_uri in ReviewUri:
            self.plot_rating_per_month(review_uri)

    def plot_rating_per_month(self, review_uri):
        df_turnover_per_month = self.__reviewDataExtractor \
            .get_monthly_rating_for_restaurant_dataframe(review_uri)

        plt.figure()
        df_turnover_per_month.plot()
        plt.title("Rating per month: " + self.__reviewDataExtractor
                                             .get_restaurant_name(review_uri))
        plt.xlabel('month')
        plt.ylabel('rating')
        plt.legend(loc="upper left")
        plt.grid()
        plt.show()


restaurantDataAnalyzer = ReviewDataAnalyzer()
restaurantDataAnalyzer.plot_rating_per_month_all_restaurants()
