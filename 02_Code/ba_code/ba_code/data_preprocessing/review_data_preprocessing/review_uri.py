from enum import Enum
import os

# TODO: buggy, better solution for this needed!!
path = "../../../resources/review_data"


class ReviewUri(Enum):
    NOOCH_BADENERSTRASSE = os.path.join(path, 'tripadvisor_review_data_NOOCH_BADENERSTRASSE.json')
    NOOCH_STEINFELS = os.path.join(path, 'tripadvisor_review_data_NOOCH_STEINFELS.json')
