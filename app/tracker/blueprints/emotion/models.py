import requests
import json
from config.settings import API_SERVER_URL as api_server_url


def get_emotional_annotation_search(sense_id, user, page):
    sense_url = api_server_url + "sense-history/emotional-annotation/search?"
    if sense_id is not '':
        sense_url += "&sense_id=" + sense_id
    if user is not '':
        sense_url += "&user=" + user
    if page is not '':
        sense_url += "&page=" + str(page)

    try:
        response = requests.get(
            url=sense_url
        )
        return json.loads(response.text)

    except Exception:
        return {}
