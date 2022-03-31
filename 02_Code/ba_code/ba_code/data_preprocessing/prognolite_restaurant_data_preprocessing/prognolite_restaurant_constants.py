from enum import Enum
import os
from ba_code.path import PROGNOLITE_RESTAURANT_DATA_PATH

path = PROGNOLITE_RESTAURANT_DATA_PATH


class PrognoliteRestaurantDataUri(Enum):
    ALL_RESTAURANT_DATA = os.path.join(path, 'fwg_composition_data_IDP.csv')

# TODO: not so clean, automate this
class Restaurant(Enum):
    BUTCHER_USTER = "fwg-butcher-uster"
    NEGISHI_METALLI = "fwg-negishi-metalli"
    BUTCHER_AARBERGERGASSE = "fwg-butcher-aarbergergasse"
    NOOCH_AARBERGERGASSE = "fwg-nooch-aarbergergasse"
    NEGISHI_ARCHHOEFE = "fwg-negishi-archhoefe"
    BUTCHER_BADENERSTRASSE = "fwg-butcher-badenerstrasse"
    NOOCH_BADENERSTRASSE = "fwg-nooch-badenerstrasse"
    NOOCH_BARFI = "fwg-nooch-barfi"
    MISSMIU_EUROPAALLEE = "fwg-missmiu-europaallee"
    NOOCH_MALL_OF_SWITZERLAND = "fwg-nooch-mallofSwitzerland"
    NOOCH_MATTENHOF = "fwg-nooch-mattenhof"
    BUTCHER_METALLI = "fwg-butcher-metalli"
    BUTCHER_NIEDERDORF = "fwg-butcher-niederdorf"
    NEGISHI_PILATUSSTRASSE = "fwg-negishi-pilatusstrasse"
    NOOCH_RICHTI = "fwg-nooch-richti"
    OUTBACK_STAD = "fwg-outback-stad"
    NEGISHI_STEINEN = "fwg-negishi-steinen"
    NOOCH_USTER = "fwg-nooch-uster"
    BUTCHER_ZUERICH_WEST = "fwg-butcher-zuerichWest"
