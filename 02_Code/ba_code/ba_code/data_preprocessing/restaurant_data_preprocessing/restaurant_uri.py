from enum import Enum
import os

# TODO: better solution for this
path = "../../../resources/restaurant_data"


class RestaurantUri(Enum):
    BUTCHER_BADENERSTRASSE = os.path.join(path,
                                          'Butcher_Badenerstrasse_2019-2022.csv')
    BUTCHER_NIEDERDORF = os.path.join(path,
                                      'Butcher_Niederdorf_2019-2022.csv')
    BUTCHER_ZURICHWEST = os.path.join(path,
                                      'Butcher_ZurichWest_2019-2022.csv')
    MISS_MIU = os.path.join(path,
                            'Miss_Miu_2019-2022.csv')
    NOOCH_BADENERSTRASSE = os.path.join(path,
                                        'Nooch_Badenerstrasse_2019-2022.csv')
    NOOCH_RICHTI = os.path.join(path,
                                'Nooch_Richti_2019-2022.csv')
    OUTBACK_STADELHOFEN = os.path.join(path,
                                       'Outback_Stadelhofen_2019-2022.csv')
