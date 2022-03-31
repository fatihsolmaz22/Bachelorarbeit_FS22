from enum import Enum
import os
from ba_code.path import TRIPADVISOR_RESTAURANT_DATA_PATH

path = TRIPADVISOR_RESTAURANT_DATA_PATH


class ReviewUri(Enum):
    BUTCHER_BADENERSTRASSE = os.path.join(path, 'tripadvisor_review_data_BUTCHER_BADENERSTRASSE.json')
    #BUTCHER_NIEDERDORF = os.path.join(path, 'tripadvisor_review_data_BUTCHER_NIEDERDORF.json')
    #BUTCHER_ZURICHWEST = os.path.join(path, 'tripadvisor_review_data_BUTCHER_ZURICHWEST.json')
    #MISS_MIU = os.path.join(path, 'tripadvisor_review_data_MISS_MIU.json')
    #NOOCH_BADENERSTRASSE = os.path.join(path, 'tripadvisor_review_data_NOOCH_BADENERSTRASSE.json')
    #NOOCH_RICHTI = os.path.join(path, 'tripadvisor_review_data_NOOCH_RICHTI.json')
    #OUTBACK_STADELHOFEN = os.path.join(path, 'tripadvisor_review_data_OUTBACK_STADELHOFEN.json')
