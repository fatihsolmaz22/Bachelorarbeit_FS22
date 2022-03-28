from enum import Enum

class RestaurantURLs(Enum):
    # NOOCH_BADENERSTRASSE = "https://www.tripadvisor.com/Restaurant_Review-g188113-d2437418-Reviews-Nooch_Asian_Kitchen_Badenerstrasse-Zurich.html"
    # NOOCH_RICHTI = "https://www.tripadvisor.com/Restaurant_Review-g1068946-d7106769-Reviews-Nooch_Asian_Kitchen_Richti-Wallisellen_Zurich.html"
    BUTCHER_BADENERSTRASSE = "https://www.tripadvisor.com/Restaurant_Review-g188113-d10189524-Reviews-The_Butcher_his_Daughter-Zurich.html"
    # BUTCHER_NIEDERDORF = "https://www.tripadvisor.com/Restaurant_Review-g188113-d8359077-Reviews-The_Butcher-Zurich.html"
    # BUTCHER_ZURICHWEST = "https://www.tripadvisor.com/Restaurant_Review-g188113-d12429909-Reviews-The_Butcher-Zurich.html"
    # MISS_MIU = "https://www.tripadvisor.com/Restaurant_Review-g188113-d16737769-Reviews-Miss_Miu_Europaallee-Zurich.html"
    # OUTBACK_STADELHOFEN = "https://www.tripadvisor.com/Restaurant_Review-g188113-d1047970-Reviews-Outback_Lodge-Zurich.html"

    def __str__(self):
        return str(self.name.replace("_", " ").title())

class HtmlAttributeValues:
    OVERALL_RATING = "fdsdx"
    ALL_REVIEWS = "review-container"
    REVIEW_CONTENT = "partial_entry"
    RATING_PARTIAL_MATCHER = "ui_bubble_rating bubble_"
    REVIEW_DATE = "ratingDate"
    ALL_LANGUAGES = "filters_detail_language_filterLang_ALL"
    MORE_BUTTON = "taLnk ulBlueLinks"
    NEXT_PAGE = "nav next ui_button primary"
    AUTHOR_PROFILE = "memberOverlayLink clickable"
    AUTHOR_CONTAINER = "ui_overlay ui_popover arrow_left "#"memberOverlay simple container moRedesign"
    AUTHOR_LEVEL = "badgeinfo"
    AUTHOR_MEMBER_SINCE = "memberdescriptionReviewEnhancements"
    AUTHOR_STATS_CONTAINER = "countsReviewEnhancements"
    AUTHOR_STATS_LIST = "badgeTextReviewEnhancements"
    AUTHOR_DISTRIBUTION_CONTAINER = "wrap container histogramReviewEnhancements"
    AUTHOR_DISTRIBUTION_LIST = "rowCountReviewEnhancements rowCellReviewEnhancements"
    AUTHOR_PROFILE_CLOSE = "ui_close_x"
    NUM_OF_LIKES = "numHelp"