import pandas as pd
from ba_code.data_preprocessing.prognolite_restaurant_data_preprocessing.prognolite_restaurant_constants \
    import PrognoliteRestaurantDataUri, Restaurant


class PrognoliteRestaurantDataExtractor:

    def __init__(self):
        self.__restaurant_data = dict()
        self.__initialize_dataframes()

    def __initialize_dataframes(self):
        df = pd.read_csv(PrognoliteRestaurantDataUri.PROGNOLITE_RESTAURANT_DATA.value).drop_duplicates()
        df['d'] = pd.to_datetime(df['d'])
        restaurant_names = df.drop_duplicates(subset=['tenant'])['tenant'].to_list()
        restaurant_names = [restaurant_name.strip() for restaurant_name in restaurant_names]

        for restaurant_name in restaurant_names:
            self.__restaurant_data[restaurant_name] = df[df['tenant'] == restaurant_name].reset_index(drop=True)

    def get_restaurant_data(self):
        return self.__restaurant_data

    def get_restaurant_names(self):
        return self.__restaurant_data.keys()

    def get_restaurant_data_dataframe(self, restaurant):
        return self.__restaurant_data[restaurant.value]

    def get_turnover_development_since_beginning_dataframe(self, restaurant, time_period='m'):
        df_date_turnover = self.__get_date_turnover_dataframe(restaurant)

        df_turnover_development_since_beginning = None
        if time_period == 'd' or time_period == 'm' or time_period == 'Y':
            df_turnover_development_since_beginning = \
                df_date_turnover.groupby(pd.Grouper(key='d', axis=0, freq=time_period)) \
                    .sum()['turnover'].cumsum().reset_index()
        elif time_period == 'Q':
            df_turnover_development_since_beginning = \
                df_date_turnover.groupby(df_date_turnover['d'].dt.to_period(time_period))['turnover'].agg(
                    'sum').cumsum().reset_index()
        else:
            self.__print_invalid_time_period_message()
            return

        return df_turnover_development_since_beginning

    def get_turnover_per_time_period_dataframe(self, restaurant, time_period='m'):
        df_date_turnover = self.__get_date_turnover_dataframe(restaurant)

        df_date_turnover_per_time_period = None
        if time_period == 'd' or time_period == 'm' or time_period == 'Y':
            df_date_turnover_per_time_period = \
                df_date_turnover.groupby(pd.Grouper(key='d', axis=0, freq=time_period)).sum().reset_index()
        elif time_period == 'Q':
            df_date_turnover_per_time_period = \
                df_date_turnover.groupby(df_date_turnover['d'].dt.to_period(time_period))['turnover'].agg(
                    'sum').reset_index()
        else:
            self.__print_invalid_time_period_message()
            return

        return df_date_turnover_per_time_period

    def __print_invalid_time_period_message(self):
        print("Invalid time period, enter one of the following time periods:")
        print("'d': Day")
        print("'m': Month")
        print("'Q': Quarter")
        print("'Y': Year")

    def __get_date_turnover_dataframe(self, restaurant):
        df_restaurant_data = self.__restaurant_data[restaurant.value]
        df_date_turnover = df_restaurant_data.filter(items=['d', 'turnover'])
        df_date_turnover['turnover'] = df_date_turnover['turnover'].fillna(0)
        return df_date_turnover


prognoliteRestaurantDataExtractor = PrognoliteRestaurantDataExtractor()
