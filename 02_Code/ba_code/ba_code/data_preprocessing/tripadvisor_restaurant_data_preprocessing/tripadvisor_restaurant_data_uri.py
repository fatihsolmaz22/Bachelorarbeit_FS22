from enum import Enum
import os
from ba_code.path import TRIPADVISOR_RESTAURANT_DATA_PATH

path = TRIPADVISOR_RESTAURANT_DATA_PATH


class TripadvisorRestaurantDataUri(Enum):
    #BUTCHER_BADENERSTRASSE = os.path.join(path, 'tripadvisor_review_data_BUTCHER_BADENERSTRASSE.json')
    DIFFERENTE_HOTEL_KRONE = os.path.join(path, 'tripadvisor_review_data_Differente_Hotel_Krone_Unterstrass-Zurich.json')
    KHUJUG_ZURICH = os.path.join(path, 'tripadvisor_review_data_Restaurant_Khujug-Zurich.json')
    #BUTCHER_NIEDERDORF = os.path.join(path, 'tripadvisor_review_data_BUTCHER_NIEDERDORF.json')
    #BUTCHER_ZURICHWEST = os.path.join(path, 'tripadvisor_review_data_BUTCHER_ZURICHWEST.json')
    #MISS_MIU = os.path.join(path, 'tripadvisor_review_data_MISS_MIU.json')
    #NOOCH_BADENERSTRASSE = os.path.join(path, 'tripadvisor_review_data_NOOCH_BADENERSTRASSE.json')
    #NOOCH_RICHTI = os.path.join(path, 'tripadvisor_review_data_NOOCH_RICHTI.json')
    #OUTBACK_STADELHOFEN = os.path.join(path, 'tripadvisor_review_data_OUTBACK_STADELHOFEN.json')
