from enum import Enum

class AuthorDistribution(Enum):
    REVIEW_5 = "review_value_5"
    REVIEW_4 = "review_value_4"
    REVIEW_3 = "review_value_3"
    REVIEW_2 = "review_value_2"
    REVIEW_1 = "review_value_1"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

print(AuthorDistribution.list())