from bs4 import BeautifulSoup
import requests
from enum import Enum
from lxml.html import fromstring

cookies = {"pwv":"2", "pws":"functional|analytics|content_recommendation|targeted_advertising|social_media"}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
           "Upgrade-Insecure-Requests": "1","DNT": "1",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}

class SelectorStrings(Enum):
    AttributeSelectorTemplate = '{}[{}{}="{}"]'
    divTag = "div"
    pTag = "p"
    spanTag = "span"
    classAttribute = "class"
    titleAttribute = "title"
    ReviewContainer = "review-container"
    ContentInsideOfReview = "partial_entry"
    RatingPartialMatcher = "ui_bubble_rating bubble_"
    RatingDate = "ratingDate"

class RestaurantURL(Enum):
    NoochSteinfels = "https://www.tripadvisor.com/Restaurant_Review-g188113-d1023285-Reviews-or{}-Nooch_Asian_Kitchen_Steinfels-Zurich.html"

def load_page(url):
    return requests.get(url, cookies=cookies, headers=headers)

def get_page_interpreter(loaded_page):
    return BeautifulSoup(loaded_page.content, "lxml")

def get_html_elements_by_css_selector(element, html_tag, attribute_name, attribute_value, partial_matching=False, get_first_element=False):
    empty_string = ""
    contains_string = "*"
    contains_value = contains_string if partial_matching else empty_string
    css_selector = SelectorStrings.AttributeSelectorTemplate.value.format(html_tag, attribute_name,
                                                                          contains_value, attribute_value)
    html_elements = element.select(css_selector)
    return_value = html_elements if not get_first_element else html_elements[0]
    return return_value

def redirected(page):
    return page.history

def main():

    review_count = 0
    next_page = load_page(RestaurantURL.NoochSteinfels.value.format(review_count))
    # cleaning history because first site redirects, but we want to stop the loop when it redirects at last+1 page
    next_page.history = []
    while not redirected(next_page):
        reviews_per_page = 10
        print("Review Page {} to {} loaded.".format(review_count, review_count + reviews_per_page))
        print("----------------------------")

        # # TODO: here you can use the loaded page and extract reviews from it 0-10, 10-20, etc.
        page_interpreter = get_page_interpreter(next_page)
        all_reviews = get_html_elements_by_css_selector(page_interpreter,
                                                        SelectorStrings.divTag.value,
                                                        SelectorStrings.classAttribute.value,
                                                        SelectorStrings.ReviewContainer.value)
        for review_element in all_reviews:
            # print(review_element.select('p[class="partial_entry"]')[0].text)
            # print("---------------------------")
            # TODO: rating
            rating_class_name = get_html_elements_by_css_selector(review_element,
                                                    SelectorStrings.spanTag.value,
                                                    SelectorStrings.classAttribute.value,
                                                    SelectorStrings.RatingPartialMatcher.value,
                                                    partial_matching=True,
                                                    get_first_element=True)[SelectorStrings.classAttribute.value][1]
            review_rating = int(rating_class_name.replace("bubble_", "")) / 10
            print(review_rating)

            # TODO: text of review
            review_text = get_html_elements_by_css_selector(review_element,
                                                    SelectorStrings.pTag.value,
                                                    SelectorStrings.classAttribute.value,
                                                    SelectorStrings.ContentInsideOfReview.value,
                                                    get_first_element=True).text
            print(review_text)

            # TODO: rating date (Format: September 29, 2015)
            review_date = get_html_elements_by_css_selector(review_element,
                                                            SelectorStrings.spanTag.value,
                                                            SelectorStrings.classAttribute.value,
                                                            SelectorStrings.RatingDate.value,
                                                            get_first_element=True)[SelectorStrings.titleAttribute.value]
            print(review_date)

            print("----------------------------")

        # TODO: here it goes to the next page of the restaurant review website
        review_count += reviews_per_page
        next_page = load_page(RestaurantURL.NoochSteinfels.value.format(review_count))


if __name__ == "__main__":
    main()
