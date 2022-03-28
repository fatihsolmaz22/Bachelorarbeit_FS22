import json
import datetime
import time
import math
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

    # TODO: click on all reviews
    ScrapingTool.click_element_on_page(html_element=main_page_element,
                                       html_tag=HtmlTags.BUTTON_TAG,
                                       attribute_name=HtmlAttributes.CLASS,
                                       attribute_value=HtmlAttributeValues.OPEN_REVIEWS)

    # TODO: get overall rating
    overall_rating = float(ScrapingTool.get_html_elements_by_css_selector(
        html_element=main_page_element,
        html_tag=HtmlTags.DIV_TAG,
        attribute_name=HtmlAttributes.CLASS,
        attribute_value=HtmlAttributeValues.OVERALL_RATING,
        get_first_element=True
    ).text.replace(",", "."))
    print(overall_rating)

    # TODO: get total reviews count & calculate how many times you have to scroll (10 reviews per scroll)
    total_reviews_count = int(ScrapingTool.get_html_elements_by_css_selector(
        html_element=main_page_element,
        html_tag=HtmlTags.DIV_TAG,
        attribute_name=HtmlAttributes.CLASS,
        attribute_value=HtmlAttributeValues.TOTAL_REVIEWS_COUNT,
        get_first_element=True).text.split(" ")[0].replace("’", ""))
    print(total_reviews_count)

    scroll_amount = math.floor(total_reviews_count / 10)
    print("Scrolling {} times..".format(scroll_amount))

    scroll_box = ScrapingTool.get_html_elements_by_css_selector(
        html_element=main_page_element,
        html_tag=HtmlTags.DIV_TAG,
        attribute_name=HtmlAttributes.CLASS,
        attribute_value=HtmlAttributeValues.SCROLL_BOX,
        get_first_element=True)

    all_reviews = []

    for i in range(scroll_amount):
        """
        Through passing a simple JavaScript snippet to the chrome driver(driver.execute_script) 
        we set the scroll element’s(scrollable_div) vertical position(.scrollTop) to it’s height (.scrollHeight).
        """
        main_page_element.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',
                scroll_box)
        print(i+1)
        time.sleep(3)
        if i != 0 and i % 50 == 0:
            current_all_reviews = ScrapingTool.get_html_elements_by_css_selector(
                html_element=main_page_element,
                html_tag=HtmlTags.DIV_TAG,
                attribute_name=HtmlAttributes.CLASS,
                attribute_value=HtmlAttributeValues.ALL_REVIEWS
            )

            all_reviews += [current_all_reviews]
            j = 0
            for review in current_all_reviews:
                main_page_element.execute_script(
                    "arguments[0].parentNode.removeChild(arguments[0])", review)
                time.sleep(0.2)
                j+=1
                print("anotha one bites the dust ", j)
            time.sleep(3)

    print("-------------------------")

    # TODO: get all reviews

    print(all_reviews)


    # for review in all_reviews:
    #     # TODO: get review date
    #     date = ScrapingTool.get_html_elements_by_css_selector(
    #         html_element=review,
    #         html_tag=HtmlTags.SPAN_TAG,
    #         attribute_name=HtmlAttributes.CLASS,
    #         attribute_value=HtmlAttributeValues.REVIEW_DATE,
    #         get_first_element=True
    #     ).text
    #
    #     print(date)
    #
    #     # TODO: get review rating
    #
    #     rating = ScrapingTool.get_html_elements_by_css_selector(
    #         html_element=review,
    #         html_tag=HtmlTags.SPAN_TAG,
    #         attribute_name=HtmlAttributes.CLASS,
    #         attribute_value=HtmlAttributeValues.REVIEW_RATING,
    #         get_first_element=True
    #     ).get_attribute("aria-label")
    #
    #     print(rating)
    #
    #     # TODO: get review content
    #
    #     content = ScrapingTool.get_html_elements_by_css_selector(
    #         html_element=review,
    #         html_tag=HtmlTags.SPAN_TAG,
    #         attribute_name=HtmlAttributes.CLASS,
    #         attribute_value=HtmlAttributeValues.REVIEW_CONTENT,
    #         get_first_element=True
    #     ).text
    #
    #     print(content)
    #
    #     print("-------------------")

if __name__ == '__main__':
    main()