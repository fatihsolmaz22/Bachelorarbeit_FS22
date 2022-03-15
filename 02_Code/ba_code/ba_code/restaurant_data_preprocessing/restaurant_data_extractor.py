import pandas as pd
from restaurant_data import RestaurantData


class RestaurantDataExtractor:

    def __init__(self):
        self.__restaurant_dfs = dict()
        self.__initialize_dataframes()

    def __initialize_dataframes(self):
        for restaurant_data in RestaurantData:
            df = pd.read_csv(restaurant_data.value)
            df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
            self.__restaurant_dfs[restaurant_data] = df

    def get_dataframe(self, restaurant_data):
        return self.__restaurant_dfs[restaurant_data]

    def get_turnover_per_day_dataframe(self, restaurant_data):
        df = self.__restaurant_dfs[restaurant_data]
        df_date_turnover = df.filter(items=['date', 'turnover'])
        return df_date_turnover.groupby(['date']).sum()

    def get_turnover_per_month_dataframe(self, restaurant_data):
        df = self.__restaurant_dfs[restaurant_data]
        df_date_turnover = df.filter(items=['date', 'turnover'])
        return df_date_turnover.groupby(pd.Grouper(key='date', axis=0,
                                                   freq='m')).sum()
