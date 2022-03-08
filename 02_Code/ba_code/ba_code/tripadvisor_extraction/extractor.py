from bs4 import BeautifulSoup
import requests
from enum import Enum

cookies = {"pwv":"2", "pws":"functional|analytics|content_recommendation|targeted_advertising|social_media"}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
           "Upgrade-Insecure-Requests": "1","DNT": "1",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}

class SelectorStrings(Enum):
    ReviewElement = "ui_column is-9"
    ContentInsideOfReview = "partial_entry"

class RestaurantURL(Enum):
    NoochSteinfels = "https://www.tripadvisor.com/Restaurant_Review-g188113-d1023285-Reviews-or{}-Nooch_Asian_Kitchen_Steinfels-Zurich.html"

def load_page(url):
    return requests.get(url, cookies=cookies, headers=headers)

def load_page_interpreter(loaded_page):
    return BeautifulSoup(loaded_page.content, "lxml")

def get_list_of_elements_by_class_name(page_interpreter, class_name):
    return page_interpreter.find_all(class_=class_name)

def get_single_element_by_class_name(page_interpreter, class_name, partial_matching=False):
    return page_interpreter.find(class_=class_name, partial=partial_matching)

def get_text_of_review_element(review_element):
    partial_entry = get_single_element_by_class_name(review_element, class_name=SelectorStrings.ContentInsideOfReview.value)
    raw_text_review = partial_entry.getText()
    cleaned_text = raw_text_review.replace("...", " ").replace("More", "").replace("\n", "")
    return cleaned_text

def get_rating_of_review_element(review_element):
    partial_matching_class_name_for_rating_element = "ui_bubble_rating bubble_"
    contains_css_selector = 'span[class*="{}"]'.format(
        partial_matching_class_name_for_rating_element)  # selects any element that contains the partial_matching_class_name_for_rating_element
    class_names_of_rating_element = review_element.select("{}".format(contains_css_selector))[0]["class"]
    class_name_containing_rating = class_names_of_rating_element[1]
    # have to divide by 10 because ratings look like this 10, 35, 50 -> 1.0, 3.5, 5
    rating = int(class_name_containing_rating.replace("bubble_", "")) / 10
    return rating

def main():
    """
    responses = requests.get("http://httpbin.org/redirect/3")

    for response in responses.history:
        print(response.url)
    """
    review_page_count = 0
    next_page = load_page(RestaurantURL.NoochSteinfels.value.format(review_page_count))
    next_page.history = [] # TODO: this is because first site redirects, but we want to stop the loop when it redirects at last+1 page
    while not next_page.history :
        print("Review Page {} to {} loaded.".format(review_page_count, review_page_count+10))
        print("-------------------------")

        # TODO: here you can use the loaded page and extract reviews from it 0-10, 10-20, etc.
        page_interpreter = load_page_interpreter(next_page)

        all_reviews = get_list_of_elements_by_class_name(page_interpreter,
                                                         class_name=SelectorStrings.ReviewElement.value)
        for review_element in all_reviews:
            rating_of_review_element = get_rating_of_review_element(review_element)
            print(rating_of_review_element)

            text_of_review = get_text_of_review_element(review_element)
            print(text_of_review)
            print("-------------------------")

        # TODO: here it goes to the next page of the restaurant review website
        review_page_count += 10
        next_page = load_page(RestaurantURL.NoochSteinfels.value.format(review_page_count))



if __name__ == "__main__":
    main()
