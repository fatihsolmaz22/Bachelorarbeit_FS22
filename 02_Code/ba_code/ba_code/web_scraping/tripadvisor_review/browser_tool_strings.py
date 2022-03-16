from enum import Enum

class XPathStringFunctions(Enum):
    CONTAINS_STRING = "contains"

class XPathTemplates(Enum):
    ATTRIBUTE_SELECTOR_BASE = './/{}[@{}="{}"]'
    ATTRIBUTE_SELECTOR_STRING_FUNCTIONS = './/{}[{}(@{}, "{}")]'

class HtmlTags(Enum):
    A_TAG = "a"
    DIV_TAG = "div"
    P_TAG = "p"
    SPAN_TAG = "span"
    INPUT_TAG = "input"

class HtmlAttributes(Enum):
    CLASS = "class"
    TITLE = "title"
    ID = "id"

