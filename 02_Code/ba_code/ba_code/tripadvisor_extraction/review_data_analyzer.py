import json
import pandas as pd
import matplotlib.pyplot as plt
from ba_code.tripadvisor_extraction.tripadvisor_strings import RestaurantURLs
from ba_code.restaurant_data_preprocessing.restaurant_data_extractor import RestaurantDataExtractor
from ba_code.restaurant_data_preprocessing.restaurant_uri import RestaurantUri

class ReviewDataAnalyzer:

    # def __init__(self):
    #     df = pd.read_json("../../resources/review_data/tripadvisor_review_data_NOOCH_STEINFELS.json")
    #     print(df.head(5))

    def get_monthly_rating_dataframe_for_restaurant(self, restaurant_enum):
        template = "../../resources/review_data/tripadvisor_review_data_{}.json"
        path_to_restaurant_json = template.format(restaurant_enum.name)
        df = pd.read_json(path_to_restaurant_json)
        df = df.filter(items=["date", "rating"])
        return df.groupby(["date"]).mean()

def main():
    review_data_analyzer = ReviewDataAnalyzer()
    df_review_data = review_data_analyzer.get_monthly_rating_dataframe_for_restaurant(RestaurantURLs.NOOCH_BADENERSTRASSE)

    restaurant_data_extractor = RestaurantDataExtractor()
    df_restaurant_data = restaurant_data_extractor.get_turnover_per_month_dataframe(RestaurantUri.NOOCH_BADENERSTRASSE)

    print(df_review_data.head(5))

    plt.figure(1)
    df_review_data.plot()
    plt.show()

    plt.figure(2)
    df_restaurant_data.plot()
    plt.show()

if __name__ == '__main__':
    main()