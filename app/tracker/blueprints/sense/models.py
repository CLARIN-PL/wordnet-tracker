from time import strftime

import requests
import json
from config.settings import API_SERVER_URL as api_server_url


def get_senses_history_search(date_from, date_to, sense_id, user, pos, page):
    sense_url = api_server_url + "sense-history/search?"
    if date_from is not '':
        sense_url += "&date_from=" + date_from
    if date_to is not '':
        sense_url += "&date_to=" + date_to
    if sense_id is not '':
        sense_url += "&sense_id=" + sense_id
    if user is not '':
        sense_url += "&user=" + user
    if pos is not '':
        sense_url += "&part_of_speech=" + pos
    if page is not '':
        sense_url += "&page=" + str(page)

    try:
        response = requests.get(
            url=sense_url
        )
        return json.loads(response.text)

    except Exception:
        return {}


def get_senses_attributes_history_search(date_from, date_to, sense_id, user, page):
    sense_url = api_server_url + "sense-history/attributes/search?"
    if date_from is not '':
        sense_url += "&date_from=" + date_from
    if date_to is not '':
        sense_url += "&date_to=" + date_to
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


def get_user_name_list():
    try:
        response = requests.get(
            url=api_server_url + "users"
        )
        return json.loads(response.text)

    except Exception:
        return []


def get_sense_relation_list():
    try:
        response = requests.get(
            url=api_server_url + "senses/relations"
        )
        return json.loads(response.text)["relations"]

    except Exception:
        return []


def find_sense_history(id):
    try:
        response = requests.get(
            url=api_server_url + "sense-history/" + id
        )
        return json.loads(response.text)["sense_history"]

    except Exception:
        return {}


def get_sense_relations_history_search(date_from, date_to, sense_id, user, relation_type, page):
    sense_url = api_server_url + "sense-history/relations/search?"
    if date_from is not '':
        sense_url += "&date_from=" + date_from
    if date_to is not '':
        sense_url += "&date_to=" + date_to
    if sense_id is not '':
        sense_url += "&sense_id=" + sense_id
    if user is not '':
        sense_url += "&user=" + user
    if relation_type is not '':
        sense_url += "&relation_type=" + relation_type
    if page is not '':
        sense_url += "&page=" + str(page)

    try:
        response = requests.get(
            url=sense_url
        )
        return json.loads(response.text)

    except Exception:
        return {}


def find_sense(id):
    try:
        response = requests.get(
            url=api_server_url + "senses/" + id
        )
        return json.loads(response.text)

    except Exception:
        return {}


def find_sense_incoming_relations(id):
    try:
        response = requests.get(
            url=api_server_url + "senses/incoming-relations/" + id
        )
        return json.loads(response.text)["incoming_relations"]

    except Exception:
        return []


def find_sense_outgoing_relations(id):
    try:
        response = requests.get(
            url=api_server_url + "senses/outgoing-relations/" + id
        )
        return json.loads(response.text)["outgoing_relations"]

    except Exception:
        return []


def find_sense_incoming_relations_history(id):
    try:
        response = requests.get(
            url=api_server_url + "sense-history/incoming-relations/" + id
        )
        return json.loads(response.text)["incoming_relations_history"]

    except Exception:
        return {}


def find_sense_outgoing_relations_history(id):
    try:
        response = requests.get(
            url=api_server_url + "sense-history/outgoing-relations/" + id
        )
        return json.loads(response.text)["outgoing_relations_history"]

    except Exception:
        return {}


def find_sense_emotional_annotation(id):
    try:
        response = requests.get(
            url=api_server_url + "senses/emotional-annotation/" + id
        )
        return json.loads(response.text)

    except Exception:
        return {}


def find_sense_emotional_annotation_history(id):
    try:
        response = requests.get(
            url=api_server_url + "sense-history/emotional-annotation/" + id
        )
        return json.loads(response.text)["emotional_annotation_history_list"]

    except Exception:
        return []


def find_sense_morphologies(id):
    try:
        response = requests.get(
            url=api_server_url + "senses/morphologies/" + id
        )
        return json.loads(response.text)["morphologies"]

    except Exception:
        return []
