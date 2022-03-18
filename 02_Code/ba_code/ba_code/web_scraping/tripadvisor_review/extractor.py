import time
import json
from enum import Enum
import datetime
from selenium.common.exceptions import NoSuchElementException
from ba_code.web_scraping.scraping.scraping_tool import ScrapingTool
from ba_code.web_scraping.tripadvisor_review.tripadvisor_strings import RestaurantURLs, HtmlAttributeValues
from ba_code.web_scraping.scraping.scraping_constants import HtmlTags, HtmlAttributes, XPathStringFunctions

class JsonFormat:
    RESTAURANT_NAME = "restaurant_name"
    OVERALL_RATING = "overall_rating"
    ALL_REVIEWS = "all_reviews"
    RATING = "rating"
    DATE = "date"
    CONTENT = "content"

def click_on_all_languages(main_page_element):
    ScrapingTool.click_element_on_page(html_element=main_page_element,
                                       html_tag=HtmlTags.INPUT_TAG,
                                       attribute_name=HtmlAttributes.ID,
                                       attribute_value=HtmlAttributeValues.ALL_LANGUAGES)

def click_on_more_button(main_page_element):
    try:
        ScrapingTool.click_element_on_page(html_element=main_page_element,
                                       html_tag=HtmlTags.SPAN_TAG,
                                       attribute_name=HtmlAttributes.CLASS,
                                       attribute_value=HtmlAttributeValues.MORE_BUTTON)
    except NoSuchElementException:
        pass

def expand_information_on_page(main_page_element):
    click_on_all_languages(main_page_element)
    click_on_more_button(main_page_element)

def go_next_page(main_page_element):
    has_next_page = True
    try:
        ScrapingTool.click_element_on_page(html_element=main_page_element,
                                           html_tag=HtmlTags.A_TAG,
                                           attribute_name=HtmlAttributes.CLASS,
                                           attribute_value=HtmlAttributeValues.NEXT_PAGE)
    except NoSuchElementException:
        has_next_page = False
    return has_next_page

def get_overall_rating_of_restaurant(main_page_element):
    return float(ScrapingTool.get_html_elements_by_css_selector(html_element=main_page_element,
                                                   html_tag=HtmlTags.SPAN_TAG,
                                                   attribute_name=HtmlAttributes.CLASS,
                                                   attribute_value=HtmlAttributeValues.OVERALL_RATING,
                                                   get_first_element=True).text)

def get_all_reviews_on_page(main_page_element):
    return ScrapingTool.get_html_elements_by_css_selector(html_element=main_page_element,
                                                          html_tag=HtmlTags.DIV_TAG,
                                                          attribute_name=HtmlAttributes.CLASS,
                                                          attribute_value=HtmlAttributeValues.ALL_REVIEWS)

def get_rating_of_review(review_element):
    rating_element = ScrapingTool.get_html_elements_by_css_selector(html_element=review_element,
                                                            html_tag=HtmlTags.SPAN_TAG,
                                                            attribute_name=HtmlAttributes.CLASS,
                                                            attribute_value=HtmlAttributeValues.RATING_PARTIAL_MATCHER,
                                                            string_function_value=XPathStringFunctions.CONTAINS_STRING,
                                                            get_first_element=True)
    rating_element_class_name = rating_element.get_attribute(HtmlAttributes.CLASS)
    rating_raw = int(rating_element_class_name.replace(HtmlAttributeValues.RATING_PARTIAL_MATCHER, ""))/10
    return rating_raw

def get_content_of_review(review_element):
    content_element = ScrapingTool.get_html_elements_by_css_selector(html_element=review_element,
                                                                     html_tag=HtmlTags.P_TAG,
                                                                     attribute_name=HtmlAttributes.CLASS,
                                                                     attribute_value=HtmlAttributeValues.REVIEW_CONTENT,
                                                                     get_first_element=True)
    content_raw = content_element.text.replace("\n", "")
    return content_raw

def get_date_of_review(review_element):
    date_element = ScrapingTool.get_html_elements_by_css_selector(html_element=review_element,
                                                                  html_tag=HtmlTags.SPAN_TAG,
                                                                 attribute_name=HtmlAttributes.CLASS,
                                                                 attribute_value=HtmlAttributeValues.REVIEW_DATE,
                                                                 string_function_value=XPathStringFunctions.CONTAINS_STRING,
                                                                 get_first_element=True)
    date_raw_string = date_element.get_attribute(HtmlAttributes.TITLE)
    review_date_formatted = datetime.datetime.strptime(date_raw_string, "%B %d, %Y").strftime("%d-%m-%Y")
    return review_date_formatted

def main():

    for restaurant in RestaurantURLs:
        all_reviews_data = []

        main_page_element = ScrapingTool.get_main_page_element(restaurant.value)

        # TODO: get overall rating of restaurant
        overall_rating = get_overall_rating_of_restaurant(main_page_element)
        print(overall_rating)

        has_next_page = True
        page_count = 1
        while has_next_page:
            print("\n\n\n-----------------PAGE {}--------------------".format(page_count))
            expand_information_on_page(main_page_element)

            all_reviews = get_all_reviews_on_page(main_page_element)

            for review_element in all_reviews:
                # # TODO: review date (Format: 29-09-2015)
                date_of_review = get_date_of_review(review_element)
                print(date_of_review)

                # TODO: rating
                rating_of_review = get_rating_of_review(review_element)
                print(rating_of_review)

                # TODO: text of review
                content_of_review = get_content_of_review(review_element)
                print(content_of_review)

                print("----------------------------")

                all_reviews_data += [{JsonFormat.DATE:date_of_review,
                                      JsonFormat.RATING:rating_of_review,
                                      JsonFormat.CONTENT:content_of_review}]

            # TODO: here it goes to the next page of the restaurant review website
            has_next_page = go_next_page(main_page_element)
            page_count += 1

        restaurant_info_json = [{JsonFormat.RESTAURANT_NAME:str(restaurant),
                                 JsonFormat.OVERALL_RATING:overall_rating,
                                 JsonFormat.ALL_REVIEWS:all_reviews_data}]

        jsonString = json.dumps(restaurant_info_json)
        with open("../../../resources/review_data/tripadvisor_review_data_{}.json".format(restaurant.name), "w+") as json_file:
            json_file.write(jsonString)

if __name__ == "__main__":
    main()
