from calendar import monthrange
from datetime import datetime, timedelta
from time import gmtime, strftime
from ply.cpp import xrange

import requests
import json
from config.settings import API_SERVER_URL as api_server_url


def find_created_items_today():
    result_dict = {"new_senses": 0,
                   "new_sense_relations": 0,
                   "new_synsets": 0,
                   "new_synset_relations": 0}
    try:
        response = requests.get(
            url=api_server_url + "stats/today"
        )
        json_data = json.loads(response.text)

        for stats in json_data["users_stats"]:
            result_dict["new_senses"] += stats["senses_created"]
            result_dict["new_sense_relations"] += stats["sense_relations_created"]
            result_dict["new_synsets"] += stats["synsets_created"]
            result_dict["new_synset_relations"] += stats["synset_relations_created"]
    except Exception:
        pass

    return result_dict


def find_day_activity(date, user):
    users = set()
    activity = []

    try:
        if user != '':
            response = requests.get(
                url=api_server_url + "users/" + user + "/daily-activity/" + date
            )
            json_data = json.loads(response.text)

            users.add(json_data["user"])
            for stats in json_data["stats"]:
                stats["user"] = json_data["user"]
                activity.append(stats)
        else:
            response = requests.get(
                url=api_server_url + "stats/date/" + date
            )
            json_data = json.loads(response.text)

            for stats in json_data["users_stats"]:
                users.add(stats["user"])
                activity.append(stats)

    except Exception:
        pass

    return activity, users


def count_all_operations(stats):
    return int(stats["senses_created"] +
               stats["senses_modified"] +
               stats["senses_removed"] +
               stats["sense_relations_created"] +
               stats["sense_relations_modified"] +
               stats["sense_relations_removed"] +
               stats["synsets_created"] +
               stats["synsets_modified"] +
               stats["synsets_removed"] +
               stats["synset_relations_created"] +
               stats["synset_relations_modified"] +
               stats["synset_relations_removed"])


def users_daily_activity(date, user):
    if date == '':
        date = strftime("%d-%m-%Y", gmtime())
    activity, users = find_day_activity(date, user)

    d = []
    start_date = datetime(2018, 1, 1, 0, 0, 0)
    for td in (start_date + timedelta(hours=1 * it) for it in xrange(24)):
        row = dict()
        row['y'] = td.strftime("%H:%M")
        for u in users:
            row[u] = 0
        d.append(row)

    for act in activity:
        d[act["hour"]][act["user"]] = count_all_operations(act)

    return d, users


def find_user_activity_month(year, month, user):
    users = set()
    d = []

    if 9 >= int(month) >= 0:
        month = '0' + str(int(month))

    try:
        response = requests.get(
            url=api_server_url + "users/" + user + "/monthly-activity/01-" + month + "-" + year
        )
        json_data = json.loads(response.text)
        user = json_data["user"]
        users.add(user)
        activity = json_data["stats"]

        _max = monthrange(int(strftime("%Y", gmtime())), int(strftime("%m", gmtime())))[1] + 1
        for m in range(1, _max):
            row = dict()
            row['y'] = str(m)
            row[user] = 0
            d.append(row)

        for act in activity:
            d[int(act["day"]) - 1][user] = count_all_operations(act)

    except Exception:
        pass

    return d, users
