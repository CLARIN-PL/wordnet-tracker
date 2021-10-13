from flask import Blueprint, render_template, request
from lib.util_sqlalchemy import status, parts_of_speech, domain, aspect
from tracker.blueprints.sense.forms import SenseRelationsHistoryForm, SenseHistoryForm, SenseAttributesHistoryForm
from tracker.blueprints.sense.models import get_sense_relation_list, find_sense, \
    find_sense_history, find_sense_incoming_relations, find_sense_outgoing_relations, \
    get_senses_history_search, get_user_name_list, get_sense_relations_history_search, \
    find_sense_incoming_relations_history, find_sense_outgoing_relations_history, \
    get_senses_attributes_history_search, find_sense_emotional_annotation, find_sense_emotional_annotation_history
from tracker.blueprints.user.models import KeycloakServiceClient
from tracker.extensions import openid_connect

sense = Blueprint('sense', __name__, template_folder='templates')


class SenseistoryForm(object):
    pass


@sense.route('/senses/history', defaults={'page': 1})
@sense.route('/senses/history/page/<int:page>')
@openid_connect.require_login
def senses_history(page):
    senses = get_senses_history_search(
        request.args.get('date_from', ''),
        request.args.get('date_to', ''),
        request.args.get('sense_id', ''),
        request.args.get('user', ''),
        request.args.get('pos', ''),
        page
    )

    return render_template(
        'sense/sense-history.html',
        form=SenseHistoryForm(),
        users=get_user_name_list(),
        sense_history=senses,
        status=status(),
        pos=parts_of_speech(),
        domain=domain(),
        keycloak=KeycloakServiceClient()
    )


@sense.route('/senses/attributes/history', defaults={'page': 1})
@sense.route('/senses/attributes/history/page/<int:page>')
@openid_connect.require_login
def senses_attributes_history(page):
    sense_attributes_history = get_senses_attributes_history_search(
        request.args.get('date_from', ''),
        request.args.get('date_to', ''),
        request.args.get('sense_id', ''),
        request.args.get('user', ''),
        page
    )

    return render_template(
        'sense/sense-attributes-history.html',
        form=SenseAttributesHistoryForm(),
        users=get_user_name_list(),
        sense_attributes_history=sense_attributes_history,
        keycloak=KeycloakServiceClient()
    )


@sense.route('/senses/relations/history', defaults={'page': 1})
@sense.route('/senses/relations/history/page/<int:page>')
@openid_connect.require_login
def senses_relations_history(page):
    relations = get_sense_relations_history_search(
        request.args.get('date_from', ''),
        request.args.get('date_to', ''),
        request.args.get('sense_id', ''),
        request.args.get('user', ''),
        request.args.get('relation_type', ''),
        page
    )

    return render_template(
        'sense/sense-relations-history.html',
        form=SenseRelationsHistoryForm(),
        users=get_user_name_list(),
        relations=get_sense_relation_list(),
        history=relations,
        keycloak=KeycloakServiceClient()
    )


@sense.route('/sense/<string:id>')
@openid_connect.require_login
def sense_by_id(id):
    return render_template(
        'sense/sense.html',
        sense=find_sense(id),
        pos=parts_of_speech(),
        domain=domain(),
        status=status(),
        aspect=aspect(),
        sense_history=find_sense_history(id),
        incoming_rel=find_sense_incoming_relations(id),
        outgoing_rel=find_sense_outgoing_relations(id),
        outgoing_history=find_sense_outgoing_relations_history(id),
        incoming_history=find_sense_incoming_relations_history(id),
        keycloak=KeycloakServiceClient(),
        emotional=find_sense_emotional_annotation(id),
        emotional_history=find_sense_emotional_annotation_history(id)
    )
