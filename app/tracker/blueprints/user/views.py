from time import gmtime, strftime
from flask import Blueprint, redirect, request, url_for, render_template
from tracker.blueprints.user.forms import SearchForm, UserActivityForm
from tracker.blueprints.user.models import (
    CurrentUser, KeycloakServiceClient, Paginator, RealmUser,
    users_activity_day, users_activity_between_dates, user_activity_month
)
from tracker.blueprints.page.models import count_all_operations

from tracker.extensions import openid_connect
from utils import value_present, sort_by_attr


user = Blueprint('user', __name__, template_folder='templates')


@user.route('/profile')
@openid_connect.require_login
def profile():
    keycloak = KeycloakServiceClient()
    current_user = CurrentUser()

    q = request.args.get('q', current_user.get_email())
    user_id = request.args.get('user_id', None)

    if user_id is not None:
        user_repr = keycloak.get_user_by_id(user_id)
        if user_repr is not None:
            user = RealmUser(user_repr, op_service_client=keycloak)
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
    q = request.args.get('q', None)
    sort = request.args.get('sort', None)
    order = request.args.get('order', None)
    keycloak = KeycloakServiceClient()
    realm_users = keycloak.get_realm_users()

    if realm_users is not None:
        if q is not None:
            realm_users = [
                RealmUser(user_repr, op_service_client=keycloak)
                for user_repr in realm_users
                if value_present(q, user_repr)
            ]
        else:
            realm_users = [
                RealmUser(user_repr, op_service_client=keycloak)
                for user_repr in realm_users
            ]

        if sort is not None and order is not None:
            sort_by_attr(realm_users, attribute=sort, order_arg=order)

    paginator = Paginator(realm_users, in_page=30, page=page)
    users = paginator.get_page(page)

    search_form = SearchForm()

    return render_template(
        'user/users.html',
        form=search_form,
        paginator=paginator,
        users=users,
        openid_connect=openid_connect,
        keycloak=keycloak
    )


@user.route("/logout")
def logout():
    CurrentUser().logout()
    return redirect(url_for('page.home'))


@user.route('/users/activity')
@openid_connect.require_login
def users_activity():
    search_from = UserActivityForm()

    if request.args.get('date_from', '') != '' and request.args.get('date_to', '') != '':
        stats = users_activity_between_dates(request.args.get('date_from', ''), request.args.get('date_to', ''))
    else:
        stats = users_activity_day(strftime("%d-%m-%Y", gmtime()))

    items, total = calculate_stats(stats)

    return render_template(
        'user/users-activity.html',
        form=search_from,
        stats=items,
        total=total,
        keycloak=KeycloakServiceClient()
    )


def calculate_stats(stats):
    items = dict()
    total = dict()

    for s in stats:
        if "user" not in s:
            user_email = "None"
        else:
            user_email = s["user"]

        if user_email not in items:
            items[user_email] = dict()
            items[user_email]["user"] = user_email
            items[user_email]["total"] = count_all_operations(s)
            items[user_email]["senses_created"] = s["senses_created"]
            items[user_email]["senses_modified"] = s["senses_modified"]
            items[user_email]["senses_removed"] = s["senses_removed"]
            items[user_email]["sense_relations_created"] = s["sense_relations_created"]
            items[user_email]["sense_relations_modified"] = s["sense_relations_modified"]
            items[user_email]["sense_relations_removed"] = s["sense_relations_removed"]
            items[user_email]["synsets_created"] = s["synsets_created"]
            items[user_email]["synsets_modified"] = s["synsets_modified"]
            items[user_email]["synsets_removed"] = s["synsets_removed"]
            items[user_email]["synset_relations_created"] = s["synset_relations_created"]
            items[user_email]["synset_relations_modified"] = s["synset_relations_modified"]
            items[user_email]["synset_relations_removed"] = s["synset_relations_removed"]
        else:
            items[user_email]["total"] += count_all_operations(s)
            items[user_email]["senses_created"] += s["senses_created"]
            items[user_email]["senses_modified"] += s["senses_modified"]
            items[user_email]["senses_removed"] += s["senses_removed"]
            items[user_email]["sense_relations_created"] += s["sense_relations_created"]
            items[user_email]["sense_relations_modified"] += s["sense_relations_modified"]
            items[user_email]["sense_relations_removed"] += s["sense_relations_removed"]
            items[user_email]["synsets_created"] += s["synsets_created"]
            items[user_email]["synsets_modified"] += s["synsets_modified"]
            items[user_email]["synsets_removed"] += s["synsets_removed"]
            items[user_email]["synset_relations_created"] += s["synset_relations_created"]
            items[user_email]["synset_relations_modified"] += s["synset_relations_modified"]
            items[user_email]["synset_relations_removed"] += s["synset_relations_removed"]

        if len(total.keys()) == 0:
            total["total"] = count_all_operations(s)
            total["total_senses_created"] = s["senses_created"]
            total["total_senses_modified"] = s["senses_modified"]
            total["total_senses_removed"] = s["senses_removed"]
            total["total_sense_relations_created"] = s["sense_relations_created"]
            total["total_sense_relations_modified"] = s["sense_relations_modified"]
            total["total_sense_relations_removed"] = s["sense_relations_removed"]
            total["total_synsets_created"] = s["synsets_created"]
            total["total_synsets_modified"] = s["synsets_modified"]
            total["total_synsets_removed"] = s["synsets_removed"]
            total["total_synset_relations_created"] = s["synset_relations_created"]
            total["total_synset_relations_modified"] = s["synset_relations_modified"]
            total["total_synset_relations_removed"] = s["synset_relations_removed"]
        else:
            total["total"] += count_all_operations(s)
            total["total_senses_created"] += s["senses_created"]
            total["total_senses_modified"] += s["senses_modified"]
            total["total_senses_removed"] += s["senses_removed"]
            total["total_sense_relations_created"] += s["sense_relations_created"]
            total["total_sense_relations_modified"] += s["sense_relations_modified"]
            total["total_sense_relations_removed"] += s["sense_relations_removed"]
            total["total_synsets_created"] += s["synsets_created"]
            total["total_synsets_modified"] += s["synsets_modified"]
            total["total_synsets_removed"] += s["synsets_removed"]
            total["total_synset_relations_created"] += s["synset_relations_created"]
            total["total_synset_relations_modified"] += s["synset_relations_modified"]
            total["total_synset_relations_removed"] += s["synset_relations_removed"]

    return list(items.values()), total
