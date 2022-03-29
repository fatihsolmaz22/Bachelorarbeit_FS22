from enum import Enum

list_of_stats = ['145 Contributions', '92 Cities visited', '398 Helpful votes']

class AuthorStats(Enum):
    CONTRIBUTIONS = "Contributions"
    CITIES_VISITED = "Cities visited"
    HELPFUL_VOTES = "Helpful votes"
    PHOTOS = "Photos"

def get_stats_as_dict_from_list(list_of_stats):
    stats_dict = {}
    print(list_of_stats)
    for stat in list_of_stats:
        for stat_attribute in AuthorStats:
            print(stat)
            print(stat_attribute.value)
            if stat_attribute.value in stat:
                stat_value = int(stat.replace(",", "").split(" ")[0])
                stats_dict[stat_attribute.value] = stat_value
            else:
                stats_dict[stat_attribute.value] = 0
    return stats_dict

if AuthorStats.CONTRIBUTIONS.value in list_of_stats[0]:
    print("yes")