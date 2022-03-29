import json
import datetime
import time
from enum import Enum
from selenium.common.exceptions import NoSuchElementException
from ba_code.web_scraping.scraping.scraping_tool import ScrapingTool
from ba_code.web_scraping.tripadvisor_review.tripadvisor_constants import RestaurantURLs, HtmlAttributeValues
from ba_code.web_scraping.scraping.scraping_constants import HtmlTags, HtmlAttributes, XPathStringFunctions

class JsonFormat:
    RESTAURANT_NAME = "restaurant_name"
    OVERALL_RATING = "overall_rating"
    ALL_REVIEWS = "all_reviews"
    REVIEW_DATA = "review_data"
    RATING = "rating"
    DATE = "date"
    CONTENT = "content"
    REVIEW_LIKES = "likes"
    AUTHOR_DATA = "author_data"
    AUTHOR_INFO = "author_info"
    AUTHOR_STATS = "author_stats"
    AUTHOR_DISTRIBUTION = "author_distribution"

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

class AuthorStats(Enum):
    CONTRIBUTIONS = "Contributions"
    CITIES_VISITED = "Cities visited"
    HELPFUL_VOTES = "Helpful votes"
    PHOTOS = "Photos"

def get_stats_as_dict_from_list(list_of_stats):
    stats_dict = \
        {
            AuthorStats.CONTRIBUTIONS.name.lower():0,
            AuthorStats.CITIES_VISITED.name.lower():0,
            AuthorStats.HELPFUL_VOTES.name.lower():0,
            AuthorStats.PHOTOS.name.lower():0
        }
    for stat in list_of_stats:
        for stat_attribute in AuthorStats:
            if stat_attribute.value in stat:
                stat_value = int(stat.replace(",", "").split(" ")[0])
                stats_dict[stat_attribute.name.lower()] = stat_value
    return stats_dict

class AuthorDistribution(Enum):
    REVIEW_5 = "review_value_5"
    REVIEW_4 = "review_value_4"
    REVIEW_3 = "review_value_3"
    REVIEW_2 = "review_value_2"
    REVIEW_1 = "review_value_1"

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

def get_distr_as_dict_from_list(list_of_distr):
    distr_dict = {}
    for i in range(5):
        distr_value = 0
        try:
            distr_value = list_of_distr[i]
        except Exception:
            pass
        distr_key = AuthorDistribution.list()[i]
        distr_dict[distr_key] = distr_value

    return distr_dict

class AuthorInfo:
    AUTHOR_LEVEL = "author_level"
    AUTHOR_MEMBER_SINCE = "author_member_since"

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
                print("----------------------------")

                # TODO: click on profile of author
                ScrapingTool.click_element_on_page(
                    html_element=review_element,
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
                except IndexError:
                    pass

                print("Author Level:", author_level)

                # TODO: get "member since" info
                author_member_since = int(ScrapingTool.get_html_elements_by_css_selector(
                    html_element=author_container,
                    html_tag=HtmlTags.UL,
                    attribute_name=HtmlAttributes.CLASS,
                    attribute_value=HtmlAttributeValues.AUTHOR_MEMBER_SINCE,
                    get_first_element=True
                ).text.split("\n")[0].split(" ")[-1])

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
                    html_element=author_container,
                    html_tag=HtmlTags.DIV_TAG,
                    attribute_name=HtmlAttributes.CLASS,
                    attribute_value=HtmlAttributeValues.AUTHOR_PROFILE_CLOSE
                )

                print("----------------------------")

                # TODO: review date (Format: 29-09-2015)
                date_of_review = get_date_of_review(review_element)
                print(date_of_review)

                # TODO: rating
                rating_of_review = get_rating_of_review(review_element)
                print(rating_of_review)

                # TODO: text of review
                content_of_review = get_content_of_review(review_element)
                print(content_of_review)

                # TODO: Likes of review
                likes = 0
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

                print("----------------------------\n")

                all_reviews_data += \
                    [{
                        JsonFormat.AUTHOR_DATA:
                            {
                                 AuthorInfo.AUTHOR_LEVEL:author_level,
                                 AuthorInfo.AUTHOR_MEMBER_SINCE:author_member_since,
                                 JsonFormat.AUTHOR_STATS:author_stats_dict,
                                 JsonFormat.AUTHOR_DISTRIBUTION:author_distr_dict
                             }
                        ,
                        JsonFormat.REVIEW_DATA:
                            {
                                 JsonFormat.DATE:date_of_review,
                                 JsonFormat.RATING:rating_of_review,
                                 JsonFormat.CONTENT:content_of_review,
                                 JsonFormat.REVIEW_LIKES:likes
                             }
                    }]

            # TODO: here it goes to the next page of the restaurant review website
            has_next_page = go_next_page(main_page_element)
            page_count += 1

        restaurant_info_json = {JsonFormat.RESTAURANT_NAME:str(restaurant),
                                JsonFormat.OVERALL_RATING:overall_rating,
                                JsonFormat.ALL_REVIEWS:all_reviews_data}

        jsonString = json.dumps(restaurant_info_json)
        with open("../../../resources/review_data/tripadvisor_review_data_{}.json".format(restaurant.name), "w+") as json_file:
            json_file.write(jsonString)

if __name__ == "__main__":
    main()
