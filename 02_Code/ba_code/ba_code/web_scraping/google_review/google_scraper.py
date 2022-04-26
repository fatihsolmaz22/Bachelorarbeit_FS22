import json
import datetime
import time
import math
from selenium.common.exceptions import NoSuchElementException
from ba_code.web_scraping.scraping.scraping_tool import ScrapingTool
from ba_code.web_scraping.google_review.google_constants import RestaurantURLs, HtmlAttributeValues
from ba_code.web_scraping.scraping.scraping_constants import HtmlTags, HtmlAttributes, XPathStringFunctions

def get_overall_rating_and_reviews_count(url):
    # TODO: get main page element
    # url = "https://www.google.com/maps/place/Outback+Lodge/@47.3669614,8.5455772,17z/data=!3m1!4b1!4m5!3m4!1s0x479aa0acb95d309d:0xd08132daefd16338!8m2!3d47.3669614!4d8.5477659"
    main_page_element = ScrapingTool.get_main_page_element(url, time_sleep=15, google=True)

    # TODO: click on "agree to terms"
    ScrapingTool.click_element_on_page(
        main_page_element=main_page_element,
        search_in_element=main_page_element,
        html_tag=HtmlTags.BUTTON_TAG,
        attribute_name=HtmlAttributes.CLASS,
        attribute_value=HtmlAttributeValues.AGREE_TO_TERMS)

    # TODO: click on "bestaetigen"
    ScrapingTool.click_element_on_page(
        main_page_element=main_page_element,
        search_in_element=main_page_element,
        html_tag=HtmlTags.BUTTON_TAG,
        attribute_name=HtmlAttributes.CLASS,
        attribute_value=HtmlAttributeValues.BESTAETIGEN)

    # TODO: get overall rating
    overall_rating = float(ScrapingTool.get_html_elements_by_css_selector(
        html_element=main_page_element,
        html_tag=HtmlTags.SPAN_TAG,
        attribute_name=HtmlAttributes.CLASS,
        attribute_value=HtmlAttributeValues.OVERALL_RATING,
        get_first_element=True
    ).text.replace(",", "."))

    # TODO: get total reviews count & calculate how many times you have to scroll (10 reviews per scroll)
    total_reviews_count = int(ScrapingTool.get_html_elements_by_css_selector(
        html_element=main_page_element,
        html_tag=HtmlTags.SPAN_TAG,
        attribute_name=HtmlAttributes.CLASS,
        attribute_value=HtmlAttributeValues.TOTAL_REVIEWS_COUNT,
        get_first_element=True).text.split(" ")[0].replace(".", ""))

    page_limit = math.floor(total_reviews_count / 10)
    return overall_rating, total_reviews_count, page_limit

if __name__ == '__main__':
    get_overall_rating_and_reviews_count("")