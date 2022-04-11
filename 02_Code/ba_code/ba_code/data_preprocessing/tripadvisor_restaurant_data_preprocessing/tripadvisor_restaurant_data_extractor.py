import json
import pandas as pd
import numpy as np
from ba_code.data_preprocessing.tripadvisor_restaurant_data_preprocessing.tripadvisor_restaurant_data_uri import \
    TripadvisorRestaurantDataUri


class TripadvisorRestaurantDataExtractor:

    def __init__(self):
        self.__tripadvisor_restaurant_data = None

    def load_restaurant_data(self, file):
        tripadvisor_restaurant_data_json = json.load(file)

        restaurant_name = tripadvisor_restaurant_data_json['restaurant_name']
        overall_rating = tripadvisor_restaurant_data_json['overall_rating']

        # extract author and review data
        all_reviews = tripadvisor_restaurant_data_json['all_reviews']
        [author_base_infos, author_distribution, author_stats, review_data] = \
            self.__extract_author_and_review_data(all_reviews)

        # create author dataframes
        dfs_author_data = \
            self.__create_author_data_dataframes(author_base_infos, author_distribution, author_stats)

        # df_review_data
        df_review_data = self.__create_review_data_dataframe(review_data)

        # remove duplicates in dataframes
        [df_review_data, dfs_author_data] = self.__remove_duplicates_in_dataframes(df_review_data, dfs_author_data)

        self.__tripadvisor_restaurant_data = {
            'restaurant_name': restaurant_name,
            'overall_rating': overall_rating,
            'author_data': {
                'df_author_base_infos': dfs_author_data[0],
                'df_author_stats': dfs_author_data[1],
                'df_author_distribution': dfs_author_data[2],
            },
            'df_review_data': df_review_data,
        }

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

    def __create_author_data_dataframes(self, author_base_infos, author_distribution, author_stats):
        # df_author_base_infos, TODO: Fatih maybe you should extract the exact date
        df_author_base_infos = pd.DataFrame(author_base_infos)
        df_author_base_infos['author_member_since'] = pd.to_datetime(df_author_base_infos['author_member_since'],
                                                                     format='%Y')
        # df_author_stats
        df_author_stats = pd.DataFrame(author_stats)
        # df_author_distribution
        df_author_distribution = pd.DataFrame(author_distribution)

        return [df_author_base_infos, df_author_distribution, df_author_stats]

    def __create_review_data_dataframe(self, review_data):
        df_review_data = pd.DataFrame(review_data)
        df_review_data['date'] = pd.to_datetime(df_review_data['date'], format='%d-%m-%Y')

        return df_review_data

    def __remove_duplicates_in_dataframes(self, df_review_data, dfs_author_data):
        no_duplicates = [not duplicate for duplicate in df_review_data.duplicated().to_list()]
        df_review_data = df_review_data[no_duplicates].reset_index(drop=True)
        df_review_data.index.name = 'review_id'

        dfs_author_data_without_duplicates = []
        for df_author_data in dfs_author_data:
            df_author_data = df_author_data[no_duplicates].reset_index(drop=True)
            df_author_data.index.name = 'author_id'
            dfs_author_data_without_duplicates.append(df_author_data)

        return [df_review_data, dfs_author_data_without_duplicates]

    def get_tripadvisor_restaurant_data(self):
        return self.__tripadvisor_restaurant_data

    def get_restaurant_name(self):
        return self.__tripadvisor_restaurant_data['restaurant_name']

    def get_overall_rating(self):
        return self.__tripadvisor_restaurant_data['overall_rating']

    def get_overall_rating_computed(self):
        review_data = self.__tripadvisor_restaurant_data['df_review_data']
        return review_data['rating'].mean()

    def get_overall_rating_computed_and_rounded(self):
        overall_rating_computed = self.get_overall_rating_computed()
        return np.round(overall_rating_computed * 2) / 2

    def get_review_data_dataframe(self):
        return self.__tripadvisor_restaurant_data['df_review_data']

    def get_author_base_infos_dataframe(self):
        return self.__tripadvisor_restaurant_data['author_data']['df_author_base_infos']

    def get_author_stats_dataframe(self):
        return self.__tripadvisor_restaurant_data['author_data']['df_author_stats']

    def get_author_distribution_dataframe(self):
        return self.__tripadvisor_restaurant_data['author_data']['df_author_distribution']

"""
tripadvisor_restaurant_data_extractor = TripadvisorRestaurantDataExtractor()
tripadvisor_restaurant_data_extractor.load_restaurant_data(
    open(TripadvisorRestaurantDataUri.DIFFERENTE_HOTEL_KRONE.value))


df_review_data = tripadvisor_restaurant_data_extractor.get_review_data_dataframe()
#df_review_data.iloc[1000:1013]
#df_review_data.iloc[1004]
#df_review_data.iloc[1012]

contents = df_review_data.content.to_list()

contains_more = []
for content in contents:
    contains_more.append("...More" in content)

contains_more = any(contains_more)



df_review_data = tripadvisor_restaurant_data_extractor.get_review_data_dataframe()
df_author_base_infos = tripadvisor_restaurant_data_extractor.get_author_base_infos_dataframe()
df_author_stats = tripadvisor_restaurant_data_extractor.get_author_stats_dataframe()
df_author_distribution = tripadvisor_restaurant_data_extractor.get_author_distribution_dataframe()
any_duplicates = any(df_review_data.duplicated().to_list())

print("Restaurant name:", tripadvisor_restaurant_data_extractor.get_restaurant_name())
print("Any duplicate in reviews:", any_duplicates)
print("Number of entries in df_review_data", len(df_review_data.index))
print("Number of entries in df_author_base_infos", len(df_author_base_infos))
print("Number of entries in df_author_stats", len(df_author_stats))
print("Number of entries in df_author_distribution", len(df_author_distribution))"""
