import json
import datetime
import time
from enum import Enum
from selenium.common.exceptions import NoSuchElementException
from ba_code.web_scraping.scraping.scraping_tool import ScrapingTool
from ba_code.web_scraping.tripadvisor_review.tripadvisor_constants import RestaurantURLs, HtmlAttributeValues
from ba_code.web_scraping.scraping.scraping_constants import HtmlTags, HtmlAttributes, XPathStringFunctions

LINK_ELEMENT = "bHGqj Cj b"
NEXT_PAGE = "nav next rndBtn ui_button primary taLnk"

def go_next_page(main_page_element):
    has_next_page = True
    try:
        ScrapingTool.click_element_on_page(html_element=main_page_element,
                                           html_tag=HtmlTags.A_TAG,
                                           attribute_name=HtmlAttributes.CLASS,
                                           attribute_value=NEXT_PAGE)
        time.sleep(3)
    except NoSuchElementException:
        has_next_page = False
    return has_next_page

def main():
    top_rest_zurich_url = "https://www.tripadvisor.ch/Restaurants-g188113-Zurich.html"
    main_page_element = ScrapingTool.get_main_page_element(top_rest_zurich_url)

    has_next_page = True
    page_count = 1

    list_of_links = []

    i = 1
    while has_next_page:
        print("\n\n\n-----------------PAGE {}--------------------".format(page_count))
        while True:
            print(i)

            rest_element = ScrapingTool.get_html_elements_by_css_selector(
                    html_element=main_page_element,
                    html_tag=HtmlTags.DIV_TAG,
                    attribute_name="data-test",
                    attribute_value="{}_list_item".format(i),
                    get_first_element=True,
                )

            rest_link = ScrapingTool.get_html_elements_by_css_selector(
                    html_element= rest_element,
                    html_tag=HtmlTags.A_TAG,
                    attribute_name="class",
                    attribute_value=LINK_ELEMENT,
                    get_first_element=True,
                ).get_attribute("href")
            list_of_links += [rest_link]

            i += 1

            if i % 30 == 0:
                break

        print(len(list_of_links))
        # TODO: here it goes to the next page of the restaurant review website
        has_next_page = go_next_page(main_page_element)
        page_count += 1

    print(list_of_links)
    pass

if __name__ == '__main__':
    main()