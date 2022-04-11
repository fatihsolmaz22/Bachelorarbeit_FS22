from ba_code.data_preprocessing.tripadvisor_restaurant_data_preprocessing.tripadvisor_restaurant_data_uri import \
    TripadvisorRestaurantDataUri
from ba_code.data_preprocessing.tripadvisor_restaurant_data_preprocessing.tripadvisor_restaurant_data_extractor import \
    TripadvisorRestaurantDataExtractor


def print_infos_of_tripadvisor_restaurant_data(file):
    tripadvisor_restaurant_data_extractor = TripadvisorRestaurantDataExtractor()
    tripadvisor_restaurant_data_extractor.load_restaurant_data(file)

    df_review_data = tripadvisor_restaurant_data_extractor.get_review_data_dataframe()
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
    print("Review contains any duplicate:", any_duplicates)
    print("Review contains ...More:", contains_more)
    print("Number of entries in df_review_data", len(df_review_data.index))
    print("Number of entries in df_author_base_infos", len(df_author_base_infos))
    print("Number of entries in df_author_stats", len(df_author_stats))
    print("Number of entries in df_author_distribution", len(df_author_distribution))


print_infos_of_tripadvisor_restaurant_data(open(TripadvisorRestaurantDataUri.DIFFERENTE_HOTEL_KRONE.value))
