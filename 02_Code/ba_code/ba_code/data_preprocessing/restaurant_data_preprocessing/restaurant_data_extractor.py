import pandas as pd
from ba_code.data_preprocessing.restaurant_data_preprocessing.restaurant_uri import RestaurantUri

# TODO: not clean, code duplication (interface or superclass)
class RestaurantDataExtractor:

    def __init__(self):
        self.__restaurant_data = dict()
        self.__initialize_dataframes()

    def __initialize_dataframes(self):
        for restaurant_uri in RestaurantUri:
            df = pd.read_csv(restaurant_uri.value)
            df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
            self.__restaurant_data[restaurant_uri] = df

    def get_restaurant_name(self, restaurant_uri):
        restaurant_name_location_array = str(restaurant_uri).lower().split(".")[1].split("_")
        restaurant_name_location_array = [element.capitalize() for element in restaurant_name_location_array]
        return ' '.join(restaurant_name_location_array)

    def get_dataframe(self, restaurant_uri):
        return self.__restaurant_data[restaurant_uri]

    def get_turnover_per_day_dataframe(self, restaurant_uri):
        df_date_turnover = self.__get_date_turnover_dataframe(restaurant_uri)
        return df_date_turnover.groupby(['date']).sum()

    def get_turnover_per_month_dataframe(self, restaurant_uri):
        df_date_turnover = self.__get_date_turnover_dataframe(restaurant_uri)
        return df_date_turnover.groupby(pd.Grouper(key='date', axis=0,
                                                   freq='m')).sum()
    
    def __get_date_turnover_dataframe(self, restaurant_uri):
        df = self.__restaurant_data[restaurant_uri]
        return df.filter(items=['date', 'turnover'])
