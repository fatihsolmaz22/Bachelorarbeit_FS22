import pandas as pd
from ba_code.data_preprocessing.review_data_preprocessing.review_uri import ReviewUri
import json


class ReviewDataExtractor:

    def __init__(self):
        self.__review_data = dict()
        self.__load_review_data()

    def __load_review_data(self):
        for review_uri in ReviewUri:
            review_data = json.load(open(review_uri.value))
            # TODO: Tell Fatih to store json differently [0]
            restaurant_name = review_data[0]['restaurant_name']
            overall_rating = review_data[0]['overall_rating']
            df = pd.DataFrame(review_data[0]['all_reviews'])
            df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

            self.__review_data[review_uri] = {
                'restaurant_name': restaurant_name,
                'overall_rating': overall_rating,
                'dataframe': df
            }

    def get_monthly_rating_for_restaurant_dataframe(self, review_uri):
        df = self.__review_data[review_uri]['dataframe']
        df = df.filter(items=["date", "rating"])
        return df.groupby(pd.Grouper(key='date', axis=0,
                                     freq='m')).mean().fillna(0)

    def get_restaurant_name(self, review_uri):
        return self.__review_data[review_uri]['restaurant_name']

    def get_overall_rating(self, review_uri):
        return self.__review_data[review_uri]['overall_rating']

    def get_dataframe(self, review_uri):
        return self.__review_data[review_uri]['dataframe']


