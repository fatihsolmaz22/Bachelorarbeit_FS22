from enum import Enum

class RestaurantURLs(Enum):
    # NOOCH_STEINFELS = "https://www.tripadvisor.com/Restaurant_Review-g188113-d1023285-Reviews-Nooch_Asian_Kitchen_Steinfels-Zurich.html"
    NOOCH_BADENERSTRASSE = "https://www.tripadvisor.com/Restaurant_Review-g188113-d2437418-Reviews-Nooch_Asian_Kitchen_Badenerstrasse-Zurich.html"

    def __str__(self):
        return str(self.name.replace("_", " ").title())

class HtmlAttributeValues:
    AGREE_TO_TERMS = "VfPpkd-vQzf8d"
    OPEN_REVIEWS = "Yr7JMd-pane-hSRGPd"
    TOTAL_REVIEWS_COUNT = "gm2-caption"