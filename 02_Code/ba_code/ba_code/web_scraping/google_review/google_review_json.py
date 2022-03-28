import json
import requests
import time
import pickle
from ba_code.web_scraping.scraping.scraping_tool import ScrapingTool
main_page_element = ScrapingTool.get_main_page_element("https://www.google.com")

# Saving cookies:
# import pickle
#
# driver.get("http://www.google.com")
# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

cookies = pickle.load(open("cookies.pkl", "rb"))

for cookie in cookies:
    main_page_element.add_cookie(cookie)

url = "https://www.google.com/maps/preview/review/listentitiesreviews?authuser=0&hl=en&gl=ch&pb=!1m2!1y5159612986811035805!2y15024345747792421688!2m2!1i{}0!2i10!3e1!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1scYRAYouuGY_c7_UPxte1uAg!7e81"
for i in range(40, 161):
    main_page_element.get(url.format(i))
    time.sleep(1)
    print(i+1)