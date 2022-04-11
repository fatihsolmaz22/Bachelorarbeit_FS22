import json
import requests
import time
import pickle
import math
from ba_code.web_scraping.scraping.scraping_tool import ScrapingTool
from ba_code.web_scraping.google_review.google_constants import RestListJsonFormat
# main_page_element = ScrapingTool.get_main_page_element("https://www.google.com")

# Saving cookies:
# import pickle
#
# driver.get("http://www.google.com")
# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

cookies = pickle.load(open("cookies.pkl", "rb"))

# for cookie in cookies:
#     print(cookie)
#     main_page_element.add_cookie(cookie)

# url = "https://www.google.com/maps/preview/review/listentitiesreviews?authuser=0&hl=en&gl=ch&pb=!1m2!1y5156632572410836831!2y15622472877203166342!2m2!1i{}0!2i10!3e1!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1s2TJUYvXKC7vg7_UP9_SEgAY!7e81"
#
with open("google_rest_list.json") as json_file:
    data_list = json.load(json_file)
    for data in data_list:
        rest_name = data[RestListJsonFormat.RESTAURANT_NAME]
        reviews_link_template = data[RestListJsonFormat.REVIEWS_LINK_TEMPLATE]
        # reviews_count = data[RestListJsonFormat.REVIEWS_COUNT]
        # limit = math.ceil(reviews_count/10)
        s = requests.Session()
        for cookie in cookies:
            s.cookies.set(cookie['name'], cookie['value'])
        # x = requests.get(reviews_link_template.format(0))
        # print(x.text)
        limit = 1
        for i in range(0, limit):
            # print(i)
            x = requests.get(reviews_link_template.format(i))
            # print(x.text)
            x = x.text[4:]#.replace(")]}'\n", "")
            # print(x)
            parsed = json.loads(x)
            stars_1 = parsed[5][0]
            stars_2 = parsed[5][1]
            stars_3 = parsed[5][2]
            stars_4 = parsed[5][3]
            stars_5 = parsed[5][4]
            print(stars_1)
            print(stars_2)
            print(stars_3)
            print(stars_4)
            print(stars_5)
            distr = [stars_1, stars_2, stars_3, stars_4, stars_5]
            sum_of_amount_mult_by_stars = 0
            for j in range(0, len(distr)):
                sum_of_amount_mult_by_stars += (j+1)*distr[j]
            result = sum_of_amount_mult_by_stars / sum(distr)
            print(rest_name)
            print(result)
            # print(parsed)
            # print(json.dumps(parsed, indent=4, sort_keys=True))
            print("-------------------------\n")
            # main_page_element.get(url.format(i))
            time.sleep(1)
            break