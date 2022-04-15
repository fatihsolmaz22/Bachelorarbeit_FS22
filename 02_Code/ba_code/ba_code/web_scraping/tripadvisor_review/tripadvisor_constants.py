from enum import Enum

class RestaurantURLs(Enum):
    BUTCHER_USTER = "https://www.tripadvisor.com/Restaurant_Review-g667198-d18187148-Reviews-The_Butcher-Uster.html"
    NEGISHI_METALLI = "https://www.tripadvisor.com/Restaurant_Review-g188110-d6954588-Reviews-Negishi_Sushi_Bar-Zug.html"
    BUTCHER_AARBERGERGASSE = "https://www.tripadvisor.com/Restaurant_Review-g188052-d11772424-Reviews-The_Butcher-Bern_Bern_Mittelland_District_Canton_of_Bern.html"
    NOOCH_AARBERGERGASSE = "https://www.tripadvisor.com/Restaurant_Review-g188052-d1385872-Reviews-Nooch_Asian_Kitchen-Bern_Bern_Mittelland_District_Canton_of_Bern.html"
    NOOCH_BARFI = "https://www.tripadvisor.com/Restaurant_Review-g188049-d1208716-Reviews-Nooch_Basel_Barfi-Basel.html"
    MISSMIU_EUROPAALLEE = "https://www.tripadvisor.com/Restaurant_Review-g188113-d16737769-Reviews-Miss_Miu_Europaallee-Zurich.html"
    NOOCH_MALL_OF_SWITZERLAND = "https://www.tripadvisor.com/Restaurant_Review-g1079168-d12954748-Reviews-Nooch_Asian_Kitchen-Ebikon.html"
    NOOCH_MATTENHOF = "https://www.tripadvisor.com/Restaurant_Review-g1124758-d16699857-Reviews-Nooch_Asian_Kitchen-Kriens_Lucerne.html"
    BUTCHER_METALLI = "https://www.tripadvisor.com/Restaurant_Review-g188110-d10453304-Reviews-The_Butcher-Zug.html"
    NEGISHI_PILATUSSTRASSE = "https://www.tripadvisor.com/Restaurant_Review-g188064-d12009305-Reviews-Negishi_Sushi_Bar-Lucerne.html"
    NOOCH_RICHTI = "https://www.tripadvisor.com/Restaurant_Review-g1068946-d7106769-Reviews-Nooch_Asian_Kitchen_Richti-Wallisellen_Zurich.html"
    OUTBACK_STAD = "https://www.tripadvisor.com/Restaurant_Review-g188113-d1047970-Reviews-Outback_Lodge-Zurich.html"
    NEGISHI_STEINEN = "https://www.tripadvisor.com/Restaurant_Review-g188049-d2656832-Reviews-Negishi_Sushi_Bar-Basel.html"
    NOOCH_USTER = "https://www.tripadvisor.com/Restaurant_Review-g667198-d18716074-Reviews-Nooch_Asian_Kitchen_Uster-Uster.html"
    BUTCHER_ZUERICH_WEST = "https://www.tripadvisor.com/Restaurant_Review-g188113-d12429909-Reviews-The_Butcher-Zurich.html"

    def __str__(self):
        return str(self.name.replace("_", " ").title())

class HtmlAttributeValues:
    OVERALL_RATING = "fdsdx"
    ALL_REVIEWS = "review-container"
    REVIEW_TITLE = "quote"
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