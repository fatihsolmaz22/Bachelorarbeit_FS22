from ba_code.data_preprocessing.prognolite_restaurant_data_preprocessing.prognolite_restaurant_data_extractor import \
    PrognoliteRestaurantDataExtractor, Restaurant
import pandas as pd


def test_get_average_turnover_per_time_period_dataframe(prognolite_restaurant_data_extractor):
    restaurant = Restaurant.NOOCH_USTER

    df_date_turnover = prognolite_restaurant_data_extractor.get_date_turnover_dataframe(restaurant)

    # get turnover per day dataframe
    df_turnover_per_day = df_date_turnover \
        .groupby(pd.Grouper(key='d', axis=0, freq='d')).sum() \
        .rename(columns={"turnover": "turnover_per_day"}).reset_index()

    # get turnover per day where turnover != 0 dataframe
    df_turnover_per_day_where_turnover_not_equal_zero = \
        df_turnover_per_day[df_turnover_per_day['turnover_per_day'] != 0].reset_index(drop=True)

    # testing get average_turnvover_per_month
    df_average_turnover_per_month = \
        prognolite_restaurant_data_extractor.get_average_turnover_per_time_period_dataframe(restaurant, 'm')

    print("get_average_turnover_per_month works correct:",
          df_average_turnover_per_month.iloc[38]['average_turnover_per_time_period'] ==
          df_turnover_per_day_where_turnover_not_equal_zero.iloc[747:760]['turnover_per_day'].mean())

    # testing get average_turnvover_per_quarter
    df_average_turnover_per_quarter = \
        prognolite_restaurant_data_extractor.get_average_turnover_per_time_period_dataframe(restaurant, 'Q')

    print("get_average_turnover_per_quarter works correct:",
          df_average_turnover_per_quarter.iloc[13]['average_turnover_per_time_period'] ==
          df_turnover_per_day_where_turnover_not_equal_zero.iloc[719:760]['turnover_per_day'].mean())

    # testing get average_turnvover_per_year
    df_average_turnover_per_year = \
        prognolite_restaurant_data_extractor.get_average_turnover_per_time_period_dataframe(restaurant, 'Y')

    print("get_average_turnover_per_year works correct:",
          df_average_turnover_per_year.iloc[3]['average_turnover_per_time_period'] ==
          df_turnover_per_day_where_turnover_not_equal_zero.iloc[615:760]['turnover_per_day'].mean())


prognoliteRestaurantDataExtractor = PrognoliteRestaurantDataExtractor()
test_get_average_turnover_per_time_period_dataframe(prognoliteRestaurantDataExtractor)
