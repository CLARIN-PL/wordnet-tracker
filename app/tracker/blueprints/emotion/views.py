from flask import Blueprint, render_template, request
from tracker.blueprints.emotion.forms import EmotionDisagreementForm
from tracker.blueprints.emotion.models import get_emotional_annotation_search
from tracker.blueprints.sense.models import get_user_name_list
from tracker.blueprints.user.models import KeycloakServiceClient
from tracker.extensions import openid_connect

emotion = Blueprint('emotion', __name__, template_folder='templates')


@emotion.route('/emotional-annotation', defaults={'page': 1})
@emotion.route('/emotional-annotation/page/<int:page>')
@openid_connect.require_login
def emotional_annotation(page):
    emotional = get_emotional_annotation_search(
        request.args.get('sense_id', ''),
        request.args.get('user', ''),
        page
    )

    return render_template(
        '/emotion/emotional-annotation.html',
        form=EmotionDisagreementForm(),
        users=get_user_name_list(),
        emotions=emotional,
        keycloak=KeycloakServiceClient()
    )
