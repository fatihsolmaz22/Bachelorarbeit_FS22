from enum import Enum
import os
from ba_code.path import TRIPADVISOR_RESTAURANT_DATA_PATH, TRIPADVISOR_RESTAURANT_GOOGLE_DATASET_PATH, \
    TRIPADVISOR_RESTAURANT_ONLY_RATING_DATASET_PATH

path_tripadvisor = TRIPADVISOR_RESTAURANT_DATA_PATH
path_google = TRIPADVISOR_RESTAURANT_GOOGLE_DATASET_PATH


class TripadvisorRestaurantDataUri(Enum):
    BUTCHER_USTER = os.path.join(path_tripadvisor, 'tripadvisor_review_data_BUTCHER_USTER.json')
    NEGISHI_METALLI = os.path.join(path_tripadvisor, 'tripadvisor_review_data_NEGISHI_METALLI.json')
    BUTCHER_AARBERGERGASSE = os.path.join(path_tripadvisor, 'tripadvisor_review_data_BUTCHER_AARBERGERGASSE.json')
    NOOCH_AARBERGERGASSE = os.path.join(path_tripadvisor, 'tripadvisor_review_data_NOOCH_AARBERGERGASSE.json')
    NOOCH_BARFI = os.path.join(path_tripadvisor, 'tripadvisor_review_data_NOOCH_BARFI.json')
    MISSMIU_EUROPAALLEE = os.path.join(path_tripadvisor, 'tripadvisor_review_data_MISSMIU_EUROPAALLEE.json')
    NOOCH_MALL_OF_SWITZERLAND = os.path.join(path_tripadvisor, 'tripadvisor_review_data_NOOCH_MALL_OF_SWITZERLAND.json')
    NOOCH_MATTENHOF = os.path.join(path_tripadvisor, 'tripadvisor_review_data_NOOCH_MATTENHOF.json')
    BUTCHER_METALLI = os.path.join(path_tripadvisor, 'tripadvisor_review_data_BUTCHER_METALLI.json')
    NEGISHI_PILATUSSTRASSE = os.path.join(path_tripadvisor, 'tripadvisor_review_data_NEGISHI_PILATUSSTRASSE.json')
    NOOCH_RICHTI = os.path.join(path_tripadvisor, 'tripadvisor_review_data_NOOCH_RICHTI.json')
    OUTBACK_STAD = os.path.join(path_tripadvisor, 'tripadvisor_review_data_OUTBACK_STAD.json')
    NEGISHI_STEINEN = os.path.join(path_tripadvisor, 'tripadvisor_review_data_NEGISHI_STEINEN.json')
    NOOCH_USTER = os.path.join(path_tripadvisor, 'tripadvisor_review_data_NOOCH_USTER.json')
    BUTCHER_ZUERICH_WEST = os.path.join(path_tripadvisor, 'tripadvisor_review_data_BUTCHER_ZUERICH_WEST.json')


class GoogleRestaurantDataUri(Enum):
    BUTCHER_USTER = os.path.join(path_google, 'google_review_data_BUTCHER_USTER.json')
    NEGISHI_METALLI = os.path.join(path_google, 'google_review_data_NEGISHI_METALLI.json')
    BUTCHER_AARBERGERGASSE = os.path.join(path_google, 'google_review_data_BUTCHER_AARBERGERGASSE.json')
    NOOCH_AARBERGERGASSE = os.path.join(path_google, 'google_review_data_NOOCH_AARBERGERGASSE.json')
    NOOCH_BARFI = os.path.join(path_google, 'google_review_data_NOOCH_BARFI.json')
    MISSMIU_EUROPAALLEE = os.path.join(path_google, 'google_review_data_MISSMIU_EUROPAALLEE.json')
    NOOCH_MALL_OF_SWITZERLAND = os.path.join(path_google, 'google_review_data_NOOCH_MALL_OF_SWITZERLAND.json')
    NOOCH_MATTENHOF = os.path.join(path_google, 'google_review_data_NOOCH_MATTENHOF.json')
    BUTCHER_METALLI = os.path.join(path_google, 'google_review_data_BUTCHER_METALLI.json')
    NEGISHI_PILATUSSTRASSE = os.path.join(path_google, 'google_review_data_NEGISHI_PILATUSSTRASSE.json')
    NOOCH_RICHTI = os.path.join(path_google, 'google_review_data_NOOCH_RICHTI.json')
    OUTBACK_STAD = os.path.join(path_google, 'google_review_data_OUTBACK_STADELHOFEN.json')
    NEGISHI_STEINEN = os.path.join(path_google, 'google_review_data_NEGISHI_STEINEN.json')
    NOOCH_USTER = os.path.join(path_google, 'google_review_data_NOOCH_USTER.json')
    BUTCHER_ZUERICH_WEST = os.path.join(path_google, 'google_review_data_BUTCHER_ZUERICH_WEST.json')
