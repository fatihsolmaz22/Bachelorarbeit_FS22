from enum import Enum

class RestListJsonFormat:
    RESTAURANT_NAME = "restaurant_name"
    REVIEWS_LINK_TEMPLATE = "reviews_link_template"
    REVIEWS_COUNT = "reviews_count"

class RestaurantURLs(Enum):
    # TODO: add google review links

    def __str__(self):
        return str(self.name.replace("_", " ").title())

class HtmlAttributeValues:
    AGREE_TO_TERMS = "VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc qfvgSe"
    OPEN_REVIEWS = "Yr7JMd-pane-hSRGPd"
    SCROLL_BOX = "siAUzd-neVct section-scrollbox cYB2Ge-oHo7ed cYB2Ge-ti6hGc"
    TOTAL_REVIEWS_COUNT = "gm2-caption"
    OVERALL_RATING = "gm2-display-2"
    ALL_REVIEWS = "ODSEW-ShBeI NIyLF-haAclf gm2-body-2"
    REVIEW_DATE = "ODSEW-ShBeI-RgZmSc-date"
    REVIEW_CONTENT = "ODSEW-ShBeI-text"
    REVIEW_RATING = "ODSEW-ShBeI-H1e3jb"