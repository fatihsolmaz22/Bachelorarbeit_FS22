import requests
import pickle
from ba_code.web_scraping.scraping.scraping_tool import ScrapingTool
import time

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

main_page = ScrapingTool.get_main_page_element("https://www.google.com/maps/preview/review/listentitiesreviews?authuser=0&hl=en&gl=ch&pb=!1m2!1y5159612986811035805!2y15024345747792421688!2m2!1i0!2i10!3e1!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1sMXRlYqbuKozXkgXnv6_AAw!7e81")
time.sleep(30)
pickle.dump( main_page.get_cookies() , open("cookies.pkl","wb"))