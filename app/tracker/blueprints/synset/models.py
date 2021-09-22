import requests
import json
from config.settings import API_SERVER_URL as api_server_url


def search_synsets_history(date_from, date_to, synset_id, user, page):
    synset_url = api_server_url + "synset-history/search?"
    if date_from is not '':
        synset_url += "&date_from=" + date_from
    if date_to is not '':
        synset_url += "&date_to=" + date_to
    if synset_id is not '':
        synset_url += "&synset_id=" + synset_id
    if user is not '':
        synset_url += "&user=" + user
    if page is not '':
        synset_url += "&page=" + str(page)

    try:
        response = requests.get(
            url=synset_url
        )
        return json.loads(response.text)

    except Exception:
        return {}


def search_synsets_attributes_history(date_from, date_to, synset_id, user, page):
    synset_url = api_server_url + "synset-history/attributes/search?"
    if date_from is not '':
        synset_url += "&date_from=" + date_from
    if date_to is not '':
        synset_url += "&date_to=" + date_to
    if synset_id is not '':
        synset_url += "&synset_id=" + synset_id
    if user is not '':
        synset_url += "&user=" + user
    if page is not '':
        synset_url += "&page=" + str(page)

    try:
        response = requests.get(
            url=synset_url
        )
        return json.loads(response.text)

    except Exception:
        return {}


def search_synset_relations_history(date_from, date_to, synset_id, user, relation_type, page):
    synset_url = api_server_url + "synset-history/relations/search?"
    if date_from is not '':
        synset_url += "&date_from=" + date_from
    if date_to is not '':
        synset_url += "&date_to=" + date_to
    if synset_id is not '':
        synset_url += "&synset_id=" + synset_id
    if user is not '':
        synset_url += "&user=" + user
    if relation_type is not '':
        synset_url += "&relation_type=" + relation_type
    if page is not '':
        synset_url += "&page=" + str(page)

    try:
        response = requests.get(
            url=synset_url
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


def get_synset_relation_list():
    try:
        response = requests.get(
            url=api_server_url + "synsets/relations"
        )
        return json.loads(response.text)["relations"]

    except Exception:
        return []


def find_synset(id):
    try:
        response = requests.get(
            url=api_server_url + "synsets/" + id
        )
        return json.loads(response.text)

    except Exception:
        return {}


def find_synset_incoming_relations(id):
    try:
        response = requests.get(
            url=api_server_url + "synsets/incoming-relations/" + id
        )
        return json.loads(response.text)["incoming_relations"]

    except Exception:
        return []


def find_synset_outgoing_relations(id):
    try:
        response = requests.get(
            url=api_server_url + "synsets/outgoing-relations/" + id
        )
        return json.loads(response.text)["outgoing_relations"]

    except Exception:
        return []


def find_synset_senses(id):
    try:
        response = requests.get(
            url=api_server_url + "synsets/senses/" + id
        )
        return json.loads(response.text)["senses"]

    except Exception:
        return []


def find_synset_sense_history(id):
    try:
        response = requests.get(
            url=api_server_url + "synset-history/senses/" + id
        )
        return json.loads(response.text)["sense_history"]

    except Exception:
        return []


def find_synset_history(id):
    try:
        response = requests.get(
            url=api_server_url + "synset-history/" + id
        )
        return json.loads(response.text)["synset_history"]

    except Exception:
        return []


def find_synset_incoming_relations_history(id):
    try:
        response = requests.get(
            url=api_server_url + "synset-history/incoming-relations/" + id
        )
        return json.loads(response.text)["incoming_relations_history"]

    except Exception:
        return []


def find_synset_outgoing_relations_history(id):
    try:
        response = requests.get(
            url=api_server_url + "synset-history/outgoing-relations/" + id
        )
        return json.loads(response.text)["outgoing_relations_history"]

    except Exception:
        return []