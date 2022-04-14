from enum import Enum
import os
from ba_code.path import PROGNOLITE_RESTAURANT_DATA_PATH


class PrognoliteRestaurantDataUri(Enum):
    PROGNOLITE_RESTAURANT_DATA = os.path.join(PROGNOLITE_RESTAURANT_DATA_PATH, 'fwg_composition_data_IDP.csv')


# Restaurants with revenue data are listed below. Not listed are some restaurants where no revenue data exists.
# I got these informations by calling PrognoliteRestaurantDataExtractor().get_restaurant_data() which lists
# all revenue data for all restaurants.
class Restaurant(Enum):
    BUTCHER_USTER = "fwg-butcher-uster"
    NEGISHI_METALLI = "fwg-negishi-metalli"
    BUTCHER_AARBERGERGASSE = "fwg-butcher-aarbergergasse"
    NOOCH_AARBERGERGASSE = "fwg-nooch-aarbergergasse"
    NOOCH_BARFI = "fwg-nooch-barfi"
    MISSMIU_EUROPAALLEE = "fwg-missmiu-europaallee"
    NOOCH_MALL_OF_SWITZERLAND = "fwg-nooch-mallofSwitzerland"
    NOOCH_MATTENHOF = "fwg-nooch-mattenhof"
    BUTCHER_METALLI = "fwg-butcher-metalli"
    NEGISHI_PILATUSSTRASSE = "fwg-negishi-pilatusstrasse"
    NOOCH_RICHTI = "fwg-nooch-richti"
    OUTBACK_STAD = "fwg-outback-stad"
    NEGISHI_STEINEN = "fwg-negishi-steinen"
    NOOCH_USTER = "fwg-nooch-uster"
    BUTCHER_ZUERICH_WEST = "fwg-butcher-zuerichWest"
