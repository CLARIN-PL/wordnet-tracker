from time import gmtime, strftime
from flask import Blueprint, redirect, request, url_for, render_template
from tracker.blueprints.user.forms import SearchForm, UserActivityForm
from tracker.blueprints.user.models import (
    CurrentUser, KeycloakServiceClient, Paginator, RealmUser,
    user_activity_day, user_activity_between_dates, user_activity_month
)

from tracker.extensions import openid_connect
from utils import value_present, sort_by_attr


user = Blueprint('user', __name__, template_folder='templates')


@user.route('/profile')
@openid_connect.require_login
def profile():
    keycloak = KeycloakServiceClient()
    current_user = CurrentUser()

    q = request.args.get('q', current_user.get_fullname())
    user_id = request.args.get('user_id', None)

    if user_id is not None:
        user_repr = keycloak.get_user_by_id(user_id)
        if user_repr is not None:
            user = RealmUser(user_repr)
        else:
            user = None
    else:
        user = current_user

    results = user_activity_month(strftime("%Y", gmtime()), strftime("%m", gmtime()), q)
    items, _ = calculate_stats(results)

    return render_template(
        'user/profile.html',
        stats=items,
        user=user,
        keycloak=KeycloakServiceClient()
    )


@user.route('/users', defaults={'page': 1})
@user.route('/users/page/<int:page>')
@openid_connect.require_login
def users(page):
    search_form = SearchForm()

    sort_by = User.sort_by(request.args.get('sort', 'id'),
                           request.args.get('direction', 'desc'))

    order_values = '{0} {1}'.format(sort_by[0], sort_by[1])

    arg = request.args.get('q', '')
    if arg == '':
        paginated_users = User.query.paginate(page, 50, True)
    else:
        paginated_users = User.query \
            .filter(User.search(request.args.get('q', ''))) \
            .order_by(User.role.asc(), text(order_values)) \
            .paginate(page, 50, True)

    return render_template(
        'user/users.html',
        form=search_form,
        users=paginated_users,
        openid_connect=openid_connect,
        current_app=current_app
    )


@user.route("/logout")
def logout():
    if openid_connect.user_loggedin:
        resp = make_response()
        # resp.set_cookie('oidc_id_token', '', expires=0)
        resp.delete_cookie('oidc_id_token')
        # openid_connect.logout()

        return redirect(url_for('page.home'))

    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('user.login'))


@user.route('/users/activity')
@openid_connect.require_login
def users_activity():

    search_from = UserActivityForm()

    if request.args.get('date_from', '') != '' and request.args.get('date_to', '') != '':
        stats = user_activity_between_dates(request.args.get('date_from', ''), request.args.get('date_to', ''))
    else:
        stats = user_activity_day(strftime("%Y-%m-%d", gmtime()))

    items, total = calculate_stats(stats)

    return render_template(
        'user/users-activity.html',
        form=search_from,
        stats=items,
        total=total,
        openid_connect=openid_connect,
        current_app=current_app
    )


def calculate_stats(stats):
    items = []
    for s in stats:
        row = dict()
        total = 0
        for i in range(0, len(s)):

            if i == 0:
                if s[i] is None:
                    row['user'] = 'None'
                else:
                    row['user'] = s[i]
            else:
                row[str(i)] = s[i]
                total = total + s[i]
        row['total'] = total
        items.append(row)

    total = dict()

    if len(items) > 0:
        for i in range(1, 11):
            total[str(i)] = sum(item[str(i)] for item in items)
        total['total'] = sum(item['total'] for item in items)

    return items, total
