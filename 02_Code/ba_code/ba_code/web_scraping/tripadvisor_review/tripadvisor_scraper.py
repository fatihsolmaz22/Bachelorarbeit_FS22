import json
import datetime
import time
from selenium.common.exceptions import NoSuchElementException
from ba_code.web_scraping.scraping.scraping_tool import ScrapingTool
from ba_code.web_scraping.tripadvisor_review.tripadvisor_constants import RestaurantURLs, HtmlAttributeValues
from ba_code.web_scraping.scraping.scraping_constants import HtmlTags, HtmlAttributes, XPathStringFunctions
from ba_code.web_scraping.tripadvisor_review.tripadvisor_json_format import RestaurantInfo, AllReviews, AuthorData
from ba_code.web_scraping.tripadvisor_review.tripadvisor_json_format import AuthorStats, AuthorDistribution, ReviewData
from selenium.webdriver.common.by import By
from ba_code.path import TRIPADVISOR_RESTAURANT_ONLY_RATING_DATASET_PATH


def click_on_all_languages(main_page_element):
    ScrapingTool.click_element_on_page(
        main_page_element=main_page_element,
        search_in_element=main_page_element,
        html_tag=HtmlTags.INPUT_TAG,
        attribute_name=HtmlAttributes.ID,
        attribute_value=HtmlAttributeValues.ALL_LANGUAGES)

def click_on_more_button(main_page_element):
    i = 0
    while i != 3:
        try:
            ScrapingTool.click_element_on_page(
                main_page_element=main_page_element,
                search_in_element=main_page_element,
                html_tag=HtmlTags.SPAN_TAG,
                attribute_name=HtmlAttributes.CLASS,
                attribute_value=HtmlAttributeValues.MORE_BUTTON)
        except NoSuchElementException:
            if i < 2:
                time.sleep(5)
        i = i+1

def expand_information_on_page(main_page_element):
    click_on_all_languages(main_page_element)
    # click_on_more_button(main_page_element)

def go_next_page(main_page_element):
    has_next_page = True
    try:
        ScrapingTool.click_element_on_page(
            main_page_element=main_page_element,
            search_in_element=main_page_element,
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

def get_stats_as_dict_from_list(list_of_stats):
    stats_dict = \
        {
            AuthorStats.CONTRIBUTIONS.value:None,
            AuthorStats.CITIES_VISITED.value:None,
            AuthorStats.HELPFUL_VOTES.value:None,
            AuthorStats.PHOTOS.value:None
        }
    for stat in list_of_stats:
        for stat_attribute in AuthorStats:
            if stat_attribute.value.replace("_", " ").capitalize() in stat:
                stat_value = int(stat.replace(",", "").split(" ")[0])
                stats_dict[stat_attribute.value] = stat_value
    return stats_dict

def get_distr_as_dict_from_list(list_of_distr):
    distr_dict = {}
    for i in range(5):
        distr_value = None
        try:
            distr_value = list_of_distr[i]
        except Exception:
            pass
        distr_key = AuthorDistribution.list()[i]
        distr_dict[distr_key] = distr_value

    return distr_dict

from ba_code.web_scraping.tripadvisor_review.tripadvisor_scraper_rest_list import get_list_of_rest
def main():
    list_of_rest = get_list_of_rest()
    for restaurant in list_of_rest:
        all_reviews_data = []

        main_page_element = ScrapingTool.get_main_page_element(restaurant)#.value)

        # TODO: get overall rating of restaurant
        overall_rating = get_overall_rating_of_restaurant(main_page_element)

        print("\n\nRestaurant link:", restaurant)#.value)
        print(overall_rating)

        has_next_page = True
        page_count = 1
        while has_next_page:
            print("\n\n\n-----------------PAGE {}--------------------".format(page_count))

            expand_information_on_page(main_page_element)

            all_reviews = get_all_reviews_on_page(main_page_element)

            for review_element in all_reviews:
                print("----------------------------")

                author_level = None
                author_member_since = None
                author_stats_dict = \
                            {
                                AuthorStats.CONTRIBUTIONS.value:None,
                                AuthorStats.CITIES_VISITED.value:None,
                                AuthorStats.HELPFUL_VOTES.value:None,
                                AuthorStats.PHOTOS.value:None
                            }
                author_distr_dict = get_distr_as_dict_from_list([])
                """
                try:
                    # TODO: click on profile of author
                    ScrapingTool.click_element_on_page(
                        main_page_element=main_page_element,
                        search_in_element=review_element,
                        html_tag=HtmlTags.DIV_TAG,
                        attribute_name=HtmlAttributes.CLASS,
                        attribute_value=HtmlAttributeValues.AUTHOR_PROFILE
                    )

                    # TODO: get author container
                    author_container = ScrapingTool.get_html_elements_by_css_selector(
                        html_element=main_page_element,
                        html_tag=HtmlTags.SPAN_TAG,
                        attribute_name=HtmlAttributes.CLASS,
                        attribute_value=HtmlAttributeValues.AUTHOR_CONTAINER,
                        get_first_element=True
                    )

                    # TODO: get author level
                    author_level = 0
                    try:
                        author_level = int(ScrapingTool.get_html_elements_by_css_selector(
                            html_element=author_container,
                            html_tag=HtmlTags.DIV_TAG,
                            attribute_name=HtmlAttributes.CLASS,
                            attribute_value=HtmlAttributeValues.AUTHOR_LEVEL,
                            get_first_element=True
                        ).text.split(" ")[1])
                    except Exception:
                        pass

                    print("Author Level:", author_level)

                    # TODO: get "member since" info
                    author_description = ScrapingTool.get_html_elements_by_css_selector(
                        html_element=author_container,
                        html_tag=HtmlTags.UL,
                        attribute_name=HtmlAttributes.CLASS,
                        attribute_value=HtmlAttributeValues.AUTHOR_MEMBER_SINCE,
                        get_first_element=True
                    )

                    author_member_since_raw = author_description.find_element(by=By.XPATH, value=".//li").text

                    author_member_since = int(author_member_since_raw.split(" ")[-1])

                    print("Author member since:", author_member_since)

                    # TODO: get author stats container
                    author_stats_container = ScrapingTool.get_html_elements_by_css_selector(
                        html_element=author_container,
                        html_tag=HtmlTags.UL,
                        attribute_name=HtmlAttributes.CLASS,
                        attribute_value=HtmlAttributeValues.AUTHOR_STATS_CONTAINER,
                        get_first_element=True
                    )

                    # TODO: get dict of stats of author
                    author_stats_element_list = ScrapingTool.get_html_elements_by_css_selector(
                        html_element=author_stats_container,
                        html_tag=HtmlTags.SPAN_TAG,
                        attribute_name=HtmlAttributes.CLASS,
                        attribute_value=HtmlAttributeValues.AUTHOR_STATS_LIST
                    )

                    author_stats_list = [element.text for element in author_stats_element_list]
                    author_stats_dict = get_stats_as_dict_from_list(author_stats_list)
                    print(author_stats_dict)

                    # TODO get review distribution as dict of author
                    author_distr_list = []
                    try:
                        author_distr_container = ScrapingTool.get_html_elements_by_css_selector(
                            html_element=author_container,
                            html_tag=HtmlTags.DIV_TAG,
                            attribute_name=HtmlAttributes.CLASS,
                            attribute_value=HtmlAttributeValues.AUTHOR_DISTRIBUTION_CONTAINER,
                            get_first_element=True
                        )

                        author_distr_element_list = ScrapingTool.get_html_elements_by_css_selector(
                            html_element=author_distr_container,
                            html_tag=HtmlTags.SPAN_TAG,
                            attribute_name=HtmlAttributes.CLASS,
                            attribute_value=HtmlAttributeValues.AUTHOR_DISTRIBUTION_LIST
                        )

                        author_distr_list = [int(element.text) for element in author_distr_element_list]
                    except Exception:
                        pass
                    author_distr_dict = get_distr_as_dict_from_list(author_distr_list)
                    print(author_distr_dict)

                    # TODO: close author profile ui

                    ScrapingTool.click_element_on_page(
                        main_page_element=main_page_element,
                        search_in_element=author_container,
                        html_tag=HtmlTags.DIV_TAG,
                        attribute_name=HtmlAttributes.CLASS,
                        attribute_value=HtmlAttributeValues.AUTHOR_PROFILE_CLOSE
                    )

                    print("----------------------------")
                except Exception:
                    pass
                """
                # TODO: review date (Format: 29-09-2015)
                date_of_review = get_date_of_review(review_element)
                print(date_of_review)

                # TODO: review title
                review_title = ""
                review_title = ScrapingTool.get_html_elements_by_css_selector(
                    html_element=review_element,
                    html_tag=HtmlTags.DIV_TAG,
                    attribute_name=HtmlAttributes.CLASS,
                    attribute_value=HtmlAttributeValues.REVIEW_TITLE,
                    get_first_element=True,
                    string_function_value=XPathStringFunctions.CONTAINS_STRING
                ).text.replace("\n", "")
                print(review_title)

                # TODO: rating
                rating_of_review = get_rating_of_review(review_element)
                print(rating_of_review)

                # TODO: text of review
                content_of_review = ""
                content_of_review = get_content_of_review(review_element)
                print(content_of_review)

                # TODO: Likes of review
                likes = 0
                """
                try:
                    likes = int(ScrapingTool.get_html_elements_by_css_selector(
                        html_element=review_element,
                        html_tag=HtmlTags.SPAN_TAG,
                        attribute_name=HtmlAttributes.CLASS,
                        attribute_value=HtmlAttributeValues.NUM_OF_LIKES,
                        get_first_element=True,
                        string_function_value=XPathStringFunctions.CONTAINS_STRING
                    ).text)
                except Exception:
                    pass
                print(likes)
                """

                print("----------------------------\n")

                all_reviews_data += \
                    [{
                        AllReviews.AUTHOR_DATA:
                            {
                                 AuthorData.AUTHOR_LEVEL:author_level,
                                 AuthorData.AUTHOR_MEMBER_SINCE:author_member_since,
                                 AuthorData.AUTHOR_STATS:author_stats_dict,
                                 AuthorData.AUTHOR_DISTRIBUTION:author_distr_dict
                             }
                        ,
                        AllReviews.REVIEW_DATA:
                            {
                                 ReviewData.DATE:date_of_review,
                                 ReviewData.TITLE:review_title,
                                 ReviewData.RATING:rating_of_review,
                                 ReviewData.CONTENT:content_of_review,
                                 ReviewData.LIKES:likes
                             }
                    }]

            # TODO: here it goes to the next page of the restaurant review website
            has_next_page = go_next_page(main_page_element)
            page_count += 1

        restaurant_info_json = {RestaurantInfo.RESTAURANT_NAME:restaurant.split("Reviews-")[1].replace(".html", ""), # restaurant.name
                                RestaurantInfo.OVERALL_RATING:overall_rating,
                                RestaurantInfo.ALL_REVIEWS:all_reviews_data}

        jsonString = json.dumps(restaurant_info_json)
        with open("{}/tripadvisor_review_data_{}.json".format(
                TRIPADVISOR_RESTAURANT_ONLY_RATING_DATASET_PATH,
                restaurant.split("Reviews-")[1].replace(".html", "")), "w+") as json_file: # was  restaurant.name), "w+")
            json_file.write(jsonString)

if __name__ == "__main__":
    main()
