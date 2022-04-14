from ba_code.data_preprocessing.tripadvisor_restaurant_data_preprocessing.tripadvisor_restaurant_data_uri import \
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


def print_overall_rating_history(restaurant_data_extractor):
    df_review_data_1 = restaurant_data_extractor.get_review_data_dataframe()

    overall_rating_history_over_time = df_review_data_1 \
        .sort_values(by='date', ascending=True)['rating'] \
        .expanding().mean().to_list()

    df_overall_rating_history_over_time_deprecated = pd.DataFrame({
        'date': df_review_data_1['date'].to_list(),
        'rating_history': overall_rating_history_over_time
    })

    print(df_overall_rating_history_over_time_deprecated.head)


tripadvisor_restaurant_data_extractor = TripadvisorRestaurantDataExtractor()
tripadvisor_restaurant_data_extractor.load_restaurant_data(open(TripadvisorRestaurantDataUri.WEISSES_ROSSLI.value))

print_infos_of_tripadvisor_restaurant_data(tripadvisor_restaurant_data_extractor)
print_overall_rating_history(tripadvisor_restaurant_data_extractor)
