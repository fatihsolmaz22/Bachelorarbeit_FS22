import pandas as pd
from ba_code.data_processing_and_analysis.prognolite.prognolite_restaurant_constants \
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
            df_restaurant_data = df[df['tenant'] == restaurant_name].reset_index(drop=True)
            df_restaurant_data = df_restaurant_data[df_restaurant_data['turnover'].notnull()]
            self.__restaurant_data[restaurant_name] = df_restaurant_data

    def get_restaurant_data(self):
        return self.__restaurant_data

    def get_restaurant_names(self):
        return self.__restaurant_data.keys()

    def get_restaurant_data_dataframe(self, restaurant):
        return self.__restaurant_data[restaurant.value]

    # TODO: remove this method later, this is not what Martin asked for
    def get_turnover_development_since_beginning_dataframe(self, restaurant, time_period='m'):
        df_date_turnover = self.get_date_turnover_dataframe(restaurant)

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
        df_date_turnover = self.get_date_turnover_dataframe(restaurant)

        df_turnover_per_time_period = None
        if time_period == 'd' or time_period == 'm' or time_period == 'Q' or time_period == 'Y':
            df_turnover_per_time_period = \
                df_date_turnover.groupby(pd.Grouper(key='d', axis=0, freq=time_period)).sum() \
                    .rename(columns={"turnover": "turnover_per_time_period"}).reset_index()
        else:
            self.__print_invalid_time_period_message()
            return

        return df_turnover_per_time_period

    def get_average_turnover_per_time_period_dataframe(self, restaurant, time_period='m'):
        df_date_turnover = self.get_date_turnover_dataframe(restaurant)

        df_average_turnover_per_time_period = None
        if time_period == 'm' or time_period == 'Q' or time_period == 'Y':
            # get turnover per day dataframe
            df_turnover_per_day = df_date_turnover \
                .groupby(pd.Grouper(key='d', axis=0, freq='d')).sum() \
                .rename(columns={"turnover": "turnover_per_day"}).reset_index()

            # get turnover per day where turnover != 0 dataframe
            df_turnover_per_day_where_turnover_not_equal_zero = \
                df_turnover_per_day[df_turnover_per_day['turnover_per_day'] != 0].reset_index(drop=True)

            # get turnover per time period dataframe, month or year dataframe
            df_average_turnover_per_time_period = df_turnover_per_day_where_turnover_not_equal_zero \
                .groupby(pd.Grouper(key='d', axis=0, freq=time_period)).mean() \
                .rename(columns={"turnover_per_day": "average_turnover_per_time_period"}).reset_index()
        else:
            print("Invalid time period, enter one of the following time periods:")
            print("'m': Month")
            print("'Q': Quarter")
            print("'Y': Year")
            return

        return df_average_turnover_per_time_period

    def __print_invalid_time_period_message(self):
        print("Invalid time period, enter one of the following time periods:")
        print("'d': Day")
        print("'m': Month")
        print("'Q': Quarter")
        print("'Y': Year")

    def get_date_turnover_dataframe(self, restaurant):
        df_restaurant_data = self.__restaurant_data[restaurant.value]
        df_date_turnover = df_restaurant_data.filter(items=['d', 'turnover'])
        return df_date_turnover


prognoliteRestaurantDataExtractor = PrognoliteRestaurantDataExtractor()
