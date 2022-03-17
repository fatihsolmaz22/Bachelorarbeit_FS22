from enum import Enum

class XPathStringFunctions(Enum):
    CONTAINS_STRING = "contains"

class XPathTemplates(Enum):
    ATTRIBUTE_SELECTOR_BASE = './/{}[@{}="{}"]'
    ATTRIBUTE_SELECTOR_STRING_FUNCTIONS = './/{}[{}(@{}, "{}")]'

# TODO: add function to remove necessity of .value to get value of Enum when calling
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

