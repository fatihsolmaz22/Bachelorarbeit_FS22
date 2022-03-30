import pandas as pd
from ba_code.data_preprocessing.restaurant_data_preprocessing.restaurant_constants import RestaurantUri


# TODO: not clean, code duplication (interface or superclass)
class RestaurantDataExtractor:

    def __init__(self):
        self.__restaurant_data = dict()
        self.__initialize_dataframes()

    def __initialize_dataframes(self):
        df = pd.read_csv(RestaurantUri.RESTAURANT_DATA.value).drop_duplicates()
        df['d'] = pd.to_datetime(df['d'])
        restaurant_names = df.drop_duplicates(subset=['tenant'])['tenant'].to_list()
        restaurant_names = [restaurant_name.strip() for restaurant_name in restaurant_names]

        for restaurant_name in restaurant_names:
            self.__restaurant_data[restaurant_name] = df[df['tenant'] == restaurant_name].reset_index(drop=True)

    def get_restaurant_data(self):
        return self.__restaurant_data

    def get_restaurant_names(self):
        return self.__restaurant_data.keys()

    def get_dataframe(self, restaurant):
        return self.__restaurant_data[restaurant.value]

    def get_turnover_per_day_dataframe(self, restaurant):
        df_date_turnover = self.__get_date_turnover_dataframe(restaurant)
        return df_date_turnover.groupby(pd.Grouper(key='d', axis=0,
                                                   freq='d')).sum()

    def get_turnover_per_month_dataframe(self, restaurant):
        df_date_turnover = self.__get_date_turnover_dataframe(restaurant)
        return df_date_turnover.groupby(pd.Grouper(key='d', axis=0,
                                                   freq='m')).sum()

    def __get_date_turnover_dataframe(self, restaurant):
        df = self.__restaurant_data[restaurant.value]
        return df.filter(items=['d', 'turnover'])




