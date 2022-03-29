from enum import Enum

class RestaurantInfo:
    RESTAURANT_NAME = "restaurant_name"
    OVERALL_RATING = "overall_rating"
    ALL_REVIEWS = "all_reviews"

class AllReviews:
    AUTHOR_DATA = "author_data"
    REVIEW_DATA = "review_data"

class AuthorData:
    AUTHOR_LEVEL = "author_level"
    AUTHOR_MEMBER_SINCE = "author_member_since"
    AUTHOR_STATS = "author_stats"
    AUTHOR_DISTRIBUTION = "author_distribution"

class AuthorStats(Enum):
    CONTRIBUTIONS = "Contributions"
    CITIES_VISITED = "Cities visited"
    HELPFUL_VOTES = "Helpful votes"
    PHOTOS = "Photos"

class AuthorDistribution(Enum):
    REVIEW_5 = "review_value_5"
    REVIEW_4 = "review_value_4"
    REVIEW_3 = "review_value_3"
    REVIEW_2 = "review_value_2"
    REVIEW_1 = "review_value_1"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class ReviewData:
    RATING = "rating"
    DATE = "date"
    CONTENT = "content"
    LIKES = "likes"
