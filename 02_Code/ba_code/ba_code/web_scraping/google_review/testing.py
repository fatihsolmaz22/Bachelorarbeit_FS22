from enum import Enum

class AuthorStats(Enum):
    CONTRIBUTIONS = "contributions"
    CITIES_VISITED = "cities_visited"
    HELPFUL_VOTES = "helpful_votes"
    PHOTOS = "photos"

    def __repr__(self):
        return self.value

print(AuthorStats.CONTRIBUTIONS)