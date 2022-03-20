from enum import Enum
import os
from ba_code.path import REVIEW_DATA_PATH

path = REVIEW_DATA_PATH


class ReviewUri(Enum):
    NOOCH_BADENERSTRASSE = os.path.join(path, 'tripadvisor_review_data_NOOCH_BADENERSTRASSE.json')
    # NOOCH_STEINFELS = os.path.join(path, 'tripadvisor_review_data_NOOCH_STEINFELS.json')
