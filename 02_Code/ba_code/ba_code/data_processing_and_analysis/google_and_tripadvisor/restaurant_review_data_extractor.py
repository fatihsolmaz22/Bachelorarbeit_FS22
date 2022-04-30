import json
import pandas as pd
import numpy as np

from ba_code.data_processing_and_analysis.google_and_tripadvisor.restaurant_review_data_uri import \
    TripadvisorRestaurantReviewDataUri, GoogleRestaurantReviewDataUri, RestaurantReviewDataType


class RestaurantReviewDataExtractor:

    def __init__(self):
        self.__restaurant_review_data = None

    def load_restaurant_review_data(self, file, restaurant_review_data_type):
        restaurant_review_data_json = json.load(file)

        restaurant_name = restaurant_review_data_json['restaurant_name']
        overall_rating = restaurant_review_data_json['overall_rating']
        reviews_count = None

        # TODO: remove try/except as soon as the reviews_count is added.
        try:
            reviews_count = restaurant_review_data_json['reviews_count']
        except KeyError:
            pass

        # extract author and review data
        all_reviews = restaurant_review_data_json['all_reviews']
        [author_base_infos, author_distribution, author_stats, review_data] = \
            self.__extract_author_and_review_data(all_reviews)

        # create author dataframes
        dfs_author_data = \
            self.__create_author_data_dataframes(author_base_infos, author_distribution, author_stats)

        # df_review_data
        df_review_data = self.__create_review_data_dataframe(review_data)

        # tripadvisor dataset contains duplicates which has to be removed
        if restaurant_review_data_type == RestaurantReviewDataType.TRIPADVISOR_REVIEW:
            # remove duplicates in dataframes
            [df_review_data, dfs_author_data] = self.__remove_duplicates_in_dataframes(df_review_data, dfs_author_data)

        self.__restaurant_review_data = {
            'restaurant_name': restaurant_name,
            'overall_rating': overall_rating,
            'reviews_count': reviews_count,
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

    def get_restaurant_review_data(self):
        return self.__restaurant_review_data

    def get_restaurant_name(self):
        return self.__restaurant_review_data['restaurant_name']

    def get_overall_rating(self):
        return self.__restaurant_review_data['overall_rating']

    def get_number_of_reviews(self):
        return self.__restaurant_review_data['reviews_count']

    def get_overall_rating_computed(self):
        review_data = self.__restaurant_review_data['df_review_data']
        return review_data['rating'].mean()

    def get_overall_rating_computed_and_rounded(self):
        overall_rating_computed = self.get_overall_rating_computed()
        overall_rating_computed_times_two = overall_rating_computed * 2

        overall_rating_computed_and_rounded = None

        if (overall_rating_computed_times_two - int(overall_rating_computed_times_two)) >= 0.5:
            overall_rating_computed_and_rounded = np.ceil(overall_rating_computed_times_two) / 2
        else:
            overall_rating_computed_and_rounded = np.floor(overall_rating_computed_times_two) / 2

        return overall_rating_computed_and_rounded

    def get_review_data_dataframe(self):
        return self.__restaurant_review_data['df_review_data']

    def get_author_base_infos_dataframe(self):
        return self.__restaurant_review_data['author_data']['df_author_base_infos']

    def get_author_stats_dataframe(self):
        return self.__restaurant_review_data['author_data']['df_author_stats']

    def get_author_distribution_dataframe(self):
        return self.__restaurant_review_data['author_data']['df_author_distribution']

    def get_incremental_overall_rating_over_years_dataframe(self):
        df_review_data = self.get_review_data_dataframe()
        df_incremental_overall_rating = pd.DataFrame({
            'date': df_review_data['date'].to_list(),
            'bygone_year': df_review_data['date']
                .apply(lambda date: np.abs(date - df_review_data.iloc[0]['date']) / np.timedelta64(1, 'Y')),
            'incremental_overall_rating': df_review_data['rating'].expanding().mean().to_list()
        })
        df_incremental_overall_rating.index.name = df_review_data.index.name

        return df_incremental_overall_rating

    def get_overall_rating_development_over_time_period_dataframe(self, time_period='m', offset_in_months=0):
        df_review_data = self.get_review_data_dataframe()

        df_review_data_with_offset_in_months = pd.DataFrame({
            'date': df_review_data['date'] + pd.DateOffset(months=offset_in_months),
            'rating': df_review_data['rating'].to_numpy()
        })

        # I use ...time_period which is a "placeholder" for: per_day, per_month, per_quarter or per_year
        # 'd' --> day, 'm' --> month, 'Q' --> quarter, 'Y' --> year
        if time_period == 'd' or time_period == 'm' or time_period == 'Q' or time_period == 'Y':
            # get number of ratings per day, month or year dataframe
            df_number_of_ratings_per_time_period = df_review_data_with_offset_in_months \
                .sort_values(by='date', ascending=True) \
                .groupby(pd.Grouper(key='date', axis=0, freq=time_period)).count()['rating'] \
                .to_frame().rename(columns={"rating": "number_of_ratings_per_time_period"}).reset_index()

            # get sum of ratings per day, month or year dataframe
            df_sum_of_ratings_per_time_period = df_review_data_with_offset_in_months \
                .sort_values(by='date', ascending=True) \
                .groupby(pd.Grouper(key='date', axis=0, freq=time_period)).sum()['rating'] \
                .to_frame().rename(columns={"rating": "sum_of_ratings_per_time_period"}).reset_index()
        else:
            self.__print_invalid_time_period_message()
            return

        # preparing data(frames) to compute overall_rating_development
        df_where_number_of_ratings_greater_zero_per_time_period = df_number_of_ratings_per_time_period[
            df_number_of_ratings_per_time_period['number_of_ratings_per_time_period'] != 0]

        dates = df_number_of_ratings_per_time_period['date'].to_list()
        dates_where_number_of_ratings_greater_zero = \
            df_where_number_of_ratings_greater_zero_per_time_period['date'].to_list()

        number_of_ratings_development = df_where_number_of_ratings_greater_zero_per_time_period[
            'number_of_ratings_per_time_period'].expanding().sum().to_list()

        df_where_sum_of_ratings_per_time_period_greater_zero = df_sum_of_ratings_per_time_period[
            df_sum_of_ratings_per_time_period['sum_of_ratings_per_time_period'] != 0]

        sum_of_ratings_development = df_where_sum_of_ratings_per_time_period_greater_zero[
            'sum_of_ratings_per_time_period'].expanding().sum().to_list()

        overall_rating_development = np.divide(sum_of_ratings_development,
                                               number_of_ratings_development)

        # initialising dictionary: The values for all dates are NaN
        date_overall_rating_development_dict = {date: np.nan for date in dates}

        # overriding some of the NaN values in dictionary with overall_rating_development
        for date, overall_rating in zip(dates_where_number_of_ratings_greater_zero, overall_rating_development):
            date_overall_rating_development_dict[date] = overall_rating

        df_overall_rating_development_since_beginning = pd.DataFrame({
            'date': date_overall_rating_development_dict.keys(),
            'overall_rating_development': date_overall_rating_development_dict.values()
        })

        # replacing NaNs with preceding overall_rating_development value in dataframe
        df_overall_rating_development_since_beginning['overall_rating_development'].fillna(method='ffill', inplace=True)

        df_overall_rating_development_since_beginning.index.name = df_review_data.index.name

        return df_overall_rating_development_since_beginning

    def get_average_rating_per_time_period_dataframe(self, time_period='m', offset_in_months=0):
        df_review_data = self.get_review_data_dataframe()

        df_review_data_with_offset_in_months = pd.DataFrame({
            'date': df_review_data['date'] + pd.DateOffset(months=offset_in_months),
            'rating': df_review_data['rating'].to_numpy()
        })

        df_average_rating_per_time_period = df_review_data_with_offset_in_months \
            .sort_values(by='date', ascending=True) \
            .groupby(pd.Grouper(key='date', axis=0, freq=time_period)).mean()['rating'] \
            .to_frame().rename(columns={"rating": "average_rating_per_time_period"}).reset_index()

        return df_average_rating_per_time_period

    def __print_invalid_time_period_message(self):
        print("Invalid time period, enter one of the following time periods:")
        print("'d': Day")
        print("'m': Month")
        print("'Q': Quarter")
        print("'Y': Year")

    def get_author_level_with_rating_dataframe(self):
        df_author_base_infos = self.get_author_base_infos_dataframe()
        df_review_data = self.get_review_data_dataframe()

        df_author_level_with_rating = pd.DataFrame({
            'author_level': df_author_base_infos['author_level'].to_numpy(),
            'rating': df_review_data['rating'].to_numpy()
        })
        df_author_level_with_rating.index.name = df_author_base_infos.index.name

        return df_author_level_with_rating


restaurantReviewDataExtractor = RestaurantReviewDataExtractor()
"""
restaurantReviewDataExtractor.load_restaurant_review_data(open(TripadvisorRestaurantReviewDataUri.BUTCHER_USTER.value),
                                                          RestaurantReviewDataType.TRIPADVISOR_REVIEW)
restaurantReviewDataExtractor.load_restaurant_review_data(open(GoogleRestaurantReviewDataUri.BUTCHER_USTER.value),
                                                          RestaurantReviewDataType.GOOGLE_REVIEW)
"""