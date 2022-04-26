import json
import pandas as pd
import numpy as np
from datetime import datetime
from ba_code.data_preprocessing.tripadvisor_restaurant_data_preprocessing.restaurant_data_uri import TripadvisorRestaurantDataUri

# TODO: this file is deprecated, update equations after the review data were analysed
def get_mlr_equations_dataframe():
    overall_ratings = []
    expression_0 = []
    expression_1 = []
    expression_2 = []
    expression_3 = []
    expression_4 = []
    expression_5 = []
    expression_6 = []
    expression_7 = []
    expression_8 = []

    # read review data for each restaurant
    for review_uri in TripadvisorRestaurantDataUri:
        review_data_of_restaurant = json.load(open(review_uri.value))

        # extracting important variables for the equation
        number_of_reviews = len(review_data_of_restaurant['all_reviews'])
        overall_rating = review_data_of_restaurant['overall_rating']
        all_reviews = review_data_of_restaurant['all_reviews']

        # extracting important properties from author_data and review_data
        [author_data, review_data] = extract_author_and_review_data(all_reviews)
        [author_levels, contributions, helpful_votes, author_distributions] = \
            extract_important_properties_from_author_data(author_data)
        author_distribution_levels = extract_author_distribution_levels(author_distributions)
        [age_of_reviews_in_days, ratings, likes] = extract_important_properties_from_review_data(review_data)

        # build equations, TODO special reviews: include: https://www.tripadvisor.ch/Restaurant_Review-g60763-d1236281-Reviews-or70-Club_A_Steakhouse-New_York_City_New_York.html
        overall_ratings.append(overall_rating)
        expression_0.append(
            (1 / number_of_reviews) * np.sum(np.multiply(ratings, np.reciprocal(age_of_reviews_in_days))))
        expression_1.append((1 / number_of_reviews) * np.sum(np.multiply(ratings, likes)))
        expression_2.append((1 / number_of_reviews) * np.sum(np.multiply(ratings, author_levels)))
        expression_3.append((1 / number_of_reviews) * np.sum(np.multiply(ratings, helpful_votes)))
        # TODO: fix contributions bug, some values are zero, and check if expressions are calculated correctly
        reciprocal_of_contributions = np.reciprocal(contributions)
        expression_4.append((1 / number_of_reviews) *
                            np.sum(reciprocal_of_contributions * ratings * author_distribution_levels[0]))
        expression_5.append((1 / number_of_reviews) *
                            np.sum(reciprocal_of_contributions * ratings * author_distribution_levels[1]))
        expression_6.append((1 / number_of_reviews) *
                            np.sum(reciprocal_of_contributions * ratings * author_distribution_levels[2]))
        expression_7.append((1 / number_of_reviews) *
                            np.sum(reciprocal_of_contributions * ratings * author_distribution_levels[3]))
        expression_8.append((1 / number_of_reviews) *
                            np.sum(reciprocal_of_contributions * ratings * author_distribution_levels[4]))

    df_mlr_equations = pd.DataFrame({
        "overall_rating": overall_ratings,
        "expression_0": expression_0,
        "expression_1": expression_1,
        "expression_2": expression_2,
        "expression_3": expression_3,
        "expression_4": expression_4,
        "expression_5": expression_5,
        "expression_6": expression_6,
        "expression_7": expression_7,
        "expression_8": expression_8,
    })

    return df_mlr_equations


def extract_author_and_review_data(all_reviews):
    author_data = []
    review_data = []

    for review in all_reviews:
        author_data.append(review['author_data'])
        review_data.append(review['review_data'])

    return [author_data, review_data]


def extract_important_properties_from_author_data(author_data):
    author_levels = []
    contributions = []
    helpful_votes = []
    author_distributions = []

    for data in author_data:
        author_levels.append(data['author_level'])
        contributions.append(data['author_stats']['contributions'])
        helpful_votes.append(data['author_stats']['helpful_votes'])
        author_distributions.append(data['author_distribution'])

    return [author_levels, contributions, helpful_votes, author_distributions]


def extract_author_distribution_levels(author_distributions):
    review_values_5 = []
    review_values_4 = []
    review_values_3 = []
    review_values_2 = []
    review_values_1 = []

    for author_distribution in author_distributions:
        review_values_5.append(author_distribution['review_value_5'])
        review_values_4.append(author_distribution['review_value_4'])
        review_values_3.append(author_distribution['review_value_3'])
        review_values_2.append(author_distribution['review_value_2'])
        review_values_1.append(author_distribution['review_value_1'])

    return [review_values_5, review_values_4, review_values_3, review_values_2, review_values_1]


def extract_important_properties_from_review_data(review_data):
    age_of_reviews_in_days = []
    ratings = []
    likes = []

    for data in review_data:
        age_of_review_in_days = float((datetime.today() - datetime.strptime(data['date'], '%d-%m-%Y')).days)
        age_of_reviews_in_days.append(age_of_review_in_days)
        ratings.append(data['rating'])
        likes.append(data['likes'])

    return [age_of_reviews_in_days, ratings, likes]


########################################################################################################################
df = get_mlr_equations_dataframe()
