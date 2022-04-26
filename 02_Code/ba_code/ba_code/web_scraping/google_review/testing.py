import requests
import pickle
from ba_code.web_scraping.scraping.scraping_tool import ScrapingTool
import time
from ba_code.web_scraping.scraping.scraping_constants import HtmlTags, HtmlAttributes, XPathStringFunctions

# cookies_pkl_file = open("cookies.pkl", "rb")
# cookies = pickle.load(cookies_pkl_file)
#
# s = requests.Session()
# for cookie in cookies:
#     s.cookies.set(cookie['name'], cookie['value'])
#
# url = "https://www.google.com/maps/place/Outback+Lodge/@47.3669614,8.5455772,17z/data=!3m1!4b1!4m5!3m4!1s0x479aa0acb95d309d:0xd08132daefd16338!8m2!3d47.3669614!4d8.5477659"
# x = requests.get(url).content
# print(x)
#
# cookies_pkl_file.close()

main_page = ScrapingTool.get_main_page_element("https://www.google.com/search?q=OUTBACK+STADELHOFEN", time_sleep=3)
# time.sleep(3)
# pickle.dump( main_page.get_cookies() , open("cookies.pkl","wb"))
ScrapingTool.click_element_on_page(
                        main_page_element=main_page,
                        search_in_element=main_page,
                        html_tag=HtmlTags.BUTTON_TAG,
                        attribute_name=HtmlAttributes.ID,
                        attribute_value="L2AGLb"
                    )
"""
"""