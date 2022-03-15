from enum import Enum
import os

# TODO: discuss a better solution with Fatih
os.chdir("../../resources/restaurant_data")


class RestaurantData(Enum):
    BUTCHER_BADENERSTRASSE = os.path.join(os.getcwd(),
                                          'Butcher_Badenerstrasse_2019-2022.csv')
    BUTCHER_NIEDERDORF = os.path.join(os.getcwd(),
                                      'Butcher_Niederdorf_2019-2022.csv')
    BUTCHER_ZURICHWEST = os.path.join(os.getcwd(),
                                      'Butcher_ZurichWest_2019-2022.csv')
    MISS_MIU = os.path.join(os.getcwd(),
                            'Miss_Miu_2019-2022.csv')
    NOOCH_BADENERSTRASSE = os.path.join(os.getcwd(),
                                        'Nooch_Badenerstrasse_2019-2022.csv')
    NOOCH_RICHTI = os.path.join(os.getcwd(),
                                'Nooch_Richti_2019-2022.csv')
    OUTBACK_STADELHOFEN = os.path.join(os.getcwd(),
                                       'Outback_Stadelhofen_2019-2022.csv')
