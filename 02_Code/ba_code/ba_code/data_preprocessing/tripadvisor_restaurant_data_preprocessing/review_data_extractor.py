import pandas as pd
from ba_code.data_preprocessing.tripadvisor_restaurant_data_preprocessing.review_uri import ReviewUri
import json


# TODO: this file is deprecated
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

    def get_overall_yearly_rating_for_restaurant_dataframe(self, review_uri):
        df_date_rating = self.__get_date_rating_dataframe(review_uri)

        df_cumsum_of_ratings_over_years = \
            self.__get_cumsum_of_ratings_over_years_dataframe(df_date_rating)
        df_cumsum_of_number_of_ratings_per_year = \
            self.__get_cumsum_of_number_of_ratings_per_year_dataframe(df_date_rating)

        df_joined = pd.concat([df_cumsum_of_ratings_over_years,
                               df_cumsum_of_number_of_ratings_per_year['cumsum_of_number_of_ratings_over_years']],
                              axis=1)

        # extract date and overall rating per year
        date = df_joined['date']
        overall_rating_per_year = \
            df_joined["cumsum_of_ratings_over_years"] / df_joined["cumsum_of_number_of_ratings_over_years"]

        # creating new dataframe with date and overall_rating
        data = {'date': date,
                'overall_rating_per_year': overall_rating_per_year}
        return pd.DataFrame(data, columns=['date', 'overall_rating_per_year'])

    def __get_cumsum_of_ratings_over_years_dataframe(self, df_date_rating):
        df_sum_of_ratings_per_year = df_date_rating.groupby(pd.Grouper(key='date', axis=0, freq='Y')).sum()
        df_cumsum_of_ratings_over_years = df_sum_of_ratings_per_year.groupby(df_sum_of_ratings_per_year.index.month) \
            .cumsum().reset_index() \
            .rename(columns={"rating": "cumsum_of_ratings_over_years"})
        return df_cumsum_of_ratings_over_years

    def __get_cumsum_of_number_of_ratings_per_year_dataframe(self, df_date_rating):
        df_number_of_ratings_per_year = df_date_rating.groupby(pd.Grouper(key='date', axis=0, freq='Y')).count()
        df_cumsum_of_number_of_ratings_per_year = df_number_of_ratings_per_year.groupby(
            df_number_of_ratings_per_year.index.month) \
            .cumsum().reset_index() \
            .rename(columns={"rating": "cumsum_of_number_of_ratings_over_years"})
        return df_cumsum_of_number_of_ratings_per_year

    def __get_date_rating_dataframe(self, review_uri):
        df = self.__review_data[review_uri]['dataframe']
        return df.filter(items=["date", "rating"])

    # TODO: not correct the way this is implemented
    def get_overall_monthly_rating_for_restaurant_dataframe(self, review_uri):
        df_date_rating = self.__get_date_rating_dataframe(review_uri)
        return df_date_rating.groupby(pd.Grouper(key='date', axis=0,
                                                 freq='m')).mean()

    def get_restaurant_name(self, review_uri):
        return self.__review_data[review_uri]['restaurant_name']

    def get_overall_rating(self, review_uri):
        return self.__review_data[review_uri]['overall_rating']

    def get_dataframe(self, review_uri):
        return self.__review_data[review_uri]['dataframe']
