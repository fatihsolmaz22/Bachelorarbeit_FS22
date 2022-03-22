from review_data_extractor import ReviewDataExtractor
from ba_code.data_preprocessing.review_data_preprocessing.review_uri import ReviewUri
import matplotlib.pyplot as plt


# TODO: not clean, code duplication (interface or superclass)
class ReviewDataAnalyzer:

    def __init__(self):
        self.__reviewDataExtractor = ReviewDataExtractor()

    def plot_rating_per_month_all_restaurants(self):
        for review_uri in ReviewUri:
            self.plot_average_rating_per_year(review_uri)

    def plot_average_rating_per_year(self, review_uri):
        df_overall_rating_per_year = self.__reviewDataExtractor \
            .get_overall_yearly_rating_for_restaurant_dataframe(review_uri)

        x = 'date'
        y = 'overall_rating_per_year'
        title = "Average rating per year"
        x_label = "year"
        y_label = "overall rating"

        self.__plot_dataframe(df_overall_rating_per_year, x, y,
                              title, x_label, y_label, review_uri)

    def __plot_dataframe(self, df, x, y, title, x_label, y_label, review_uri):
        plt.figure()
        df.plot(x=x, y=y, marker='o')
        plt.title(title + ": " + self.__reviewDataExtractor.get_restaurant_name(review_uri))
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc="upper left")
        plt.grid()
        plt.show()


restaurantDataAnalyzer = ReviewDataAnalyzer()
restaurantDataAnalyzer.plot_rating_per_month_all_restaurants()
