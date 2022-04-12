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

    def get_incremental_overall_rating_dataframe(self):
        df_review_data = self.get_review_data_dataframe()
        df_incremental_overall_rating = pd.DataFrame({
            'date': df_review_data['date'].to_list(),
            'incremental_overall_rating': df_review_data['rating'].expanding().mean().to_list()
        })
        df_incremental_overall_rating.index.name = df_review_data.index.name

        return df_incremental_overall_rating

    def get_monthly_incremental_overall_rating_dataframe(self):
        df_review_data = self.get_review_data_dataframe()

        [dates, monthly_incremental_number_of_ratings] = self.__get_dates_and_monthly_incremental_number_of_ratings(
            df_review_data)

        monthly_incremental_sum_of_ratings = self.__get_monthly_incremental_sum_of_ratings(df_review_data)

        df_monthly_incremental_overall_rating = pd.DataFrame({
            'date': dates,
            'monthly_incremental_overall_rating': np.divide(monthly_incremental_sum_of_ratings,
                                                            monthly_incremental_number_of_ratings)
        })
        df_monthly_incremental_overall_rating.index.name = df_review_data.index.name

        return df_monthly_incremental_overall_rating

    def __get_dates_and_monthly_incremental_number_of_ratings(self, df_review_data):
        df_number_of_ratings_per_month = df_review_data \
            .groupby(pd.Grouper(key='date', axis=0, freq='m')).count()['rating'] \
            .to_frame().rename(columns={"rating": "number_of_ratings_over_months"}).reset_index() \
            .sort_values(by='date', ascending=False)

        df_date_number_of_ratings = df_number_of_ratings_per_month[
            df_number_of_ratings_per_month['number_of_ratings_over_months'] != 0]

        dates = df_date_number_of_ratings['date'].to_list()
        monthly_incremental_number_of_ratings = df_date_number_of_ratings['number_of_ratings_over_months'] \
            .expanding().sum().to_list()

        return [dates, monthly_incremental_number_of_ratings]

    def __get_monthly_incremental_sum_of_ratings(self, df_review_data):
        df_sum_of_ratings_per_month = df_review_data \
            .groupby(pd.Grouper(key='date', axis=0, freq='m')).sum()['rating'] \
            .to_frame().rename(columns={"rating": "sum_of_ratings_per_months"}).reset_index() \
            .sort_values(by='date', ascending=False)

        df_date_sum_of_ratings = df_sum_of_ratings_per_month[
            df_sum_of_ratings_per_month['sum_of_ratings_per_months'] != 0]

        monthly_incremental_sum_of_ratings = df_date_sum_of_ratings['sum_of_ratings_per_months'] \
            .expanding().sum().to_list()

        return monthly_incremental_sum_of_ratings


tripadvisorRestaurantDataExtractor = TripadvisorRestaurantDataExtractor()
tripadvisorRestaurantDataExtractor.load_restaurant_data(open(TripadvisorRestaurantDataUri.KHUJUG_ZURICH.value))
