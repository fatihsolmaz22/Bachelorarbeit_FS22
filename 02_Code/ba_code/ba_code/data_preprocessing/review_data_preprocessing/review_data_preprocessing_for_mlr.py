import json
import pandas as pd
from ba_code.data_preprocessing.review_data_preprocessing.review_uri import ReviewUri

"""Lieber Manu Grundsätzlich kann man das schon ausmultiplizieren. Du musst einfach das Datum in einen numerischen 
Wert umwandeln. Z.B. Tage seit heute. Besser als Tage seit heute wäre wohl noch der Kehrwert, 1/Tage. Zur Normierung 
würde ich den ganzen Ausdruck in erster Näherung noch durch die Anzahl Reviews teilen. Hilft das? Ist das überhaupt 
das was Du meinst? Liebe Grüsse Martin """


# extract author_data and review_data from each review
def get_author_and_review_data(all_reviews):
    author_data = []
    review_data = []

    for review in all_reviews:
        # TODO: fix mixed syntax in json attributes FATIHHHHHH --> syntax CAMELCASE
        author_data.append(review['author_data'])
        review_data.append(review['review_data'])

    return [author_data, review_data]


# extract author_level, contribution and helpful_votes from author_data
def extract_important_properties_from_author_data(author_data):
    author_level = []
    contribution = []
    helpful_votes = []

    for data in author_data:
        # TODO: fix mixed syntax in json attributes FATIHHHHHH --> syntax CAMELCASE
        author_level.append(data['Author Level'])
        contribution.append(data['author_stats']['Contributions'])
        helpful_votes.append(data['author_stats']['Helpful votes'])

    return [author_level, contribution, helpful_votes]


# extract date, rating, likes  review_data
def extract_important_properties_from_review_data(review_data):
    dates = []
    ratings = []
    likes = []

    for data in review_data:
        # TODO: fix mixed syntax in json attributes FATIHHHHHH --> syntax CAMELCASE
        dates.append(data['date'])
        ratings.append(data['rating'])
        likes.append(data['likes'])

    return [dates, ratings, likes]


########################################################################################################################
df_mlr_equations = None

review_data_of_restaurant = None

# read review data for each restaurant
for review_uri in ReviewUri:
    review_data_of_restaurant = json.load(open(review_uri.value))

num_of_review = len(review_data_of_restaurant['all_reviews'])
overall_rating = review_data_of_restaurant['overall_rating']
all_reviews = review_data_of_restaurant['all_reviews']

# extracting important properites for the equation
[author_data, review_data] = get_author_and_review_data(all_reviews)
[author_level, contribution, helpful_votes] = extract_important_properties_from_author_data(author_data)
[dates, ratings, likes] = extract_important_properties_from_review_data(review_data)

# equation: overall_rating = rating_1 *
