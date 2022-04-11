from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ba_code.web_scraping.scraping.scraping_constants import XPathTemplates

class ScrapingTool:

    @staticmethod
    def get_main_page_element(url):
        s = Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox") # linux only
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(service=s, options=chrome_options)
        driver.get(url)
        time.sleep(15)
        return driver

    @staticmethod
    def __get_css_selector_template(use_string_function=False):
        css_selector_template = XPathTemplates.ATTRIBUTE_SELECTOR_BASE
        if use_string_function:
            css_selector_template = XPathTemplates.ATTRIBUTE_SELECTOR_STRING_FUNCTIONS
        return css_selector_template

    @staticmethod
    def __get_css_selector(html_tag, attribute_name, attribute_value, string_function_value=None):
        use_string_function = bool(string_function_value)
        css_selector_template = ScrapingTool.__get_css_selector_template(use_string_function=use_string_function)
        if use_string_function:
            css_selector = css_selector_template.format(html_tag, string_function_value, attribute_name, attribute_value)
        else:
            css_selector = css_selector_template.format(html_tag, attribute_name, attribute_value)
        return css_selector

    @staticmethod
    def get_html_elements_by_css_selector(html_element, html_tag, attribute_name, attribute_value, string_function_value=None,
                                          get_first_element=False):
        css_selector = ScrapingTool.__get_css_selector(html_tag, attribute_name, attribute_value, string_function_value)
        html_elements = html_element.find_elements(by=By.XPATH, value=css_selector)
        return html_elements if not get_first_element else html_elements[0]

    @staticmethod
    def click_element_on_page(main_page_element, search_in_element, html_tag, attribute_name, attribute_value):
        css_selector = ScrapingTool.__get_css_selector(html_tag, attribute_name, attribute_value)
        # wait = WebDriverWait(search_in_element, 10)
        # element_to_click = wait.until(EC.element_to_be_clickable((By.XPATH, css_selector)))
        # is_not_clickable = True
        # while is_not_clickable:
        #     try:
        element_to_click = search_in_element.find_element(by=By.XPATH, value=css_selector)#.click()
        main_page_element.execute_script("arguments[0].click();", element_to_click)
        is_not_clickable = False
        time.sleep(2)
            # except Exception:
            #     time.sleep(2)
            #     pass
