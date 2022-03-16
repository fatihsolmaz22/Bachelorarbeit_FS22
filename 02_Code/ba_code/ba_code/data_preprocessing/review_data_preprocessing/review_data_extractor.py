import pandas as pd
from ba_code.data_preprocessing.review_data_preprocessing.review_uri import ReviewUri

# TODO: not clean, code duplication (interface or superclass)
class ReviewDataExtractor:

    def __init__(self):
        self.__review_dfs = dict()
        self.__initialize_dataframes()

    def __initialize_dataframes(self):
        for review_uri in ReviewUri:
            df = pd.read_json(review_uri.value)
            self.__review_dfs[review_uri] = df

    def get_monthly_rating_for_restaurant_dataframe(self, review_uri):
        df = self.__review_dfs[review_uri]
        df = df.filter(items=["date", "rating"])
        return df.groupby(pd.Grouper(key='date', axis=0,
                                     freq='m')).mean().fillna(0)

    def get_dataframe(self, review_uri):
        return self.__review_dfs[review_uri]

