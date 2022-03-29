import json

# Opening JSON file
f = open('tripadvisor_review_data_BUTCHER_BADENERSTRASSE.json')

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
print(data["all_reviews"][0]["author_data"])

# Closing file
f.close()