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
            df = pd.DataFrame(review_data['all_reviews'])
            df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
            self.__review_data[review_uri] = {
                'restaurant_name': review_data['restaurant_name'],
                'overall_rating': review_data['overall_rating'],
                'dataframe': df
            }

    def get_overall_monthly_rating_for_restaurant_dataframe(self, review_uri):
        df_date_rating = self.__get_date_rating_dataframe(review_uri)
        return df_date_rating.groupby(pd.Grouper(key='date', axis=0,
                                                 freq='m')).mean()

    def get_overall_yearly_rating_for_restaurant_dataframe(self, review_uri):
        df_date_rating = self.__get_date_rating_dataframe(review_uri)
        return df_date_rating.groupby(pd.Grouper(key='date', axis=0,
                                                 freq='Y')).mean()

    def __get_date_rating_dataframe(self, review_uri):
        df = self.__review_data[review_uri]['dataframe']
        return df.filter(items=["date", "rating"])

    def get_restaurant_name(self, review_uri):
        return self.__review_data[review_uri]['restaurant_name']

    def get_overall_rating(self, review_uri):
        return self.__review_data[review_uri]['overall_rating']

    def get_dataframe(self, review_uri):
        return self.__review_data[review_uri]['dataframe']
