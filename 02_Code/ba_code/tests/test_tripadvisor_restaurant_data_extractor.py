from ba_code.data_preprocessing.tripadvisor_restaurant_data_preprocessing.restaurant_data_uri import \
    TripadvisorRestaurantDataUri
from ba_code.data_preprocessing.tripadvisor_restaurant_data_preprocessing.tripadvisor_restaurant_data_extractor import \
    TripadvisorRestaurantDataExtractor
import pandas as pd


def print_infos_of_tripadvisor_restaurant_data(restaurant_data_extractor):
    df_review_data = restaurant_data_extractor.get_review_data_dataframe()
    contents = df_review_data.content.to_list()

    contains_more = []
    for content in contents:
        contains_more.append("...More" in content)

    contains_more = any(contains_more)

    df_review_data = restaurant_data_extractor.get_review_data_dataframe()
    df_author_base_infos = restaurant_data_extractor.get_author_base_infos_dataframe()
    df_author_stats = restaurant_data_extractor.get_author_stats_dataframe()
    df_author_distribution = restaurant_data_extractor.get_author_distribution_dataframe()
    any_duplicates = any(df_review_data.duplicated().to_list())

    print("Restaurant name:", restaurant_data_extractor.get_restaurant_name())
    print("Review contains any duplicate:", any_duplicates)
    print("Review contains ...More:", contains_more)
    print("Number of entries in df_review_data", len(df_review_data.index))
    print("Number of entries in df_author_base_infos", len(df_author_base_infos))
    print("Number of entries in df_author_stats", len(df_author_stats))
    print("Number of entries in df_author_distribution", len(df_author_distribution))

def test_get_average_rating_per_time_period_dataframe_offset_in_months(restaurant_data_extractor):
    df_average_rating_per_month = \
        restaurant_data_extractor.get_average_rating_per_time_period_dataframe('m', offset_in_months=0)

    print("df_average_rating_per_month\n", df_average_rating_per_month.head(5))

    df_average_rating_per_month_minus_2 = \
        restaurant_data_extractor.get_average_rating_per_time_period_dataframe('m', offset_in_months=-2)

    print("df_average_rating_per_month_minus_2\n", df_average_rating_per_month_minus_2.head(5))

    df_average_rating_per_month_minus_1 = \
        restaurant_data_extractor.get_average_rating_per_time_period_dataframe('m', offset_in_months=-1)

    print("df_average_rating_per_month_minus_1\n", df_average_rating_per_month_minus_1.head(5))

    df_average_rating_per_month_plus_1 = \
        restaurant_data_extractor.get_average_rating_per_time_period_dataframe('m', offset_in_months=1)

    print("df_average_rating_per_month_plus_1\n", df_average_rating_per_month_plus_1.head(5))

    df_average_rating_per_month_plus_2 = \
        restaurant_data_extractor.get_average_rating_per_time_period_dataframe('m', offset_in_months=2)

    print("df_average_rating_per_month_plus_2\n", df_average_rating_per_month_plus_2.head(5))

tripadvisor_restaurant_data_extractor = TripadvisorRestaurantDataExtractor()
tripadvisor_restaurant_data_extractor.load_restaurant_data(open(TripadvisorRestaurantDataUri.BUTCHER_USTER.value))

print_infos_of_tripadvisor_restaurant_data(tripadvisor_restaurant_data_extractor)
test_get_average_rating_per_time_period_dataframe_offset_in_months(tripadvisor_restaurant_data_extractor)
