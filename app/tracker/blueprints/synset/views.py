from flask import Blueprint, render_template, request
from lib.util_sqlalchemy import status, parts_of_speech
from tracker.blueprints.synset.forms import SynsetHistoryForm, SynsetRelationsHistoryForm, SynsetAttributesHistoryForm
from tracker.blueprints.synset.models import get_user_name_list, search_synset_relations_history, \
    get_synset_relation_list, find_synset_incoming_relations, find_synset_incoming_relations_history, \
    find_synset_outgoing_relations, find_synset_senses, find_synset_sense_history, search_synsets_history, \
    find_synset_outgoing_relations_history, find_synset, find_synset_history, search_synsets_attributes_history
from tracker.blueprints.user.models import KeycloakServiceClient
from tracker.extensions import openid_connect


synset = Blueprint('synset', __name__, template_folder='templates')


@synset.route('/synsets', defaults={'page': 1})
@synset.route('/synsets/page/<int:page>')
@openid_connect.require_login
def synsets(page):
    paginated_synsets = []
    # TODO: not implemented

    return render_template(
        'synset/synsets.html',
        synsets=paginated_synsets,
        keycloak=KeycloakServiceClient()
    )


@synset.route('/synsets/relations/history', defaults={'page': 1})
@synset.route('/synsets/relations/history/page/<int:page>')
@openid_connect.require_login
def synsets_relations_history(page):
    history = search_synset_relations_history(
            request.args.get('date_from', ''),
            request.args.get('date_to', ''),
            request.args.get('synset_id', ''),
            request.args.get('user', ''),
            request.args.get('relation_type', ''),
            page
        )

    return render_template(
        'synset/synset-relations-history.html',
        form=SynsetRelationsHistoryForm(),
        users=get_user_name_list(),
        relations=get_synset_relation_list(),
        history=history,
        keycloak=KeycloakServiceClient()
    )


@synset.route('/synsets/history', defaults={'page': 1})
@synset.route('/synsets/history/page/<int:page>')
@openid_connect.require_login
def synsets_history(page):
    history = search_synsets_history(
            request.args.get('date_from', ''),
            request.args.get('date_to', ''),
            request.args.get('synset_id', ''),
            request.args.get('user', ''),
            page
        )

    return render_template(
        'synset/synset-history.html',
        form=SynsetHistoryForm(),
        users=get_user_name_list(),
        synsets=history,
        keycloak=KeycloakServiceClient()
    )


@synset.route('/synsets/attributes/history', defaults={'page': 1})
@synset.route('/synsets/attributes/history/page/<int:page>')
@openid_connect.require_login
def synsets_attributes_history(page):
    synsets_attributes_history = search_synsets_attributes_history(
            request.args.get('date_from', ''),
            request.args.get('date_to', ''),
            request.args.get('synset_id', ''),
            request.args.get('user', ''),
            page
        )

    return render_template(
        'synset/synset-attributes-history.html',
        form=SynsetAttributesHistoryForm(),
        users=get_user_name_list(),
        synsets_attributes_history=synsets_attributes_history,
        keycloak=KeycloakServiceClient()
    )


@synset.route('/synsets/<string:id>')
@openid_connect.require_login
def synset_by_id(id):
    return render_template(
        'synset/synset.html',
        status=status(),
        pos=parts_of_speech(),
        incoming_rel=find_synset_incoming_relations(id),
        outgoing_rel=find_synset_outgoing_relations(id),
        outgoing_history=find_synset_outgoing_relations_history(id),
        incoming_history=find_synset_incoming_relations_history(id),
        senses_history=find_synset_sense_history(id),
        senses=find_synset_senses(id),
        synset=find_synset(id),
        synset_history=find_synset_history(id),
        keycloak=KeycloakServiceClient()
    )
