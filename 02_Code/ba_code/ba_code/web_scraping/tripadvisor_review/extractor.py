import time
import json
from enum import Enum
import datetime
from selenium.common.exceptions import NoSuchElementException
from browser_tool import BrowserTool
from tripadvisor_strings import RestaurantURLs, HtmlAttributeValues
from browser_tool_strings import HtmlTags, HtmlAttributes, XPathStringFunctions

class JsonFormat(Enum):
    rating = "rating"
    date = "date"
    content = "content"

def click_on_all_languages(browser_tool, main_page_element):
    browser_tool.click_element_on_page(html_element=main_page_element,
                                       html_tag=HtmlTags.INPUT_TAG.value,
                                       attribute_name=HtmlAttributes.ID.value,
                                       attribute_value=HtmlAttributeValues.ALL_LANGUAGES.value)

def click_on_more_button(browser_tool, main_page_element):
    try:
        browser_tool.click_element_on_page(html_element=main_page_element,
                                       html_tag=HtmlTags.SPAN_TAG.value,
                                       attribute_name=HtmlAttributes.CLASS.value,
                                       attribute_value=HtmlAttributeValues.MORE_BUTTON.value)
    except NoSuchElementException:
        pass

def expand_information_on_page(browser_tool, main_page_element):
    click_on_all_languages(browser_tool, main_page_element)
    click_on_more_button(browser_tool, main_page_element)

def go_next_page(browser_tool, main_page_element):
    has_next_page = True
    try:
        browser_tool.click_element_on_page(html_element=main_page_element,
                                           html_tag=HtmlTags.A_TAG.value,
                                           attribute_name=HtmlAttributes.CLASS.value,
                                           attribute_value=HtmlAttributeValues.NEXT_PAGE.value)
    except NoSuchElementException:
        has_next_page = False
    return has_next_page

def get_all_reviews_on_page(browser_tool, main_page_element):
    return browser_tool.get_html_elements_by_css_selector(html_element=main_page_element,
                                                          html_tag=HtmlTags.DIV_TAG.value,
                                                          attribute_name=HtmlAttributes.CLASS.value,
                                                          attribute_value=HtmlAttributeValues.ALL_REVIEWS.value)

def get_rating_of_review(browser_tool, review_element):
    rating_element = browser_tool.get_html_elements_by_css_selector(html_element=review_element,
                                                            html_tag=HtmlTags.SPAN_TAG.value,
                                                            attribute_name=HtmlAttributes.CLASS.value,
                                                            attribute_value=HtmlAttributeValues.RATING_PARTIAL_MATCHER.value,
                                                            string_function_value=XPathStringFunctions.CONTAINS_STRING.value,
                                                            get_first_element=True)
    rating_element_class_name = rating_element.get_attribute(HtmlAttributes.CLASS.value)
    rating_raw = int(rating_element_class_name.replace(HtmlAttributeValues.RATING_PARTIAL_MATCHER.value, ""))/10
    return rating_raw

def get_content_of_review(browser_tool, review_element):
    content_element = browser_tool.get_html_elements_by_css_selector(html_element=review_element,
                                                                     html_tag=HtmlTags.P_TAG.value,
                                                                     attribute_name=HtmlAttributes.CLASS.value,
                                                                     attribute_value=HtmlAttributeValues.REVIEW_CONTENT.value,
                                                                     get_first_element=True)
    content_raw = content_element.text.replace("\n", "")
    return content_raw

def get_date_of_review(browser_tool, review_element):
    date_element = browser_tool.get_html_elements_by_css_selector(html_element=review_element,
                                                                  html_tag=HtmlTags.SPAN_TAG.value,
                                                                 attribute_name=HtmlAttributes.CLASS.value,
                                                                 attribute_value=HtmlAttributeValues.REVIEW_DATE.value,
                                                                 string_function_value=XPathStringFunctions.CONTAINS_STRING.value,
                                                                 get_first_element=True)
    date_raw_string = date_element.get_attribute(HtmlAttributes.TITLE.value)
    review_date_formatted = datetime.datetime.strptime(date_raw_string, "%B %d, %Y").strftime("%d-%m-%Y")
    return review_date_formatted

def main():

    for restaurant in RestaurantURLs:
        all_reviews_data = []

        browser_tool = BrowserTool()
        main_page_element = browser_tool.get_main_page_element(restaurant.value)
        has_next_page = True

        page_count = 1
        while has_next_page:
            print("\n\n\n-----------------PAGE {}--------------------".format(page_count))
            expand_information_on_page(browser_tool, main_page_element)

            all_reviews = get_all_reviews_on_page(browser_tool, main_page_element)

            for review_element in all_reviews:
                # # TODO: review date (Format: 29-09-2015)
                date_of_review = get_date_of_review(browser_tool, review_element)
                print(date_of_review)

                # TODO: rating
                rating_of_review = get_rating_of_review(browser_tool, review_element)
                print(rating_of_review)

                # TODO: text of review
                content_of_review = get_content_of_review(browser_tool, review_element)
                print(content_of_review)

                print("----------------------------")

                all_reviews_data += [{ JsonFormat.date.value:date_of_review,
                                       JsonFormat.rating.value:rating_of_review,
                                       JsonFormat.content.value:content_of_review}]

            # TODO: here it goes to the next page of the restaurant review website
            has_next_page = go_next_page(browser_tool, main_page_element)
            page_count += 1

        jsonString = json.dumps(all_reviews_data)
        with open("../../resources/review_data/tripadvisor_review_data_{}.json".format(restaurant.name), "w+") as json_file:
            json_file.write(jsonString)

if __name__ == "__main__":
    main()
