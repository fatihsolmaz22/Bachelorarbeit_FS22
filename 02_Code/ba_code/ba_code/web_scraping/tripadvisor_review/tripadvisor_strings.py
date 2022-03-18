from enum import Enum

class RestaurantURLs(Enum):
    # NOOCH_STEINFELS = "https://www.tripadvisor.com/Restaurant_Review-g188113-d1023285-Reviews-Nooch_Asian_Kitchen_Steinfels-Zurich.html"
    NOOCH_BADENERSTRASSE = "https://www.tripadvisor.com/Restaurant_Review-g188113-d2437418-Reviews-Nooch_Asian_Kitchen_Badenerstrasse-Zurich.html"

class HtmlAttributeValues:
    ALL_REVIEWS = "review-container"
    REVIEW_CONTENT = "partial_entry"
    RATING_PARTIAL_MATCHER = "ui_bubble_rating bubble_"
    REVIEW_DATE = "ratingDate"
    ALL_LANGUAGES = "filters_detail_language_filterLang_ALL"
    MORE_BUTTON = "taLnk ulBlueLinks"
    NEXT_PAGE = "nav next ui_button primary"