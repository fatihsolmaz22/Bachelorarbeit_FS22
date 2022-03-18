from enum import Enum

class XPathStringFunctions:
    CONTAINS_STRING = "contains"

class XPathTemplates:
    ATTRIBUTE_SELECTOR_BASE = './/{}[@{}="{}"]'
    ATTRIBUTE_SELECTOR_STRING_FUNCTIONS = './/{}[{}(@{}, "{}")]'

# TODO: add function to remove necessity of .value to get value of Enum when calling
class HtmlTags:
    A_TAG = "a"
    DIV_TAG = "div"
    P_TAG = "p"
    SPAN_TAG = "span"
    INPUT_TAG = "input"

class HtmlAttributes:
    CLASS = "class"
    TITLE = "title"
    ID = "id"