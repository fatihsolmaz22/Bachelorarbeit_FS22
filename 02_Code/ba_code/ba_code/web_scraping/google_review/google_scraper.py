import json
import datetime
from selenium.common.exceptions import NoSuchElementException
from ba_code.web_scraping.scraping.scraping_tool import ScrapingTool
from ba_code.web_scraping.google_review.google_constants import RestaurantURLs, HtmlAttributeValues
from ba_code.web_scraping.scraping.scraping_constants import HtmlTags, HtmlAttributes, XPathStringFunctions

def main():
    # TODO: get main page element
    url = "https://www.google.com/maps/place/Outback+Lodge/@47.3669614,8.5455772,17z/data=!3m1!4b1!4m5!3m4!1s0x479aa0acb95d309d:0xd08132daefd16338!8m2!3d47.3669614!4d8.5477659"
    main_page_element = ScrapingTool.get_main_page_element(url)

    # TODO: click on "agree to terms"
    ScrapingTool.click_element_on_page(html_element=main_page_element,
                                       html_tag=HtmlTags.BUTTON_TAG,
                                       attribute_name=HtmlAttributes.CLASS,
                                       attribute_value=HtmlAttributeValues.AGREE_TO_TERMS)

    # TODO: click on rezensionen
    ScrapingTool.click_element_on_page(html_element=main_page_element,
                                       html_tag=HtmlTags.BUTTON_TAG,
                                       attribute_name=HtmlAttributes.CLASS,
                                       attribute_value=HtmlAttributeValues.OPEN_REVIEWS)

    # TODO: get all reviews
    all_reviews = ScrapingTool.get_html_elements_by_css_selector(
        html_element=main_page_element,
        html_tag=HtmlTags.DIV_TAG,
        attribute_name=HtmlAttributes.CLASS,
        attribute_value=HtmlAttributeValues.ALL_REVIEWS
    )

    for review in all_reviews:
        # TODO: get review date
        date = ScrapingTool.get_html_elements_by_css_selector(
            html_element=review,
            html_tag=HtmlTags.SPAN_TAG,
            attribute_name=HtmlAttributes.CLASS,
            attribute_value=HtmlAttributeValues.REVIEW_DATE,
            get_first_element=True
        ).text

        print(date)

        # TODO: get review content

        content = ScrapingTool.get_html_elements_by_css_selector(
            html_element=review,
            html_tag=HtmlTags.SPAN_TAG,
            attribute_name=HtmlAttributes.CLASS,
            attribute_value=HtmlAttributeValues.REVIEW_CONTENT,
            get_first_element=True
        ).text

        print(content)

        print("-------------------")

if __name__ == '__main__':
    main()