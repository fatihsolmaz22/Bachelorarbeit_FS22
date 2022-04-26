class XPathStringFunctions:
    CONTAINS_STRING = "contains"

class XPathTemplates:
    ATTRIBUTE_SELECTOR_BASE = './/{}[@{}="{}"]'
    ATTRIBUTE_SELECTOR_STRING_FUNCTIONS = './/{}[{}(@{}, "{}")]'

class HtmlTags:
    A_TAG = "a"
    DIV_TAG = "div"
    P_TAG = "p"
    SPAN_TAG = "span"
    INPUT_TAG = "input"
    BUTTON_TAG = "button"
    UL = "ul"
    LI = "li"

class HtmlAttributes:
    CLASS = "class"
    TITLE = "title"
    ID = "id"
    DATA_VALUE = "data-value"


# input[@class="btn-primary btn-lg btn"]