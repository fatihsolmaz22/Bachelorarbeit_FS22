from ba_code.data_processing_and_analysis.google_and_tripadvisor.restaurant_review_data_analyzer import \
    RestaurantReviewDataAnalyzer


def print_infos_of_tripadvisor_restaurant_data_of_all_restaurants(tripadvisor_restaurant_data_analyzer):
    tripadvisor_restaurant_data = tripadvisor_restaurant_data_analyzer.get_tripadvisor_restaurant_data_extractors()

    for tripadvisor_restaurant_data_extractor in tripadvisor_restaurant_data.values():
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


def print_author_level_infos(tripadvisor_restaurant_data_analyzer):
    tripadvisor_restaurant_data = tripadvisor_restaurant_data_analyzer.get_tripadvisor_restaurant_data_extractors()

    for tripadvisor_restaurant_data_extractor in tripadvisor_restaurant_data.values():
        df_author_level_with_rating = tripadvisor_restaurant_data_extractor.get_author_level_with_rating_dataframe()
        print('\n########################')
        print(tripadvisor_restaurant_data_extractor.get_restaurant_name())
        print("author_level contains nan:", df_author_level_with_rating['author_level'].isnull().values.any())
        print("Number of nans in author_level:", df_author_level_with_rating['author_level'].isnull().sum())


restaurantReviewDataAnalyzer = RestaurantReviewDataAnalyzer()
print_infos_of_tripadvisor_restaurant_data_of_all_restaurants(restaurantReviewDataAnalyzer)
print_author_level_infos(restaurantReviewDataAnalyzer)