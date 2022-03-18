from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

from ba_code.web_scraping.scraping.scraping_constants import XPathTemplates

class ScrapingTool:

    @staticmethod
    def get_main_page_element(url):
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s)
        driver.get(url)
        time.sleep(5)
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
    def click_element_on_page(html_element, html_tag, attribute_name, attribute_value):
        css_selector = ScrapingTool.__get_css_selector(html_tag, attribute_name, attribute_value)
        html_element.find_element(by=By.XPATH, value=css_selector).click()
        time.sleep(1)