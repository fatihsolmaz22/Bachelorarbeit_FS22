import json
import os
from ba_code.path import TRIPADVISOR_RESTAURANT_DATA_PATH

# Opening JSON file
f = open(os.path.join(TRIPADVISOR_RESTAURANT_DATA_PATH, 'tripadvisor_review_data_BUTCHER_BADENERSTRASSE.json'))

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
print(data["all_reviews"][14]["review_data"])

# Closing file
f.close()