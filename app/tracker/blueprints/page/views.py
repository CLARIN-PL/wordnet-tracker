from time import strftime, gmtime
from flask import Blueprint, render_template, jsonify, request

from tracker.blueprints.page.models import find_created_items_today, find_user_activity_month, users_daily_activity
from tracker.blueprints.user.models import KeycloakServiceClient
from tracker.extensions import openid_connect

page = Blueprint('page', __name__, template_folder='templates')


@page.route('/')
@openid_connect.require_login
def home():
    return render_template(
        'page/dashboard.html',
        stats=find_created_items_today(),
        keycloak=KeycloakServiceClient()
    )


@page.route('/api/users/activity/now')
def users_activity_now():
    user = request.args.get('q', '')
    d, users = users_daily_activity('', user)

    response = {
        'data': d,
        'xkey': 'y',
        'ykeys': list(users),
        'labels': list(users),
        'fillOpacity': 0.6,
        'hideHover': 'auto',
        'behaveLikeLine': bool('true'),
        'resize': bool('true'),
        'pointFillColors': ['#ffffff'],
        'pointStrokeColors': ['black'],
        'element': 'user-activity-today',
        'parseTime': bool('false'),
        'stacked': bool('true')
    }

    return jsonify(response), 200


@page.route('/api/users/activity/date/<string:_date>')
def users_activity_by_day(_date):
    user = request.args.get('q', '')
    d, users = users_daily_activity(_date, user)

    response = {
        'data': d,
        'xkey': 'y',
        'ykeys': list(users),
        'labels': list(users),
        'fillOpacity': 0.6,
        'hideHover': 'auto',
        'behaveLikeLine': bool('true'),
        'resize': bool('true'),
        'pointFillColors': ['#ffffff'],
        'pointStrokeColors': ['black'],
        'element': 'user-activity-today',
        'parseTime': bool('false'),
        'stacked': bool('true')
    }

    return jsonify(response), 200


@page.route('/api/users/activity/monthly')
def users_activity_monthly():
    user = request.args.get('q', '')
    d, users = find_user_activity_month(strftime("%Y", gmtime()), strftime("%m", gmtime()), user)

    response = {
        'data': d,
        'xkey': 'y',
        'ykeys': list(users),
        'labels': list(users),
        'fillOpacity': 0.6,
        'hideHover': 'auto',
        'behaveLikeLine': bool('true'),
        'resize': bool('true'),
        'pointFillColors': ['#ffffff'],
        'pointStrokeColors': ['black'],
        'element': 'user-activity-monthly',
        'parseTime': bool('false'),
        'stacked': bool('true')
    }

    return jsonify(response), 200
