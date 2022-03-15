import pandas as pd
from restaurant_uri import RestaurantUri


class RestaurantDataExtractor:

    def __init__(self):
        self.__restaurant_dfs = dict()
        self.__initialize_dataframes()

    def __initialize_dataframes(self):
        for restaurant_uri in RestaurantUri:
            df = pd.read_csv(restaurant_uri.value)
            df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
            self.__restaurant_dfs[restaurant_uri] = df

    def get_dataframe(self, restaurant_uri):
        return self.__restaurant_dfs[restaurant_uri]

    def get_turnover_per_day_dataframe(self, restaurant_uri):
        df = self.__restaurant_dfs[restaurant_uri]
        df_date_turnover = df.filter(items=['date', 'turnover'])
        return df_date_turnover.groupby(['date']).sum()

    def get_turnover_per_month_dataframe(self, restaurant_uri):
        df = self.__restaurant_dfs[restaurant_uri]
        df_date_turnover = df.filter(items=['date', 'turnover'])
        return df_date_turnover.groupby(pd.Grouper(key='date', axis=0,
                                                   freq='m')).sum()
