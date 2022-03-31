import json
import pandas as pd
from ba_code.data_preprocessing.review_data_preprocessing.review_uri import ReviewUri


class TripAdvisorRestaurantDataExtractor:

    def __init__(self):
        self.__tripadvisor_restaurant_data = None

    def load_restaurant_data(self, file):
        tripadvisor_restaurant_data = json.load(file)

        restaurant_name = tripadvisor_restaurant_data['restaurant_name']
        overall_rating = tripadvisor_restaurant_data['overall_rating']

        # extract author and review data
        all_reviews = tripadvisor_restaurant_data['all_reviews']
        [author_base_infos, author_distribution, author_stats, review_data] = \
            self.__extract_author_and_review_data(all_reviews)

        # create dataframes
        [df_author_base_infos, df_author_distribution, df_author_stats] = \
            self.__create_author_data_dataframes(author_base_infos, author_distribution, author_stats)

        # df_review_data
        df_review_data = self.__create_review_data_dataframe(review_data)

        self.__tripadvisor_restaurant_data = {
            'restaurant_name': restaurant_name,
            'overall_rating': overall_rating,
            'author_data': {
                'df_author_base_infos': df_author_base_infos,
                'df_author_stats': df_author_stats,
                'df_author_distribution': df_author_distribution,
            },
            'df_review_data': df_review_data,
        }

    def __create_author_data_dataframes(self, author_base_infos, author_distribution, author_stats):
        author_index_name = 'author_id'
        # df_author_base_infos, TODO: Fatih maybe you should extract the exact date
        df_author_base_infos = pd.DataFrame(author_base_infos)
        df_author_base_infos['author_member_since'] = pd.to_datetime(df_author_base_infos['author_member_since'],
                                                                     format='%Y')
        df_author_base_infos.index.name = author_index_name
        # df_author_stats
        df_author_stats = pd.DataFrame(author_stats)
        df_author_stats.index.name = author_index_name
        # df_author_distribution
        df_author_distribution = pd.DataFrame(author_distribution)
        df_author_distribution.index.name = author_index_name

        return [df_author_base_infos, df_author_distribution, df_author_stats]

    def __create_review_data_dataframe(self, review_data):
        df_review_data = pd.DataFrame(review_data)
        df_review_data['date'] = pd.to_datetime(df_review_data['date'], format='%d-%m-%Y')
        df_review_data.index.name = 'review_id'

        return df_review_data

    def __extract_author_and_review_data(self, all_reviews):
        author_base_infos = []
        author_stats = []
        author_distributions = []
        review_data = []

        for review in all_reviews:
            author_data = review['author_data']
            author_base_infos.append({
                'author_level': author_data['author_level'],
                'author_member_since': author_data['author_member_since']
            })
            author_stats.append(author_data['author_stats'])
            author_distributions.append(author_data['author_distribution'])

            review_data.append(review['review_data'])

        return [author_base_infos, author_stats, author_distributions, review_data]

    def get_tripadvisor_restaurant_data(self):
        return self.__tripadvisor_restaurant_data

    def get_restaurant_name(self):
        return self.__tripadvisor_restaurant_data['restaurant_name']

    def get_overall_rating(self):
        return self.__tripadvisor_restaurant_data['overall_rating']

    def get_computed_overall_rating(self):
        review_data = self.__tripadvisor_restaurant_data['df_review_data']
        return review_data['rating'].mean()

"""
# Opening JSON file
tripAdvisorRestaurantDataExtractor = TripAdvisorRestaurantDataExtractor()
f = open(ReviewUri.BUTCHER_BADENERSTRASSE.value)
tripAdvisorRestaurantDataExtractor.load_restaurant_data(f)
"""

