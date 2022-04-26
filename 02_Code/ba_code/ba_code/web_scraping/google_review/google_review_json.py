import json
import requests
import time
import pickle
import datetime
import math
from ba_code.web_scraping.scraping.scraping_tool import ScrapingTool
from ba_code.web_scraping.google_review.google_constants import RestListJsonFormat
# main_page_element = ScrapingTool.get_main_page_element("https://www.google.com")
from ba_code.web_scraping.google_review.google_scraper import get_overall_rating_and_reviews_count
from ba_code.web_scraping.tripadvisor_review.tripadvisor_json_format import RestaurantInfo, AllReviews, AuthorData
from ba_code.web_scraping.tripadvisor_review.tripadvisor_json_format import AuthorStats, AuthorDistribution, ReviewData
from ba_code.path import TRIPADVISOR_RESTAURANT_GOOGLE_DATASET_PATH
# Saving cookies:
# import pickle
#
# driver.get("http://www.google.com")
# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

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

cookies_pkl_file = open("cookies.pkl", "rb")
cookies = pickle.load(cookies_pkl_file)

with open("google_rest_list.json") as rest_list_file:
    restaurant_list = json.load(rest_list_file)
    for restaurant in restaurant_list:
        all_reviews_data = []

        s = requests.Session()
        for cookie in cookies:
            s.cookies.set(cookie['name'], cookie['value'])

        rest_name = restaurant[RestListJsonFormat.RESTAURANT_NAME]
        reviews_link_template = restaurant[RestListJsonFormat.REVIEWS_LINK_TEMPLATE]

        # reviews_info_link = restaurant[RestListJsonFormat.REVIEWS_INFO_LINK]
        reviews_info_link = "https://www.google.com/search?q=" + "+".join(rest_name.split("_"))
        overall_rating, reviews_count, page_limit = get_overall_rating_and_reviews_count(reviews_info_link)

        print("restaurant:", rest_name)
        print("overall rating real:", overall_rating)

        # page_limit = 1
        for i in range(0, page_limit+1):
            print("Page {} of {}".format(i, page_limit))
            x = s.get(reviews_link_template.format(i))
            x = x.text[4:]#.replace(")]}'\n", "")

            review_data = json.loads(x)

            reviews_10 = review_data[2]
            try:
                for review in reviews_10:
                    author_level = review[12][1][0][0] if review[12][1][0] is not None else 0
                    review_time_from_epoch = int(review[57])/1000 # epoch times is in milliseconds/1000 -> seconds
                    review_date = datetime.datetime.fromtimestamp(review_time_from_epoch).strftime('%d-%m-%Y')
                    review_rating = review[4]
                    review_content = review[3]
                    print("author level:", author_level)
                    print("date:", review_date)
                    print("rating:", review_rating)
                    print("content:", review_content)
                    print("-------------------------------")

                    author_stats_dict = \
                        {
                            AuthorStats.CONTRIBUTIONS.value: None,
                            AuthorStats.CITIES_VISITED.value: None,
                            AuthorStats.HELPFUL_VOTES.value: None,
                            AuthorStats.PHOTOS.value: None
                        }
                    author_distr_dict = get_distr_as_dict_from_list([])
                    author_member_since = None

                    all_reviews_data += \
                        [{
                            AllReviews.AUTHOR_DATA:
                                {
                                    AuthorData.AUTHOR_LEVEL: author_level,
                                    AuthorData.AUTHOR_MEMBER_SINCE: author_member_since,
                                    AuthorData.AUTHOR_STATS: author_stats_dict,
                                    AuthorData.AUTHOR_DISTRIBUTION: author_distr_dict
                                }
                            ,
                            AllReviews.REVIEW_DATA:
                                {
                                    ReviewData.DATE: review_date,
                                    ReviewData.TITLE: None,
                                    ReviewData.RATING: review_rating,
                                    ReviewData.CONTENT: review_content,
                                    ReviewData.LIKES: None
                                }
                        }]
                # stars_1 = review_data[5][0]
                # stars_2 = review_data[5][1]
                # stars_3 = review_data[5][2]
                # stars_4 = review_data[5][3]
                # stars_5 = review_data[5][4]
                #
                # distr = [stars_1, stars_2, stars_3, stars_4, stars_5]
                # sum_of_amount_mult_by_stars = 0
                # for j in range(0, len(distr)):
                #     sum_of_amount_mult_by_stars += (j+1)*distr[j]
                # result = sum_of_amount_mult_by_stars / sum(distr)
                # print("overall rating calculated", result)
                print("-------------------------\n")
                time.sleep(1)
            except Exception:
                pass

        restaurant_info_json = {RestaurantInfo.RESTAURANT_NAME: rest_name,
                                RestaurantInfo.OVERALL_RATING: overall_rating,
                                RestaurantInfo.ALL_REVIEWS: all_reviews_data,
                                RestaurantInfo.REVIEWS_COUNT: reviews_count}

        jsonString = json.dumps(restaurant_info_json)
        with open("{}/google_review_data_{}.json".format(
                TRIPADVISOR_RESTAURANT_GOOGLE_DATASET_PATH,
                rest_name), "w+") as json_file: # was  restaurant.name), "w+")
            json_file.write(jsonString)

# TODO: scraper needs same cookies for captcha test
cookies_pkl_file.close()