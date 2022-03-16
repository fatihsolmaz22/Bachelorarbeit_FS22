import pandas as pd
import matplotlib.pyplot as plt
from ba_code.data_preprocessing.restaurant_data.restaurant_data_extractor import RestaurantDataExtractor
from ba_code.data_preprocessing.restaurant_data.restaurant_uri import RestaurantUri
from ba_code.data_preprocessing.review_data.review_uri import ReviewUri


class ReviewDataAnalyzer:

    # def __init__(self):
    #     df = pd.read_json("../../resources/review_data/tripadvisor_review_data_NOOCH_STEINFELS.json")
    #     print(df.head(5))

    def get_monthly_rating_dataframe_for_restaurant(self, review_uri):
        template = "../../../resources/review_data/tripadvisor_review_data_{}.json"
        path_to_restaurant_json = template.format(review_uri.name)
        df = pd.read_json(path_to_restaurant_json)
        df = df.filter(items=["date", "rating"])
        return df.groupby(pd.Grouper(key='date', axis=0,
                                     freq='m')).mean().fillna(0)


def main():
    review_data_analyzer = ReviewDataAnalyzer()
    df_review_data = review_data_analyzer.get_monthly_rating_dataframe_for_restaurant(
        ReviewUri.NOOCH_BADENERSTRASSE)

    restaurant_data_extractor = RestaurantDataExtractor()
    df_restaurant_data = restaurant_data_extractor.get_turnover_per_month_dataframe(RestaurantUri.NOOCH_BADENERSTRASSE)

    print(df_review_data.head(5))
    print(df_restaurant_data.head(5))

    # plot ###################################################################
    color = 'red'
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('date ')
    ax1.set_ylabel('rating', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    df_review_data.plot(ax=ax1, color=color)

    color = 'blue'
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    ax2.set_ylabel('turnover in CHF', color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    df_restaurant_data.plot(ax=ax2, color=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.legend(loc="upper left")
    plt.show()
    # plot ###################################################################"""

if __name__ == '__main__':
    main()
