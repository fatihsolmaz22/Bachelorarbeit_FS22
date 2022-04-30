from ba_code.data_processing_and_analysis.google_and_tripadvisor.restaurant_review_data_analyzer import \
    RestaurantReviewDataAnalyzer
from ba_code.path import TRIPADVISOR_RESTAURANT_DATA_PATH, TRIPADVISOR_RESTAURANT_ONLY_RATING_DATASET_PATH, \
    TRIPADVISOR_RESTAURANT_GOOGLE_DATASET_PATH
from ba_code.data_processing_and_analysis.google_and_tripadvisor.restaurant_review_data_uri import \
    RestaurantReviewDataType


def print_infos_of_tripadvisor_restaurant_data_of_all_restaurants():
    path = TRIPADVISOR_RESTAURANT_DATA_PATH
    data_type = RestaurantReviewDataType.TRIPADVISOR_REVIEW
    restaurant_review_data_analyzer = RestaurantReviewDataAnalyzer(path, data_type)

    tripadvisor_restaurant_data_extractors = restaurant_review_data_analyzer.get_restaurant_review_data_extractors()

    for tripadvisor_restaurant_data_extractor in tripadvisor_restaurant_data_extractors.values():
        df_review_data = tripadvisor_restaurant_data_extractor.get_review_data_dataframe()
        df_author_base_infos = tripadvisor_restaurant_data_extractor.get_author_base_infos_dataframe()
        df_author_stats = tripadvisor_restaurant_data_extractor.get_author_stats_dataframe()
        df_author_distribution = tripadvisor_restaurant_data_extractor.get_author_distribution_dataframe()
        any_duplicates = any(df_review_data.duplicated().to_list())

        contents = df_review_data.content.to_list()

        contains_more = []
        for content in contents:
            contains_more.append("...More" in content)

        any_contains_more = any(contains_more)

        print("\n#########################################")
        print("Restaurant name:", tripadvisor_restaurant_data_extractor.get_restaurant_name())
        print("Any duplicate in reviews:", any_duplicates)
        print("Review contains ...More:", any_contains_more)
        print("Number of entries in df_review_data", len(df_review_data.index))
        print("Number of entries in df_author_base_infos", len(df_author_base_infos))
        print("Number of entries in df_author_stats", len(df_author_stats))
        print("Number of entries in df_author_distribution", len(df_author_distribution))

def test_google_review_data_type():
    path = TRIPADVISOR_RESTAURANT_GOOGLE_DATASET_PATH
    data_type = RestaurantReviewDataType.GOOGLE_REVIEW
    restaurant_review_data_analyzer = RestaurantReviewDataAnalyzer(path, data_type)
    restaurant_review_data_extractors = restaurant_review_data_analyzer.get_restaurant_review_data_extractors()

    for restaurant_review_data_extractor in restaurant_review_data_extractors.values():
        print("Restaurant name:", restaurant_review_data_extractor.get_restaurant_name())
        print("Number of Reviews",
              restaurant_review_data_extractor.get_number_of_reviews() == len(restaurant_review_data_extractor
                                                                              .get_review_data_dataframe()))

def test_google_review_data_overall_rating_vs_overall_rating_computed():
    path = TRIPADVISOR_RESTAURANT_GOOGLE_DATASET_PATH
    data_type = RestaurantReviewDataType.GOOGLE_REVIEW
    restaurant_review_data_analyzer = RestaurantReviewDataAnalyzer(path, data_type)
    restaurant_review_data_extractors = restaurant_review_data_analyzer.get_restaurant_review_data_extractors()

    for restaurant_review_data_extractor in restaurant_review_data_extractors.values():
        print("Restaurant name:", restaurant_review_data_extractor.get_restaurant_name())
        print("overall_rating:", restaurant_review_data_extractor.get_overall_rating())
        print("overall_rating_computed:", restaurant_review_data_extractor.get_overall_rating_computed())
        print("overall_rating == overall_rating_computed_and_rounded_one:",
              restaurant_review_data_extractor.get_overall_rating() == restaurant_review_data_extractor
              .get_overall_rating_computed_and_rounded())

def test_tripadvisor_review_data_overall_rating_vs_overall_rating_computed():
    path = TRIPADVISOR_RESTAURANT_ONLY_RATING_DATASET_PATH
    data_type = RestaurantReviewDataType.TRIPADVISOR_REVIEW
    restaurant_review_data_analyzer = RestaurantReviewDataAnalyzer(path, data_type)
    restaurant_review_data_extractors = restaurant_review_data_analyzer.get_restaurant_review_data_extractors()

    for restaurant_review_data_extractor in restaurant_review_data_extractors.values():
        print("Restaurant name:", restaurant_review_data_extractor.get_restaurant_name())
        print("overall_rating:", restaurant_review_data_extractor.get_overall_rating())
        print("overall_rating_computed:", restaurant_review_data_extractor.get_overall_rating_computed())
        print("overall_rating == overall_rating_computed_and_rounded_one:",
              restaurant_review_data_extractor.get_overall_rating() == restaurant_review_data_extractor
              .get_overall_rating_computed_and_rounded())

def print_author_level_infos():
    path = TRIPADVISOR_RESTAURANT_DATA_PATH
    data_type = RestaurantReviewDataType.TRIPADVISOR_REVIEW
    tripadvisor_restaurant_data_analyzer = RestaurantReviewDataAnalyzer(path, data_type)

    tripadvisor_restaurant_data = tripadvisor_restaurant_data_analyzer.get_restaurant_review_data_extractors()

    for tripadvisor_restaurant_data_extractor in tripadvisor_restaurant_data.values():
        df_author_level_with_rating = tripadvisor_restaurant_data_extractor.get_author_level_with_rating_dataframe()
        print('\n########################')
        print(tripadvisor_restaurant_data_extractor.get_restaurant_name())
        print("author_level contains nan:", df_author_level_with_rating['author_level'].isnull().values.any())
        print("Number of nans in author_level:", df_author_level_with_rating['author_level'].isnull().sum())


#print_infos_of_tripadvisor_restaurant_data_of_all_restaurants()
#test_google_review_data_type()
#print_author_level_infos()
#test_google_review_data_overall_rating_vs_overall_rating_computed()
#test_tripadvisor_review_data_overall_rating_vs_overall_rating_computed()
